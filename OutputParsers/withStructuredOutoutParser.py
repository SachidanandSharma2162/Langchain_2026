from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StructuredOutputParser, ResponseSchema
response_schemas = [
    ResponseSchema(name="title", description="Title of the report"),
    ResponseSchema(name="introduction", description="Introduction of GST"),
    ResponseSchema(name="key_features", description="Key features of GST"),
    ResponseSchema(name="importance", description="Importance of GST"),
    ResponseSchema(name="conclusion", description="Conclusion of the report"),
]

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)

parser = StructuredOutputParser.from_response_schemas(response_schemas)

template=PromptTemplate(
    template="Write a report on the topic {topic} \n {format_instruction}",
    input_variables=["topic"],
    partial_variables={"format_instruction": parser.get_format_instructions()}
)

chain=template|model|parser

res=chain.invoke({
    "topic":"GST"
})
# do not perform data validation which is one of the drawback of StructuredOutputParser
print(res)
