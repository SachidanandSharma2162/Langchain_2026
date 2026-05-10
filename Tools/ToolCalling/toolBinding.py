from langchain_core.tools import tool
import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

load_dotenv()

@tool
def multiply_tool(a:int,b:int)->int:
    """This tool return product of a and b"""

    return a*b

multiply=multiply_tool.invoke({
    'a':3,
    'b':8
})

print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)


llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv('HUGGINGFACEHUB_API_TOKEN')
)

model = ChatHuggingFace(llm=llm)

llm_with_tools=model.bind_tools([multiply_tool])

response=llm_with_tools.invoke("what is 12 multiplied by 4")

print(response)