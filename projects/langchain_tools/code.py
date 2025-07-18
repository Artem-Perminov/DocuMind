import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import time
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from pydantic import Field

# import json

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
}


@tool
def get_order_status(order_id: str = Field(description="Identifier of order")) -> str:
    """Get status of order by order identifier"""
    return ORDERS_STATUSES_DATA.get(
        order_id, f"Не существует заказа с order_id={order_id}"
    )


# print("Name:", get_order_status.name)
# print("Description:", get_order_status.description)
# print("Arguments:", get_order_status.args)
# print(json.dumps(get_order_status.args_schema.model_json_schema(), indent=4))
# print("Result:", get_order_status.invoke({"order_id": "a42"}))


llm_with_tools = llm.bind_tools([get_order_status])

messages = [HumanMessage(content="What about my order b61?")]

# print(messages)

ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)

# print(ai_message.content) - ''

# print("Name:", ai_message.tool_calls)

for tool_call in ai_message.tool_calls:
    # print(tool_call["name"])
    # print(tool_call)
    if tool_call["name"] == get_order_status.name:
        tool_message = get_order_status.invoke(tool_call)
        messages.append(tool_message)

# print(messages)

time.sleep(2)
ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)

print(ai_message.content)
# print(messages)
