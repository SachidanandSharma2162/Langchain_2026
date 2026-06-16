import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

PDF_PATH = "islr.pdf"

# 1. Load PDF
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)
splits = splitter.split_documents(docs)

# 3. Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(
    documents=splits,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# 4. Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Answer ONLY from the provided context. "
        "If the answer is not present in the context, say 'I don't know'."
    ),
    (
        "human",
        "Question: {question}\n\nContext:\n{context}"
    )
])

# 5. Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Helper function
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 6. RAG Chain
parallel = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

chain = (
    parallel
    | prompt
    | llm
    | StrOutputParser()
)

# 7. Ask questions
print("PDF RAG ready. Ask a question (Ctrl+C to exit)")

while True:
    q = input("\nQ: ").strip()

    if q.lower() in ["exit", "quit"]:
        break

    answer = chain.invoke(q)

    print("\nA:", answer)