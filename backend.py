from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from utils import load_code

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

llm = Ollama(model="llama3")

def get_chunks(folder="data"):
    text = load_code(folder)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    return splitter.split_text(text)


from langchain_community.vectorstores import FAISS

def create_db(chunks):
    if not chunks:
        raise ValueError("No code files found in /data folder")
    return FAISS.from_texts(chunks, embeddings)

    for i, vec in enumerate(vectors):
        client.insert(
            id=str(i),
            vector=vec,
            metadata={"text": chunks[i]}
        )

    return client


def retrieve_from_db(query, db):
    docs = db.similarity_search(query, k=3)
    return docs

def generate_answer(query, context):

    if "improve" in query:
        prompt = f"Analyze this code and suggest improvements:\n{context}\n\nQuestion: {query}"

    elif "explain" in query:
        prompt = f"Explain this code clearly:\n{context}\n\nQuestion: {query}"

    else:
        prompt = f"Answer based on this code:\n{context}\n\nQuestion: {query}"

    return llm.invoke(prompt)



def ask_question(db, query, mode):
    docs = retrieve_from_db(query, db)
    context = " ".join([doc.page_content for doc in docs])
    answer = generate_answer(query, context)
    return answer, docs