from dotenv import load_dotenv
from langchain_core.tools import InjectedToolArg, tool
from langchain_groq import ChatGroq
import requests
from typing import Annotated
from langchain_core.messages import HumanMessage,AIMessage
import json

load_dotenv()

# Tool Creation
@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
  """
  This function fetches the currency conversion factor between a given base currency and a target currency
  """
  url = f'https://v6.exchangerate-api.com/v6/c754eab14ffab33112e380ca/pair/{base_currency}/{target_currency}'

  response = requests.get(url)

  return response.json()

@tool
def convert(
    base_currency_value: int,
    conversion_rate: Annotated[
        float,
        InjectedToolArg
    ]
) -> float:
    """
    Convert currency value using conversion factor
    """

    return base_currency_value * conversion_rate

# If a parameter is set to InjectedToolArg then LLM 
# do not set its value at tool calling, you can set
# it by your means, so its value will be Injection 
# from previous tool calls.

# Groq model
llm = ChatGroq(
    model="llama-3.1-8b-instant"
)

# message queue
message=[]

llm_with_tools = llm.bind_tools([
    get_conversion_factor,
    convert
])

message.append(HumanMessage('What is the conversion factor between INR and USD, and based on that can you convert 10 inr to usd'))

response = llm_with_tools.invoke(
    message
)

tool_call = response.tool_calls[0]

# TOOL 1
tool_message1 = get_conversion_factor.invoke(tool_call)
message.append(tool_message1)
conversion_rate = json.loads(tool_message1.content)["conversion_rate"]

# TOOL 2 (manual chaining)
tool_message2 = convert.invoke({
    "base_currency_value": 34,
    "conversion_rate": conversion_rate
})
message.append(tool_message2)
print(message)