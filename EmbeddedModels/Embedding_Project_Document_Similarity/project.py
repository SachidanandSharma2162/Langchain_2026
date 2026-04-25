from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


document=[
    "Delhi is the capital of India.",
    "Mumbai is the financial capital of India.",
    "Bangalore is the IT hub of India.",
    "Chennai is the cultural capital of India.",
    "Kolkata is city of joy."
]

query="Which city is the capital of India?"

query_embedding=embedding.embed_query(query)
document_embeddings=embedding.embed_documents(document)

similarities=cosine_similarity([query_embedding], document_embeddings)
index,score=similarities[0].argmax(),similarities[0].max()
print("Similarities:")
for i, similarity in enumerate(similarities[0]):
    print(f"Document {i+1}: {similarity}")


print(f"\nMost similar document: '{document[index]}' with similarity score: {score}")