import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import chainlit as cl
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="tngtech/deepseek-r1t2-chimera:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)

messages = [
    (
        "system",
        "You are an expert in LangChain. Your task is answer the question as short as possible",
    ),
    ("human", "{question}"),
]
prompt = ChatPromptTemplate(messages)

final_chain = prompt | llm | StrOutputParser()


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="LangChain Helper",
            icon="https://ucarecdn.com/f621c671-b27b-48cf-8b95-8f6136963541/-/scale_crop/180x180/center/",
            markdown_description="Разработка MVP AI-сервиса на Python: от идеи до релиза",
            starters=[
                cl.Starter(
                    label="What is a LangChain?",
                    message="What is a LangChain?",
                    icon="/public/chain.svg",
                ),
                cl.Starter(
                    label="Why is the parrot a mascot?",
                    message="Why is the parrot a mascot?",
                    icon="/public/parrot.svg",
                ),
            ],
        )
    ]


@cl.on_message
async def handle_message(message: cl.Message):
    user_question = message.content
    msg = cl.Message(content="")
    async for chunk in final_chain.astream({"question": user_question}):
        await msg.stream_token(chunk)
    await msg.send()
