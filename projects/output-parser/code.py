import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(
    model="deepseek/deepseek-r1-0528:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0,
    # max_tokens=5000,
)


class Person(BaseModel):
    firstname: str = Field(description="fullname of hero")
    lastname: str = Field(description="fullname of hero")
    age: int = Field(description="age of hero")


messages = [
    ("system", "Handle the user query"),
    ("human", "Генрих Смит был восемнацдцателетним юношей, мечтающим уехать в город"),
]


prepared_llm = llm.with_structured_output(Person)
answer = prepared_llm.invoke(messages)
print(answer)
