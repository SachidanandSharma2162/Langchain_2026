from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.prompts import PromptTemplate

# Load API key
load_dotenv()

# Initialize model
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)

# App title
st.header("Personal Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")

# Prompt template
template = PromptTemplate.from_template(
    "You are a helpful assistant.\n"
    "Chat History:\n{chat_history}\n"
    "User: {user_input}\n"
    "Assistant:"
)

# Run chatbot
if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Format chat history
    chat_history = "\n".join(
        [f'{m["role"]}: {m["content"]}' for m in st.session_state.messages]
    )

    # Create chain
    chain = template | model

    # Get response
    result = chain.invoke({
        "user_input": user_input,
        "chat_history": chat_history
    })

    response = result.content

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response)