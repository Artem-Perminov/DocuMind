from langchain import hub
import time
import datetime
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain.agents import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import AgentExecutor, create_react_agent

load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)


@tool(name_or_callable="current-year-tool")
def get_this_year_tool() -> int:
    """Get the current year"""
    time.sleep(1)
    return datetime.datetime.now().year


class WikiInputs(BaseModel):
    """Inputs to the wikipedia tool."""

    query: str = Field(description="query to look up in Wikipedia")


wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="ru"))
wikipedia_tool = Tool(
    name="wikipedia-tool",
    description="Look up things in Wikipedia",
    args_schema=WikiInputs,
    func=wikipedia.run,
)

TOOLS = [wikipedia_tool, get_this_year_tool]

prompt = hub.pull("sanchezzz/russian_react_chat")

agent = create_react_agent(llm, TOOLS, prompt, stop_sequence=False)
agent_executor = AgentExecutor(
    agent=agent, tools=TOOLS, verbose=True, handle_parsing_errors=True
)

result = agent_executor.invoke(
    {
        "input": "Сколько лет прошло с появления передачи Поле чудес в эфире? Кто её ведущий сегодня?",
        "chat_history": [],
    }
)
print(result)
