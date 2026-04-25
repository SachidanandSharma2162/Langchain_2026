from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings=OpenAIEmbeddings(model='text-embedding-3-large',dimensions=32)
document=[
    "Delhi is the capital of India.",
    "Mumbai is the financial capital of India.",
    "Bangalore is the IT hub of India.",
    "Chennai is the cultural capital of India."
]
res=embeddings.embed_documents(document)

print(str(res))