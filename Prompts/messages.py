from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)


messages=[
    SystemMessage(content="You are a good Assistant"),
    HumanMessage(content="What is the capital of India?"),
]

response=model.invoke(messages)
messages.append(AIMessage(content=response.content))
print(response.content)

print(messages)