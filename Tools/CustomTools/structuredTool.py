from langchain_community.tools import StructuredTool
from pydantic import BaseModel,Field

class MultiplyInput(BaseModel):
    a: int=Field(description="The first number")
    b: int=Field(description="The second number")


def muntiply_num(a:int,b:int)->int:
    return a*b

multiply_tool=StructuredTool(
    func=muntiply_num,
    name="Multiply",
    description="Multiply two numbers.",
    args_schema=MultiplyInput
)

Result=multiply_tool.invoke({
    'a':3,
    'b':4
})

print(Result)