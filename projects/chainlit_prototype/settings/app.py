import chainlit as cl
from chainlit.input_widget import Select, Slider, TextInput
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


@cl.on_chat_start
async def start():
    settings = cl.ChatSettings(
        [
            Select(
                id="model",
                label="Model",
                values=[
                    "tngtech/deepseek-r1t2-chimera:free",
                    "deepseek/deepseek-r1-0528:free",
                ],
                initial_index=0,
            ),
            TextInput(
                id="token",
                label="API Token",
                initial="",
                placeholder="Type token here",
                multiline=False,
            ),
            Slider(
                id="temperature",
                label="Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    )
    await settings.send()


@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("model", settings["model"])
    cl.user_session.set("token", settings["token"])
    cl.user_session.set("temperature", settings["temperature"])


@cl.on_message
async def handle_message(message: cl.Message):
    model = cl.user_session.get("model")
    token = cl.user_session.get("token")
    temperature = cl.user_session.get("temperature")
    messages = [
        (
            "system",
            "You are an expert in LangChain. Your task is answer the question as short as possible",
        ),
        ("human", "{question}"),
    ]
    prompt = ChatPromptTemplate(messages)

    llm = ChatOpenAI(
        model=model,
        base_url="https://openrouter.ai/api/v1",
        api_key=token,
        temperature=temperature,
    )

    final_chain = prompt | llm | StrOutputParser()

    user_question = message.content
    msg = cl.Message(content="")
    async for chunk in final_chain.astream({"question": user_question}):
        await msg.stream_token(chunk)
    await msg.send()
