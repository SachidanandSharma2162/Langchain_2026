from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnableLambda,RunnablePassthrough
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
    template="Give me joke on the topic {topic}",
    input_variables=["topic"]
)
def word_count(text):
    return len(text.split())

joke_chain=RunnableSequence(prompt1,model,parser)
parallel_chain=RunnableParallel({
    "joke":RunnablePassthrough(),
    "count":RunnableLambda(word_count)
})

final_chain=RunnableSequence(joke_chain,parallel_chain)
res=final_chain.invoke({
    "topic":"Sex"
})


print(res["joke"])
print(res['count'])

