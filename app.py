import streamlit as st
import json
import difflib

# Load FAQ data
with open("ncino_faq.json", "r") as f:
    faq_data = json.load(f)

# Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Helper function: get best match
def get_answer(user_question):
    questions = [item["question"] for item in faq_data]
    best_matches = difflib.get_close_matches(user_question, questions, n=3, cutoff=0.4)
    
    if best_matches:
        for item in faq_data:
            if item["question"] == best_matches[0]:
                return item["answer"]
    return "Sorry, I don’t have an answer for that yet."

# Streamlit UI
st.set_page_config(page_title="nCino Training Bot", page_icon="🤖", layout="centered")
st.title("🤖 nCino Training Bot")
st.write("Ask me how to navigate the nCino Loan Origination System UI.")

# Suggested Questions Panel
st.subheader("💡 Suggested Questions")
cols = st.columns(2)
for i, item in enumerate(faq_data[:10]):  # show first 10 suggestions
    col = cols[i % 2]
    if col.button(item["question"]):
        answer = get_answer(item["question"])
        st.session_state.history.append({"user": True, "message": item["question"]})
        st.session_state.history.append({"user": False, "message": answer})
        st.experimental_rerun()

# Display conversation history
st.subheader("💬 Conversation")
for chat in st.session_state.history:
    if chat["user"]:
        st.markdown(f"**You:** {chat['message']}")
    else:
        st.markdown(f"**Bot:** {chat['message']}")

# Input box
user_input = st.text_input("Or type your question here:")

if user_input:
    answer = get_answer(user_input)
    st.session_state.history.append({"user": True, "message": user_input})
    st.session_state.history.append({"user": False, "message": answer})
    st.experimental_rerun()
