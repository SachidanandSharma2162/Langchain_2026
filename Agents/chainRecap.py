from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

parser=StrOutputParser()

model=ChatHuggingFace(llm=llm)

prompt=PromptTemplate(
    template="Tell me about {topic} in 10 points.",
    input_variables=["topic"]
)

chain=prompt|model|parser

response=chain.invoke({
    "topic":"RAG"
})


print(response)