import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Create a .env file for your OpenAI API key
client = openai.OpenAI(api_key=os.getenv("API_KEY"))


# Openai GPT-3.5-Turbo Response Generator
def gpt_response_generator(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
