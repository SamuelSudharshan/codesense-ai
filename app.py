import streamlit as st
import tempfile
import os
from backend import get_chunks, create_db, ask_question

st.set_page_config(page_title="CodeSense AI", page_icon="🚀", layout="wide")

st.markdown("""
<style>
body {background-color:#0f172a;}
.title {font-size:42px;font-weight:700;margin-bottom:0;}
.subtitle {color:#94a3b8;margin-bottom:20px;}

.chat-user {
    background:#1e293b;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
}

.chat-ai {
    background:#020617;
    padding:15px;
    border-radius:10px;
    border:1px solid #334155;
    margin-bottom:15px;
}

.sidebar-title {
    font-size:18px;
    font-weight:600;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚀 CodeSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered code understanding system</div>', unsafe_allow_html=True)

if "db" not in st.session_state:
    st.session_state.db = None
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("### ⚙️ Controls")

    mode = st.selectbox(
        "Query Mode",
        ["General", "Explain", "Improve"]
    )

    uploaded_files = st.file_uploader(
        "Upload Code Files",
        accept_multiple_files=True,
        type=["py", "js", "cpp"]
    )

    if st.button("🔄 Index Code"):
        if not uploaded_files:
            st.warning("Upload files first!")
        else:
            with st.spinner("Indexing..."):
                temp_dir = tempfile.mkdtemp()

                for file in uploaded_files:
                    path = os.path.join(temp_dir, file.name)
                    with open(path, "wb") as f:
                        f.write(file.read())

                chunks = get_chunks(temp_dir)
                st.session_state.db = create_db(chunks)

            st.success("Indexed!")

    if st.button("🗑 Clear Chat"):
        st.session_state.history = []

query = st.chat_input("Ask something about your code...")

if query:
    if st.session_state.db is None:
        st.warning("⚠️ Please index code first!")
    else:
        with st.spinner("Thinking..."):
            answer, docs = ask_question(st.session_state.db, query, mode)

        st.session_state.history.append((query, answer, docs))

for q, a, docs in st.session_state.history:
    st.markdown(f'<div class="chat-user">🧑 {q}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-ai">🤖 {a}</div>', unsafe_allow_html=True)

    with st.expander("📄 Retrieved Context"):
        for doc in docs:
            content = doc.page_content

            # Language detection
            if "def " in content:
                lang = "python"
            elif "function" in content:
                lang = "javascript"
            else:
                lang = "cpp"

            st.code(content, language=lang)

st.caption("⚡ Built with Ollama + FAISS + RAG")