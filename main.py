from openai import OpenAI

# Put your OpenRouter API key here
API_KEY = "<OPENROUTER_API_KEY>"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

print("AI Chat - Type 'quit' to exit")
print("-" * 30)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        break

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost:3000",  # Optional
            "X-Title": "AI Chat",  # Optional
        },
        extra_body={},
        model="deepseek/deepseek-r1-0528",
        messages=[{"role": "user", "content": user_input}],
    )

    print(f"AI: {completion.choices[0].message.content}")

print("Goodbye!")
