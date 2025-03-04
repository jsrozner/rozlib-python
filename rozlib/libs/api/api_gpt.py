from dotenv import load_dotenv
import os
import openai

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
):
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

    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo-0125",
    #     messages=[
    #         # {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": prompt}
    #     ],
    #     max_tokens=20,             # Maximum number of tokens to generate in the
    #     # completion
    #     temperature=0.8,            # Sampling temperature to control
    #     seed=1,                     # potentially should be deterministic?
    #     # randomness (range: 0 to 2)
    #     # top_p=0.95,                 # Nucleus sampling (alternative to temperature, values between 0 and 1)
    #     n=1,                        # Number of completions to generate for
    #     # each input
    #     # stop=None,                  # A sequence of tokens that will stop the model from further generating
    #     # presence_penalty=0.0,        # Penalizes repeated tokens in completion (range: -2.0 to 2.0)
    #     # frequency_penalty=0.0,       # Penalizes repeated tokens across completions (range: -2.0 to 2.0)
    #     # logit_bias={},               # Modify the likelihood of specific tokens appearing
    #     # user="user-identifier"       # Unique identifier for tracking API usage by user (useful for multi-user systems)
    # )
    # return response
