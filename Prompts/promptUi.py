from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.prompts import PromptTemplate,load_prompt

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model = ChatHuggingFace(llm=llm)

st.header('Research Tool')

paper_input = st.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

# template = PromptTemplate.from_template(
#     "You are an expert research summarizer. "
#     "Summarize the paper titled '{paper_input}' in a {style_input} style. "
#     "Provide the explanation with {length_input}."
# )

# we can also create a template using prompt generator and save it as json file and load it here.
template=load_prompt('template.json')


# here are calling invoke method for both template and model saperately but we can also create a chain of template and model and call invoke method once for the chain.


# prompt=template.invoke({
#     'paper_input': paper_input,
#         'style_input': style_input,
#         'length_input': length_input
# })

# if st.button('Summarize'):
#     result=model.invoke(prompt)
#     st.write(result.content)

# chains
if st.button('Summarize'):
    chain = template | model
    result = chain.invoke({
        'paper_input': paper_input,
        'style_input': style_input,
        'length_input': length_input
    })
    st.write(result.content)