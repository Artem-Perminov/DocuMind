import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import trim_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-r1-0528:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)

DEFAULT_SESSION_ID = "default"
chat_history = InMemoryChatMessageHistory()


messages = [
    (
        "system",
        "Ты эксперт в области {domain}. Твоя задача отвечать на вопросы пользователя как можно короче",
    ),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
]
prompt = ChatPromptTemplate(messages)

trimmer = trim_messages(
    strategy="last",
    token_counter=len,
    max_tokens=10,
    start_on="human",
    end_on="human",
    include_system=True,
    allow_partial=False,
)

chain = prompt | trimmer | llm
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: chat_history,
    input_messages_key="question",
    history_messages_key="history",
)
final_chain = chain_with_history | StrOutputParser()


domain = input("Choice domain area: ")
while True:
    print()
    user_question = input("You: ")
    print("Bot: ", end="")
    for answer_chunk in final_chain.stream(
        {"domain": domain, "question": user_question},
        config={"configurable": {"session_id": DEFAULT_SESSION_ID}},
    ):
        print(answer_chunk, end="")
    print()
