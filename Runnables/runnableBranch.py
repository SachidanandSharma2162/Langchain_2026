from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
import os
from pydantic import BaseModel,Field
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnableLambda,RunnablePassthrough,RunnableBranch
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from typing import Literal
load_dotenv()
llm=HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text_generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)
class Email(BaseModel):
    emailType:Literal['complaint','refund','general_query']=Field(description="Classify the email in to any one of the category.")
model=ChatHuggingFace(llm=llm)
parser=StrOutputParser()
parser2 = PydanticOutputParser(pydantic_object=Email)

promptEmail=PromptTemplate(
    template="Classify the {email} as Complaint, General_Query or Refund \n {format_instruction}",
    input_variables=["email"],
    partial_variables={'format_instruction':parser2.get_format_instructions()}
)

promptComplaint=PromptTemplate(
    template="Generata a respose as a single statement for a complaint from user :{complaint}",
    input_variables=["complaint"]
)
promptRefund=PromptTemplate(
    template="Generata a respose as a single statement for a refund status from user :{refund_status}",
    input_variables=["refund_status"]
)
promptGeneralQuery=PromptTemplate(
    template="Generata a respose as a single statement for a general query from user :{general_query}",
    input_variables=["general_query"]
)

email_chain=promptEmail|model|parser2

branch_chain=RunnableBranch(
    (lambda x:x.emailType=='complaint',promptComplaint|model|parser),
    (lambda x:x.emailType=='refund',promptRefund|model|parser),
    (lambda x:x.emailType=='general_query',promptGeneralQuery|model|parser),
    RunnableLambda(lambda x: "Could not classify the feedback!")
)
email="""
Subject: Question regarding your Shipping Policy

Dear Shipment Team,

I was reviewing your Shipping Policy on your website and was hoping for some clarification. Specifically, I would like to know in how many days you ship an order.

Understanding this will help me decide on my upcoming purchase. I look forward to your response.

Best regards,
Rohit Singh
"""

final_chain=RunnableSequence(email_chain,branch_chain)

res=final_chain.invoke({
    "email":email
})

print(res)