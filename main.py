import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

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
    {"role": "user", "content": args.user_prompt},
]

def generate_completion(client,messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
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




if __name__ == "__main__":
    main()
