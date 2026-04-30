from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from typing import TypedDict,Annotated, Optional,Literal
from pydantic import BaseModel,EmailStr, Field
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name: str=Field(description="Name of the Person.")
    age: int=Field(description="Age of the Person.")
    city:str=Field(description="City where the person belong to.")

parser=PydanticOutputParser(pydantic_object=Person)


template=PromptTemplate(
    template="give me details of a person from {country} in the folllowinf format \n {format_instruction}",
    input_variables=["country"],
    partial_variables={"format_instruction": parser.get_format_instructions()}
)

chain=template|model|parser

res=chain.invoke({"country": "India"})

print(res)