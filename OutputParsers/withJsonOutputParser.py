from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from typing import TypedDict,Annotated, Optional,Literal
from pydantic import BaseModel,EmailStr, Field
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)
parser=JsonOutputParser()

template1=PromptTemplate(
   template = """
You MUST return ONLY valid JSON. No explanation, no markdown.

Topic: {topic}

{format_instruction}
""",
    input_variables=["topic"],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

# prompt=template1.format_prompt(topic="Virat Kohli's career.")

# res=model.invoke(prompt)
# print(res.content)

# parsed_op=parser.parse(res.content)
chain=template1|model|parser
parsed_op=chain.invoke({
    "topic": "write a 5 line poem on the topic Man is Struggle",
})
print(parsed_op["poem"])
print(type(parsed_op))