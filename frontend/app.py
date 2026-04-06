import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Engine", layout="centered")

st.markdown("""
    <style>
    /* Styling untuk Container Hasil (Card) */
    .result-card {
        background-color: #1E1E2E; /* Warna dark mode ala VScode/Discord */
        border: 1px solid #2D2D3B;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .result-card:hover {
        border-color: #6366f1; /* Hover effect warna ungu Indigo */
        transform: translateY(-2px);
    }
    
    /* Styling untuk Badge Score */
    .result-badge {
        font-size: 0.8rem;
        color: #A6ACCD;
        background-color: #28293D;
        padding: 4px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 16px;
        font-weight: 600;
        border: 1px solid #3E405B;
    }
    
    /* Styling untuk Teks Utama */
    .result-text {
        font-size: 0.95rem;
        line-height: 1.7;
        color: #E4E4E5;
        margin-bottom: 16px;
        text-align: justify;
    }
    
    /* Styling untuk Metadata (Footer Card) */
    .result-meta {
        font-size: 0.8rem;
        color: #787CB5;
        border-top: 1px solid #2D2D3B;
        padding-top: 12px;
        font-family: monospace;
        display: flex;
        justify-content: space-between;
    }
    </style>
""", unsafe_allow_html=True)

st.title("RAG Engine")
st.markdown("Upload dokumen rahasia lu, then ask anything!")

with st.sidebar:
    st.header("Upload Knowledge")
    uploaded_file = st.file_uploader("Upload PDF atau TXT", type=["pdf", "txt", "md"])
    if st.button("Upload ke Database", use_container_width=True):
        if uploaded_file is not None:
            with st.spinner("Mengekstrak & Chunking teks..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                res = requests.post(f"{API_URL}/documents/file", files=files)
                if res.status_code == 200:
                    st.success(f"Sukses! ID: {res.json()['parent_id']}")
                else:
                    st.error("Gagal upload file.")
        else:
            st.warning("Pilih file dulu yakk")

st.header("Semantic Search")

with st.form(key="search_form"):
    query = st.text_input("Tanya sesuatu berdasarkan dokumen yang udah diupload:", placeholder="Ketik keyword atau pertanyaan di sini...")
    submit_search = st.form_submit_button("Cari Jawaban", use_container_width=True)

if submit_search:
    if query:
        with st.spinner("Mencari konteks paling relevan di database..."):
            res = requests.post(f"{API_URL}/search", json={"query": query, "n_results": 3})
            if res.status_code == 200:
                results = res.json().get("results", [])
                if results:
                    st.markdown(f"**Menemukan {len(results)} potongan dokumen yang relevan:**")
                    
                    for idx, r in enumerate(results, 1):
                        filename = r['metadata'].get('filename', 'Unknown File')
                        chunk_idx = r['metadata'].get('chunk_index', 0)
                        
                        st.markdown(f"""
                            <div class="result-card">
                                <div class="result-badge">Hasil {idx} • Akurasi: {(1 / (1 + r['distance'])) * 100:.1f}%</div>
                                <div class="result-text">{r['text']}</div>
                                <div class="result-meta">
                                    <span>{filename}</span>
                                    <span>Chunk: {chunk_idx}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Nggak ada info yang nyambung di database.")
    else:
        st.warning("Ketik pertanyaannya dulu!")