from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough
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
    template="Give me 100 word summary about the topic {topic}",
    input_variables=['topic']
)
prompt2=PromptTemplate(
    template="Generate 5 quiz questions from the text{text}",
    input_variables=["text"]
)
summ_chain=RunnableSequence(prompt1,model,parser)
parallel_chain=RunnableParallel({
    "summary":RunnablePassthrough(),
    "quiz":RunnableSequence(prompt2,model,parser)
})
final_chain=RunnableSequence(summ_chain,parallel_chain)
res=final_chain.invoke({
    "topic":"Condom"
})
print(res["summary"])


final_chain.get_graph().print_ascii()
