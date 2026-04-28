from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

chat_template=ChatPromptTemplate.from_messages([
    ("system","You are a helpful agent."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}")
])

chat_history=[]

with open("chat_history.txt") as f:
    chat_history.extend(f.readlines())

print(chat_history)

prompt = chat_template.invoke({'chat_history':chat_history, 'input':'Where is my refund'})

print(prompt)