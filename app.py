import streamlit as st
import pandas as pd
import base64
from src.logic import find_exact_duplicates, find_fuzzy_duplicates, remove_duplicates

st.set_page_config(
    page_title="Duplicate Detection System",
    page_icon="🧠",
    layout="wide"
)

def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    page_bg_img = f"""
    <style>
    .stApp {{
        background:
            linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.75)),
            url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_bg("assets/background.png")

st.markdown("""
<style>

section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(12px);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

.stMetric {
    background: rgba(0,0,0,0.5);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
}

.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    border-radius: 10px;
}

h1, h2, h3 {
    color: #f1f5f9;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio(
    "Go to",
    ["📊 Dashboard", "📘 About Project", "🧩 Project Structure"]
)

file = st.sidebar.file_uploader("📂 Upload CSV", type=["csv"])

if page == "📊 Dashboard":

    st.markdown("""
    <div style="
        background: rgba(0,0,0,0.55);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.08);
    ">
    """, unsafe_allow_html=True)

    st.title("🧠 Duplicate Data Detection System")
    st.markdown("<h3 style='color:#e2e8f0;'>🚀 Smart Data Cleaning Dashboard</h3>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if file:
        df = pd.read_csv(file)

        total = len(df)
        unique = len(df.drop_duplicates())
        duplicate = total - unique

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", total)
        col2.metric("Unique", unique)
        col3.metric("Duplicates", duplicate)

        st.subheader("Dataset Preview")
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)

        if col1.button("Find Exact Duplicates"):
            st.dataframe(find_exact_duplicates(df.copy()), use_container_width=True)

        if col2.button("Find Similar Records"):
            fuzzy = find_fuzzy_duplicates(df.copy())
            for r in fuzzy:
                st.write(r)

        if col3.button("Clean Data"):
            clean = remove_duplicates(df.copy())
            st.dataframe(clean, use_container_width=True)

            csv = clean.to_csv(index=False).encode()
            st.download_button("Download Clean Data", csv, "cleaned_data.csv")

    else:
        st.info("Upload a CSV file")


elif page == "📘 About Project":

    st.title("📘 About This Project")

    st.markdown("""
### Duplicate Data Detection System

This project focuses on detecting and removing duplicate records from datasets. 
Duplicate data can lead to incorrect analysis, inefficient storage, and poor decision-making.

The system uses both exact matching and fuzzy matching techniques to identify duplicate and similar records.

Key Features:
- Exact duplicate detection using hashing
- Fuzzy matching using similarity scores
- Data cleaning functionality
- Interactive dashboard

Technologies Used:
- Python
- Pandas
- Streamlit
- RapidFuzz

Applications:
- Data cleaning
- Big data preprocessing
- Customer data management
- Machine learning pipelines

Conclusion:
This project demonstrates a scalable and efficient way to handle duplicate data without heavy infrastructure.
""")


elif page == "🧩 Project Structure":

    st.title("🧩 Project Structure & Code")

    st.markdown("### Folder Structure")

    st.code("""
duplicate-system/
│
├── app.py
├── requirements.txt
│
├── src/
│   └── logic.py
│
├── data/
│   └── dataset.csv
│
├── assets/
│   └── background.png
""")

    st.markdown("### app.py Code")

    with open("app.py", "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")

    st.markdown("### logic.py Code")

    with open("src/logic.py", "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")