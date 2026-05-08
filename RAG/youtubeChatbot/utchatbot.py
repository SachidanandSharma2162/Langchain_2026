import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq
import os
import re

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YT Chatbot",
    page_icon="▶️",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

:root {
    --bg:      #0d0d0d;
    --surface: #161616;
    --border:  #2a2a2a;
    --accent:  #ff3c3c;
    --text:    #f0f0f0;
    --muted:   #666;
    --user-bg: #1e1e1e;
    --bot-bg:  #1a1010;
}
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
h1,h2,h3 { font-family: 'Space Mono', monospace; }

input, textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
input:focus, textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(255,60,60,0.15) !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover { opacity:0.85 !important; transform:translateY(-1px) !important; }

/* selectbox */
[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Chat bubbles */
.msg-wrapper { display:flex; gap:12px; margin-bottom:18px; align-items:flex-start; }
.msg-wrapper.user { flex-direction:row-reverse; }
.avatar {
    width:36px; height:36px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-family:'Space Mono',monospace; font-size:0.75rem; flex-shrink:0;
}
.avatar.bot  { background:var(--accent); color:#fff; }
.avatar.user { background:#333; color:var(--text); }
.bubble {
    max-width:78%; padding:12px 16px; border-radius:12px;
    font-size:0.95rem; line-height:1.6;
}
.bubble.bot  { background:var(--bot-bg);  border:1px solid #2a1515; border-top-left-radius:2px; }
.bubble.user { background:var(--user-bg); border:1px solid var(--border); border-top-right-radius:2px; }

.video-card {
    background:var(--surface); border:1px solid var(--border);
    border-left:3px solid var(--accent);
    border-radius:10px; padding:16px 20px; margin-bottom:24px;
}
.video-card .vid-id {
    font-family:'Space Mono',monospace; font-size:0.75rem;
    color:var(--accent); letter-spacing:0.05em; margin-bottom:4px;
}
.video-card .vid-title { font-size:1rem; font-weight:600; }

.hero { text-align:center; padding:3rem 0 2rem; }
.hero .logo { font-family:'Space Mono',monospace; font-size:2.6rem; font-weight:700; }
.hero .logo span { color:var(--accent); }
.hero .sub { color:var(--muted); font-size:0.95rem; margin-top:8px; }

.step-label {
    font-family:'Space Mono',monospace; font-size:0.7rem;
    color:var(--muted); letter-spacing:0.1em; text-transform:uppercase; margin-bottom:6px;
}
.info-box {
    background:#111a11; border:1px solid #1a3a1a; border-radius:8px;
    padding:12px 16px; font-size:0.82rem; color:#7fb87f; margin-bottom:16px;
    line-height:1.6;
}
.info-box a { color:#a0d4a0; }

.stSpinner > div { border-top-color: var(--accent) !important; }
hr { border-color: var(--border) !important; }
[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
.chat-container { max-height:60vh; overflow-y:auto; padding-right:4px; }
</style>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────

GROQ_MODELS = {
    "Llama 3.1 8B  (fast, free)":    "llama-3.1-8b-instant",
    "Llama 3.3 70B (smart, free)":   "llama-3.3-70b-versatile",
    "Gemma 2 9B  (free)":            "gemma2-9b-it",
    "Mixtral 8x7B  (free)":          "mixtral-8x7b-32768",
}

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about a YouTube video.
Answer ONLY from the provided transcript context.
If the context is insufficient, say "I don't have enough information from the video to answer that."
Be concise and clear."""


# ── Helpers ────────────────────────────────────────────────────────────────────

def extract_video_id(raw: str) -> str:
    raw = raw.strip()
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})", raw)
    if m:
        return m.group(1)
    if re.match(r"^[A-Za-z0-9_-]{11}$", raw):
        return raw
    return raw


@st.cache_resource(show_spinner=False)
def build_retriever(video_id: str):
    """Fetch transcript → chunk → embed → FAISS. Cached per video_id."""
    api = YouTubeTranscriptApi()
    transcript = None
    for lang in (["en"], ["hi"], None):
        try:
            tl = api.fetch(video_id, languages=lang) if lang else api.fetch(video_id)
            transcript = " ".join(chunk.text for chunk in tl)
            break
        except Exception:
            continue
    if not transcript:
        raise ValueError("No transcript found for this video.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])
    embeddings = HuggingFaceEmbeddings()
    vs = FAISS.from_documents(chunks, embeddings)
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    return retriever, len(chunks)


def ask(question: str, retriever, groq_key: str, model_id: str) -> str:
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)

    client = Groq(api_key=groq_key)
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        max_tokens=512,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [
    ("page", "home"),
    ("video_id", ""),
    ("messages", []),
    ("retriever", None),
    ("groq_key", ""),
    ("model_id", list(GROQ_MODELS.values())[0]),
    ("n_chunks", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Home
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
        <div class="logo">▶ <span>YT</span>CHAT</div>
        <div class="sub">Paste a YouTube video ID or URL and chat with the transcript.</div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:

        st.markdown("""
        <div class="info-box">
            🔑 This app uses <strong>Groq's free API</strong> — all models below are completely free.<br>
            Get your key in 30 seconds at
            <a href="https://console.groq.com/keys" target="_blank">console.groq.com/keys</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="step-label">Video ID or URL</div>', unsafe_allow_html=True)
        raw_input = st.text_input(
            label="",
            placeholder="e.g.  yKTEC1Y5bEQ  or  https://youtu.be/yKTEC1Y5bEQ",
            label_visibility="collapsed",
        )

        st.markdown('<div class="step-label" style="margin-top:12px;">Model</div>', unsafe_allow_html=True)
        model_label = st.selectbox("", options=list(GROQ_MODELS.keys()), label_visibility="collapsed")

        groq_key_input = st.text_input(
            label="Groq API Key",
            placeholder="gsk_••••••••••••••••",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Free at https://console.groq.com/keys — no credit card needed",
        )

        go = st.button("Load Video →", use_container_width=True)

    if go:
        if not raw_input.strip():
            st.error("Please enter a video ID or URL.")
        elif not groq_key_input.strip():
            st.error("Please enter your Groq API key.")
        else:
            vid = extract_video_id(raw_input)
            with st.spinner("Fetching transcript & building vector index…"):
                try:
                    retriever, n = build_retriever(vid)
                    st.session_state.video_id = vid
                    st.session_state.retriever = retriever
                    st.session_state.groq_key  = groq_key_input.strip()
                    st.session_state.model_id  = GROQ_MODELS[model_label]
                    st.session_state.n_chunks  = n
                    st.session_state.messages  = []
                    st.session_state.page      = "chat"
                    st.rerun()
                except TranscriptsDisabled:
                    st.error("❌ Captions are disabled for this video.")
                except ValueError as e:
                    st.error(f"❌ {e}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")

    st.markdown("""
    <div style='text-align:center;margin-top:2rem;font-family:Space Mono,monospace;
                font-size:0.65rem;color:#2a2a2a;'>
        LangChain · HuggingFace Embeddings · FAISS · Groq
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Chat
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "chat":

    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown(f"""
        <div class="video-card">
            <div class="vid-id">VIDEO ID · {st.session_state.n_chunks} chunks indexed</div>
            <div class="vid-title">{st.session_state.video_id}</div>
        </div>
        """, unsafe_allow_html=True)
    with top_r:
        if st.button("← New Video", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.messages = []
            st.rerun()

    # Render chat history
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.messages:
        role    = msg["role"]
        content = msg["content"].replace("\n", "<br>")
        a_lbl   = "YT" if role == "assistant" else "U"
        a_cls   = "bot" if role == "assistant" else "user"
        b_cls   = "bot" if role == "assistant" else "user"
        w_cls   = "user" if role == "user" else ""
        chat_html += f"""
        <div class="msg-wrapper {w_cls}">
            <div class="avatar {a_cls}">{a_lbl}</div>
            <div class="bubble {b_cls}">{content}</div>
        </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    question = st.chat_input("Ask anything about this video…")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking…"):
            try:
                answer = ask(
                    question,
                    st.session_state.retriever,
                    st.session_state.groq_key,
                    st.session_state.model_id,
                )
            except Exception as e:
                answer = f"⚠️ Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center;color:#444;padding:2rem 0;font-size:0.9rem;">
            Ask your first question about the video above ↑
        </div>
        """, unsafe_allow_html=True)
