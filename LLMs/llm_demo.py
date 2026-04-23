from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm=OpenAI(model='got-3.5-turbo-instruct')
res=llm.invoke("What is the capital of India?")
print(res)