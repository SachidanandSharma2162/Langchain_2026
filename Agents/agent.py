from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_core.tools import tool
import requests
from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
load_dotenv()

@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a specified city. 
    Use this whenever you need to know the temperature or conditions of a location.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        condition = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"In {city}, the weather is currently {condition} with a temperature of {temp}°C."
    
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)
chat_model=ChatHuggingFace(llm=llm)

tools=[get_weather]
 
prompt=ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    # This is the line that solves your ValueError:
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]
)

agent = create_tool_calling_agent(chat_model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "Find the capital of Uttar Pradesh, and then find the current weather condition for that city."})

print(response)