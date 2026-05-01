from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
load_dotenv()

llm1=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

llm2=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)
model1=ChatHuggingFace(llm=llm1)
model2=ChatHuggingFace(llm=llm2)

prompt1=PromptTemplate(
    template="Write a short note of 100 words on the text {text}",
    input_variables=["text"]
)
prompt2=PromptTemplate(
    template="Generate a 5 question quiz on the text {text} with 4 optins for each ",
    input_variables=["text"]
)
prompt3=PromptTemplate(
    template="Combine the following report {report} and quiz {quiz} and give me final content.",
    input_variables=["report", "quiz"]
)

parser=StrOutputParser()

parallel_chain=RunnableParallel({
    'report':prompt1|model1|parser,
    'quiz':prompt2|model2|parser
})


merge_chain=prompt3|model1|parser

chain=parallel_chain|merge_chain

res=chain.invoke({
    "text":"Dinosaurs"
})

print(res)
chain.get_graph().print_ascii()