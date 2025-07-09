import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-r1-0528:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)

messages = [
    (
        "system",
        "Ты эксперт в области {domain}. Твоя задача отвечать на вопросы пользователя как можно короче",
    ),
    MessagesPlaceholder("history"),
]
prompt_template = ChatPromptTemplate(messages)


def display_chat_history(history):
    """Display the entire chat history in a formatted way"""
    print("\n" + "=" * 50)
    print("CHAT HISTORY")
    print("=" * 50)

    for i, message in enumerate(history, 1):
        if isinstance(message, HumanMessage):
            print(f"[{i}] Пользователь: {message.content}")
        elif isinstance(message, AIMessage):
            print(f"[{i}] Умный кот: {message.content}")

    print("=" * 50 + "\n")


domain = input("Выбери интересующую тебя область: ")
history = []
while True:
    print()
    user_content = input("Пользователь: ")
    history.append(HumanMessage(content=user_content))
    prompt_value = prompt_template.invoke({"domain": domain, "history": history})
    full_ai_content = ""
    print("Умный кот: ", end="")
    for ai_message_chunk in llm.stream(prompt_value.to_messages()):
        print(ai_message_chunk.content, end="")
        full_ai_content += ai_message_chunk.content
    history.append(AIMessage(content=full_ai_content))
    print()

    # Ask if user wants to see chat history
    show_history = input("Показать историю чата? (да / нет): ").lower()
    if show_history == "да":
        display_chat_history(history)
