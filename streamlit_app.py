import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CW-MARAG",
    layout="centered"
)

st.title("🧠 CW-MARAG")
st.caption("Confidence-Weighted Multi-Agent RAG")

# ------------------ PDF Upload ------------------
st.header("📄 Upload PDF")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:
    with st.spinner("Indexing PDF..."):
        files = {
            "file": (uploaded_file.name, uploaded_file, "application/pdf")
        }
        res = requests.post(f"{BACKEND_URL}/upload/", files=files)

    if res.status_code == 200:
        st.success("PDF indexed successfully")
    else:
        st.error(f"Upload failed: {res.text}")

# ------------------ Query ------------------
st.header("❓ Ask a Question")

question = st.text_input("Enter your question")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        res = requests.post(
            f"{BACKEND_URL}/query/",
            json={"question": question}
        )

    if res.status_code == 200:
        data = res.json()

        st.subheader("🧠 Answer")
        st.write(data["answer"])

        st.subheader("📊 Evidence")
        for ev in data["evidence"]:
            st.markdown(
                f"**{ev['text']}**  \n"
                f"Confidence: `{ev['confidence']:.2f}`"
            )
    else:
        st.error("Query failed")
