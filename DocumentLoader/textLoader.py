from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from langchain_community.document_loaders import TextLoader

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model=ChatHuggingFace(llm=llm)
parser=StrOutputParser()
prompt=PromptTemplate(
    template="Generate a title for the poem {poem}",
    input_variables=["poem"]
)
loader=TextLoader('cricket.txt',encoding='utf-8')

docs=loader.load()
# print(docs[0].page_content)

chain=prompt|model|parser

res=chain.invoke({
    "poem":docs[0].page_content
})

print(res)