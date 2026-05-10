from langchain.tools import BaseTool
from pydantic import BaseModel,Field
from typing import Type


class MultiplyInput(BaseModel):
    a: int = Field(required=True, description="The first number to add")
    b: int = Field(required=True, description="The second number to add")

class MultiplyTool(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"
    args_schema: Type[BaseModel] = MultiplyInput
    def _run(self, a: int, b: int) -> int:
        return a * b
# we can also create async version on the tool using BaseTool
# _run must be defined in BaseTool
multiply_tool=MultiplyTool()

res=multiply_tool.invoke({
    'a':3,
    'b':4
})

print(res)