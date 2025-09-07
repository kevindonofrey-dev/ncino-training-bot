import streamlit as st
import json
import difflib
import time
import re

# Load FAQ data
with open("ncino_faq.json", "r") as f:
    faq_data = json.load(f)

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Track suggested question clicked
if "new_question" not in st.session_state:
    st.session_state.new_question = None

# Helper function: get best match
def get_answer(user_question):
    questions = [item["question"] for item in faq_data]
    best_matches = difflib.get_close_matches(user_question, questions, n=3, cutoff=0.4)
    
    if best_matches:
        for item in faq_data:
            if item["question"] == best_matches[0]:
                return item["answer"]
    return "Sorry, I don’t have an answer for that yet."

# Helper function to highlight matching text
def highlight_match(text, query):
    pattern = re.escape(query)
    highlighted = re.sub(f"(?i)({pattern})", r"<mark>\1</mark>", text)
    return highlighted

# Streamlit UI
st.set_page_config(page_title="nCino Training Bot", page_icon="🤖", layout="centered")
st.title("🤖 nCino Training Bot")
st.write("Ask me how to navigate the nCino Loan Origination System UI.")

# Clear Chat History Button
if st.button("🗑️ Clear Chat History"):
    st.session_state.history = []

# Select category
categories = sorted(list(set(item.get("category", "General") for item in faq_data)))
selected_category = st.radio("Select FAQ Category:", categories)

# Search bo
