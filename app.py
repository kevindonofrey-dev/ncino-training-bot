import streamlit as st
import json
import difflib

# Load FAQ data
with open("ncino_faq", "r") as f:
    faq_data = json.load(f)

# Helper function: find best match
def get_answer(user_question):
    questions = [item["question"] for item in faq_data]
    best_match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.4)
    if best_match:
        for item in faq_data:
            if item["question"] == best_match[0]:
                return item["answer"]
    return "Sorry, I don’t have an answer for that yet."

# Streamlit UI
st.set_page_config(page_title="nCino Training Bot", page_icon="🤖", layout="centered")

st.title("🤖 nCino Training Bot")
st.write("Ask me how to navigate the nCino Loan Origination System UI.")

# Input box
user_input = st.text_input("Type your question here:")

if user_input:
    answer = get_answer(user_input)
    st.write(f"**Answer:** {answer}")
