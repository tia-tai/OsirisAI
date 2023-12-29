import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def gpt_response_generator(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.conntent.strip()


gpt_response_generator("Hello, how are you?")
