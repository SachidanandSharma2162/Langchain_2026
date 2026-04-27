from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# chat_template=ChatPromptTemplate([
#     SystemMessage(content='You are a helpful {domain} assistant.'),
#     HumanMessage(content='Explain {concept} in simple terms?')
# ])
chat_template=ChatPromptTemplate([
    ('system','You are a helpful {domain} assistant.'),
    ('human','Explain {concept} in simple terms?'),
])


prompt = chat_template.invoke({'domain':'cricket','concept':'Dusra'})

print(prompt)
# messages=[SystemMessage(content='You are a helpful {domain} assistant.', additional_kwargs={}, response_metadata={}), HumanMessage(content='Explain {concept} in simple terms?', additional_kwargs={}, response_metadata={})]