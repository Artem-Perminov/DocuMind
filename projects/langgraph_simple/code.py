import random
from typing import Literal
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)


# --------------------------------- State ---------------------------------------
class State(TypedDict):
    query: str
    resolver: str
    answer: str


# --------------------------------- Nodes ---------------------------------------
def choice_resolver(state: State) -> State:
    resolver = "support" if random.random() > 0.5 else "llm_node"
    print(random.random())
    state["resolver"] = resolver
    return state


def send_to_support(state: State) -> State:
    print(f"New message for Support: {state['query']}")
    return state


def llm_node(state: State) -> State:
    messages = [
        (
            "system",
            "You are a friendly chatbot. Your task is answer the question as short as possible",
        ),
        ("human", "{question}"),
    ]
    prompt = ChatPromptTemplate(messages)

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"question": state["query"]})
    state["answer"] = answer
    return state


def send_to_user(state: State) -> State:
    print(f"New message for User: {state['answer']}")
    return state


# --------------------------------- Edges ---------------------------------------
def route_by_resolver(state: State) -> Literal["send_to_support", "llm_node"]:
    if state["resolver"] == "support":
        return "send_to_support"
    else:
        return "llm_node"


# ---------------------------- Graph Building -----------------------------------
builder = StateGraph(State)
builder.add_node("choice_resolver", choice_resolver)
builder.add_node("send_to_support", send_to_support)
builder.add_node("llm_node", llm_node)
builder.add_node("send_to_user", send_to_user)

builder.add_edge(START, "choice_resolver")
builder.add_conditional_edges("choice_resolver", route_by_resolver)
builder.add_edge("send_to_support", END)
builder.add_edge("llm_node", "send_to_user")
builder.add_edge("send_to_user", END)

graph = builder.compile()


# ------------------------ Graph Visualization ---------------------------------
with open("graph.png", "wb") as f:
    f.write(graph.get_graph().draw_mermaid_png())


# ------------------------ Graph Invoke ---------------------------------
result = graph.invoke({"query": "Hi, my computer is not working!"})
print(result)
