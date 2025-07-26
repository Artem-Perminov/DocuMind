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


@cl.on_message
async def handle_message(message: cl.Message):
    user_question = message.content
    user_session_id = cl.user_session.get("id")
    thanks_action = cl.Action(
        label="❤",
        name="thanks_action",
        payload={"user_session_id": user_session_id},
        tooltip="Send thanks for the helpful reply",
    )
    msg = cl.Message(content="", actions=[thanks_action])
    async for chunk in final_chain.astream({"question": user_question}):
        await msg.stream_token(chunk)
    await msg.send()


@cl.action_callback("thanks_action")
async def on_action(action: cl.Action):
    print("message id:", action.forId, "action payload:", action.payload)
    await action.remove()
    await cl.Message(content="Thank you too!").send()
