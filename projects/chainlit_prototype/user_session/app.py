import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import chainlit as cl
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
    BaseChatMessageHistory,
)
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

llm = ChatOpenAI(
    model="tngtech/deepseek-r1t2-chimera:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)

DOMAIN = "biology"
store = {}


def get_history_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


messages = [
    (
        "system",
        "You are an expert in {domain}. Your task is answer the question as short as possible",
    ),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
]
prompt = ChatPromptTemplate(messages)

final_chain = (
    RunnableWithMessageHistory(
        prompt | llm,
        get_history_by_session_id,
        input_messages_key="question",
        history_messages_key="history",
    )
    | StrOutputParser()
)


@cl.on_message
async def handle_message(message: cl.Message):
    user_session_id = cl.user_session.get("id")
    user_question = message.content
    msg = cl.Message(content="")
    print(user_session_id)
    print(store)
    async for chunk in final_chain.astream(
        {"domain": DOMAIN, "question": user_question, "history": messages},
        config=RunnableConfig(configurable={"session_id": user_session_id}),
    ):
        await msg.stream_token(chunk)
    await msg.send()
