import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function
import json
import sys

#Loading env variables
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY", None)
if api_key == None:
    raise RuntimeError("API Key not found in .env")

MAX_RETRIES = 20

#Model value to be passed to OpenRouter
model = "openrouter/free"

#initializing OpenAI Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

#Creating parser to validate and accept input when running main.py
# Now we can access `args.user_prompt`
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

def generate_completion(client,messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=available_functions,
    )
    return response


def main():
    print("Hello from ai-agent!")
    flag = False
    for tries in range(MAX_RETRIES):

        response = generate_completion(client,messages)
        if response.usage == None:
            raise RuntimeError("Failed API Request, please try again.")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        
        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(response.choices[0].message.content)
            flag = True
            break

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call,args.verbose)
            if not result_message['content']:
                raise Exception("Tool return empty content")
            
            if args.verbose:
                print(f"-> {result_message['content']}")
            
            messages.append(result_message)
    
    if not flag:
        print("Max retries exceeded, Agent was unable to find an answer")
        sys.exit(1)




if __name__ == "__main__":
    main()
