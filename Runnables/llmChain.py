from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os


load_dotenv()
llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model=ChatHuggingFace(llm=llm)
prompt=PromptTemplate(
    template="Write a 6 line poem on the topic {topic}.",
    input_variables=["topic"],
)

user_inp=input("Enter the topic for poem... \n")

chain=prompt|model
invoked=chain.invoke({
    "topic":user_inp
})

print(invoked.content)