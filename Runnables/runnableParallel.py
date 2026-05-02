from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os
from langchain_core.runnables import RunnableSequence,RunnableParallel
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

model=ChatHuggingFace(llm=llm)
parser=StrOutputParser()

prompt1=PromptTemplate(
    template="Give me 100 word summary about the paper {paper}",
    input_variables=['paper']
)
prompt2=PromptTemplate(
    template="Generate 5 quiz questions from the text{text}",
    input_variables=["text"]
)

parallel_chain=RunnableParallel({
    'summary':RunnableSequence(prompt1, model,parser),
    'quiz':RunnableSequence(prompt2, model,parser)
})

res=parallel_chain.invoke({
    "paper":"Diffusion Models Beat GANs on Image Synthesis",
    'text':"Attention is all you need."
})

print(res['summary'])
print(res['quiz'])

parallel_chain.get_graph().print_ascii()