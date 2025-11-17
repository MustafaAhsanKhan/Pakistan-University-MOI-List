import os
import re
import pandas as pd
from docx import Document
import streamlit as st

# -----------------------------
# Helper functions
# -----------------------------
def clean_line(text):
    text = re.sub(r"^(\s*[\-\*\•\·]\s*)", "", text)  # remove bullets
    text = re.sub(r"^\s*\d+[\)\.\-]\s*", "", text)   # remove numbering
    text = " ".join(text.split())
    return text.strip()

def build_index(folder="."):
    index = {}  # {pak_uni: set(uk_unis)}
    for filename in os.listdir(folder):
        if filename.endswith(".docx"):
            uk_uni = os.path.splitext(filename)[0]
            path = os.path.join(folder, filename)
            try:
                doc = Document(path)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
            for para in doc.paragraphs:
                raw = para.text.strip()
                if not raw:
                    continue
                cleaned = clean_line(raw)
                if not cleaned:
                    continue
                pak_uni_key = cleaned
                if pak_uni_key not in index:
                    index[pak_uni_key] = set()
                index[pak_uni_key].add(uk_uni)
    return index

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Pakistani → UK University Matcher")

st.write("Search for a Pakistani university to see which UK universities accept it.")

# Build index from current directory
index = build_index(".")

query = st.text_input("Search Pakistani University:", "")

if query:
    query_lower = query.lower()
    results = {}
    for pak_uni, uk_unis in index.items():
        if query_lower in pak_uni.lower():
            results[pak_uni] = list(uk_unis)

    if results:
        st.write(f"Found {len(results)} match(es):")
        for pak_uni, uk_list in results.items():
            st.subheader(pak_uni)
            for uk in uk_list:
                st.write(f" - {uk}")
    else:
        st.write("No matches found.")
