import os
import time
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)


ORDERS_STATUSES_DATA = {
    "a42": "Доставляется",
    "b61": "Выполнен",
    "k37": "Отменен",
    "k55": "Доставляется",
}


@tool
def get_order_status(order_id: str) -> str:
    """Get status of order by order identifier"""
    time.sleep(2)
    return ORDERS_STATUSES_DATA.get(
        order_id, f"Не существует заказа с order_id={order_id}"
    )


@tool
def cancel_order(order_id: str) -> str:
    """Cancel the order by order identifier"""
    time.sleep(2)
    if order_id not in ORDERS_STATUSES_DATA:
        return f"Такой заказ не существует"
    if ORDERS_STATUSES_DATA[order_id] != "Отменен":
        ORDERS_STATUSES_DATA[order_id] = "Отменен"
        return "Заказ успешно отменен"
    return "Заказ уже отменен"


tools = [get_order_status, cancel_order]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "Твоя задача отвечать на вопросы клиентов об их заказах, используя вызов инструментов."
                "Отвечай пользователю в реперском стиле."
            ),
        ),
        MessagesPlaceholder("chat_history"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)


agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

memory = InMemoryChatMessageHistory()
agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="output",
)

config = {"configurable": {"session_id": "test-session"}}
while True:
    print()
    user_question = input("Ты: ")
    answer = agent_with_history.invoke({"input": user_question}, config)
    print("Кот: ", answer["output"])
