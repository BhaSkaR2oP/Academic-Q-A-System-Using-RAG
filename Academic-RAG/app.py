import streamlit as st
import os
import time
import requests
from dotenv import load_dotenv
from pinecone import Pinecone
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Academic RAG Explorer",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- LOAD SECRETS ---
load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = "jina-embeddings-v5-text-small"

# --- CUSTOM CSS FOR MODERN UI ---
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px #3b82f6;
    }
    .stButton>button {
        border-radius: 12px;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
    }
    .chat-bubble {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }
    .source-box {
        background: #f1f5f9;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-top: 8px;
        font-size: 0.9em;
    }
    h1 {
        color: #0f172a;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SERVICES ---
@st.cache_resource
def init_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index("academic-rag")

@st.cache_resource
def init_gemini():
    return genai.Client(api_key=GEMINI_API_KEY)

index = init_pinecone()
gemini_client = init_gemini()

# --- RAG FUNCTIONS ---
def get_query_embedding(question):
    response = requests.post(
        "https://api.jina.ai/v1/embeddings",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {JINA_API_KEY}"
        },
        json={
            "model": EMBEDDING_MODEL,
            "input": [question],
            "normalized": True
        }
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

def retrieve_chunks(question, top_k=15):
    query_vector = get_query_embedding(question)
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    retrieved_chunks = []
    for match in results["matches"]:
        retrieved_chunks.append({
            "text": match["metadata"]["text"],
            "page": match["metadata"].get("page", "Unknown"),
            "score": match["score"]
        })
    return retrieved_chunks

def choose_top_k(question):
    question_lower = question.lower()
    broad_keywords = ["complete", "entire", "all topics", "all units", "full syllabus", "complete syllabus", "whole document", "everything", "overview"]
    conceptual_keywords = ["explain", "difference", "compare", "how does", "why", "describe", "discuss"]
    
    if any(keyword in question_lower for keyword in broad_keywords):
        return 50
    if any(keyword in question_lower for keyword in conceptual_keywords):
        return 10
    return 5

def smart_retrieve(question):
    top_k = choose_top_k(question)
    return retrieve_chunks(question, top_k=top_k)

def generate_answer(question, retrieved_chunks):
    context = ""
    for i, chunk in enumerate(retrieved_chunks):
        context += f"\n--- Context {i + 1} ---\nPage: {chunk['page']}\n{chunk['text']}\n"

    prompt = f"""
You are an academic syllabus question-answering assistant.

Use ONLY the information explicitly present in the provided context.

For syllabus questions:
- Do not infer or guess missing units.
- Do not use general knowledge.
- Do not derive topics from lab exercises, course outcomes, or related subjects unless they are explicitly listed as syllabus topics.
- If a unit is not present in the retrieved context, clearly state that the unit could not be found.
- Never invent missing syllabus content.

For a request for the COMPLETE syllabus:
- Include every unit that is explicitly present in the context.
- Preserve the unit numbers and topic structure.
- Do not claim that the syllabus is complete if one or more requested units are missing.

If the requested information cannot be found, say:
"I couldn't find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                raise

# --- UI HEADER ---
st.markdown("<h1>📚 Academic RAG Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 1.1em;'>Ask questions about your uploaded academic documents (e.g., Operating Systems Notes).</p>", unsafe_allow_html=True)
st.divider()

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble' style='background: #e0f2fe; border-color: #bae6fd;'><strong>🧑‍🎓 You:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble'><strong>🤖 AI Assistant:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
        with st.expander("View Retrieved Sources"):
            for idx, chunk in enumerate(msg.get("chunks", [])[:1]):
                st.markdown(f"<div class='source-box'><strong>Page {chunk['page']}:</strong> {chunk['text']}</div>", unsafe_allow_html=True)

# User input
if question := st.chat_input("Ask a question about your syllabus..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

# Process new question
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    question = st.session_state.messages[-1]["content"]
    
    with st.spinner("Searching documents & generating answer..."):
        try:
            chunks = smart_retrieve(question)
            answer = generate_answer(question, chunks)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "chunks": chunks
            })
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {e}")