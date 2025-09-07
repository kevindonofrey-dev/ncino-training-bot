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

# Helper: get best match
def get_answer(user_question):
    questions = [item["question"] for item in faq_data]
    best_matches = difflib.get_close_matches(user_question, questions, n=3, cutoff=0.4)
    if best_matches:
        for item in faq_data:
            if item["question"] == best_matches[0]:
                return item["answer"]
    return "Sorry, I don’t have an answer for that yet."

# Highlight matching text (for display only)
def highlight_match(text, query):
    if query:
        pattern = re.escape(query)
        return re.sub(f"(?i)({pattern})", r"**\1**", text)
    return text

# Streamlit UI
st.set_page_config(page_title="nCino Training Bot", page_icon="🤖", layout="centered")
st.title("🤖 nCino Training Bot")
st.write("Ask me how to navigate the nCino Loan Origination System UI.")

# Clear Chat History
if st.button("🗑️ Clear Chat History"):
    st.session_state.history = []

# Category selection
categories = sorted(list(set(item.get("category", "General") for item in faq_data)))
selected_category = st.radio("Select FAQ Category:", categories)

# Search box
search_query = st.text_input("Search suggested questions:")

# Filter FAQs
filtered_faqs = [
    item for item in faq_data
    if item.get("category", "General") == selected_category
    and search_query.lower() in item["question"].lower()
]

# Suggested Questions
st.subheader("💡 Suggested Questions")
for i, item in en
