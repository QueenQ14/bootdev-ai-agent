import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from functions.call_function import available_functions
import json

#Loading env variables
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY", None)
if api_key == None:
    raise RuntimeError("API Key not found in .env")

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
        temperature=0,
        tools=available_functions,
    )
    return response


def main():
    print("Hello from ai-agent!")
    response = generate_completion(client,messages)
    if response.usage == None:
        raise RuntimeError("Failed API Request, please try again.")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)

    for tool_call in response.choices[0].message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")




if __name__ == "__main__":
    main()
