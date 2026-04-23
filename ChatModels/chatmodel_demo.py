from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

chatModel=ChatOpenAI(model='gpt-4')

res=chatModel.invoke("What is the capital of India?")

print(res)