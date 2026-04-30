from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from typing import TypedDict,Annotated, Optional,Literal
from pydantic import BaseModel,EmailStr, Field
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)

template1=PromptTemplate(
    template="Write a report on the topic {topic}",
    input_variables=["topic"]
)

template2=PromptTemplate(
    template="Write a 5 point summary of the following text: {text}",
    input_variables=["text"]
)

chain =template1 | model | StrOutputParser() | template2 | model| StrOutputParser()
result1=chain.invoke({"topic": "importance of condom."})


print("Report: ",result1)