import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-r1-0528:free",
    messages=[{"role": "user", "content": "Tell us about AI agents in 1 sentence."}],
    # max_tokens=1000,
)

print(completion.choices[0].message.content)
