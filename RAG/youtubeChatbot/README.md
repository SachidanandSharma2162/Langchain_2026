▶ YTCHAT — YouTube Video Chatbot
Chat with any YouTube video using AI. Paste a video ID or URL, and ask questions about the transcript — powered by Groq LLMs, HuggingFace Embeddings, and FAISS vector search.

🚀 Features

🎬 Supports any YouTube video with captions (English, Hindi, and more)
🔍 RAG pipeline — retrieves relevant transcript chunks before answering
⚡ Groq-powered LLMs (free, fast, no credit card needed)
🧠 4 model choices — Llama 3.1 8B, Llama 3.3 70B, Gemma 2 9B, Mixtral 8x7B
🖤 Clean dark UI built with Streamlit


🛠️ Tech Stack
LayerToolUIStreamlitTranscriptyoutube-transcript-apiText SplittingLangChain RecursiveCharacterTextSplitterEmbeddingsHuggingFace sentence-transformersVector StoreFAISSLLMGroq API (Llama / Gemma / Mixtral)

📦 Installation
1. Clone the repo
bash git clone https://github.com/SachidanandSharma2162/Langchain_2026/tree/main/RAG/youtubeChatbot
cd yt-chatbot
2. Install dependencies
bash pip install -r requirements.txt
3. Get a free Groq API key
Sign up at → console.groq.com/keys
No credit card required. Takes 30 seconds.
4. Set your API key (optional)
You can paste the key in the app UI, or set it as an environment variable so it auto-fills:
Mac / Linux:
bashexport GROQ_API_KEY=gsk_your_key_here
Windows (CMD):
cmdset GROQ_API_KEY=gsk_your_key_here
Or use a .env file:
GROQ_API_KEY=gsk_your_key_here
Then add to the top of youtube_chatbot.py:
pythonfrom dotenv import load_dotenv
load_dotenv()
5. Run the app
bash streamlit run youtube_chatbot.py

📁 Project Structure
yt-chatbot/
│
├── youtube_chatbot.py   # Main Streamlit app
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md

🧭 How It Works
YouTube Video ID
      │
      ▼
Fetch Transcript (youtube-transcript-api)
      │
      ▼
Split into Chunks (LangChain RecursiveCharacterTextSplitter)
      │
      ▼
Embed Chunks (HuggingFace sentence-transformers)
      │
      ▼
Store in FAISS Vector Index
      │
      ▼
User asks a Question
      │
      ▼
Retrieve Top-4 Relevant Chunks (similarity search)
      │
      ▼
Send Context + Question → Groq LLM
      │
      ▼
Display Answer in Chat UI

💬 Usage

Open the app in your browser (http://localhost:8501)
Paste a YouTube video ID (e.g. yKTEC1Y5bEQ) or full URL
Select a model
Enter your Groq API key
Click Load Video →
Start chatting about the video!


⚠️ Notes

The video must have captions enabled. Auto-generated captions work too.
HuggingFace Inference API is used only for embeddings (free, no key needed for default model).
All 4 Groq models are on the free tier with generous rate limits.
Your API key is stored only in the Streamlit session — never saved to disk.
