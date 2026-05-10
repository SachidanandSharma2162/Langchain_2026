from langchain.tools import tool

# defining tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    
    return a * b

# defining the class
class MathToolkit:
    
    def get_tools(self):
        return [
            add,
            multiply
        ]
    
# accessing tools
toolkit = MathToolkit()
tools = toolkit.get_tools()

# using tools in toolkit
add_tool=tools[0]
res=add_tool.invoke({
    'a':3,
    'b':4
})
print(res)