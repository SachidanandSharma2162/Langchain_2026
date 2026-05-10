from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

# Tool Creation
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""

    return a * b


# Groq model
llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

# Tool Binding
llm_with_tools = llm.bind_tools([
    multiply
])

# Tool Calling
response = llm_with_tools.invoke(
    "Can you multiply 12 with 4?"
)

# Tool Execution
res=multiply.invoke(response.tool_calls[0]) # returns a Tool Message
res=multiply.invoke(response.tool_calls[0]['args']) # returns a result

# Tool Message is a message which you get when you execute a tool with the help of a tool call.
print(res)