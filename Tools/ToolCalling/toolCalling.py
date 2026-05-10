from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""

    return a * b


# Groq model
llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

# Bind tools
llm_with_tools = llm.bind_tools([
    multiply
])

# Ask question
response = llm_with_tools.invoke(
    "Can you multiply 12 with 4?"
)

print(response)

print("\nTool Calls:")
print(response.tool_calls)