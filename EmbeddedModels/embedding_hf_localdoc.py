from langchain_huggingface import HuggingFaceEmbeddings

embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

document=[
    "Delhi is the capital of India.",
    "Mumbai is the financial capital of India.",
    "Bangalore is the IT hub of India.",
    "Chennai is the cultural capital of India."
]
res=embedding.embed_documents(document)

print(str(res))