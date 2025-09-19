from dotenv import load_dotenv
import os
import openai
from openai import ChatCompletion


def load_openai_secret():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

def rungpt(
        model: str,
        content: str,
        user: str,
        temperature = 0.7,
        max_tokens=100
) -> ChatCompletion:
    if not openai.api_key:
        load_openai_secret()

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user",
             "content": content}
        ],
        user=user,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response
