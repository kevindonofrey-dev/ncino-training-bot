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

# Search box for suggested questions
search_query = st.text_input("Search suggested questions:")

# Filter FAQs by category and search query
filtered_faqs = [
    item for item in faq_data
    if item.get("category", "General") == selected_category
    and search_query.lower() in item["question"].lower()
]

# Suggested Questions Panel
st.subheader("💡 Suggested Questions")
with st.container():
    for i, item in enumerate(filtered_faqs[:20]):  # show up to 20 matches
        question_display = highlight_match(item["question"], search_query) if search_query else item["question"]
        if st.button(label="", key=f"suggest_{i}"):
            st.session_state.new_question = item["question"]
        st.markdown(f'<div style="margin-bottom:5px;">{question_display}</div>', unsafe_allow_html=True)

# Input box
user_input = st.text_input("Or type your question here:")

# Determine which question to process
if st.session_state.new_question:
    user_input = st.session_state.new_question
    st.session_state.new_question = None

# Process the question
if user_input:
    st.session_state.history.append({"user": True, "message": user_input})
    
    # Typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("**Bot is typing...**")
    time.sleep(1.0)
    
    answer = get_answer(user_input)
    st.session_state.history.append({"user": False, "message": answer})
    typing_placeholder.empty()

# Display conversation history
st.subheader("💬 Conversation")
for chat in st.session_state.history:
    if chat["user"]:
        st.markdown(f"**You:** {chat['message']}")
    else:
        st.markdown(f"**Bot:** {chat['message']}")

# Auto-scroll to bottom
st.markdown(
    """
    <script>
    var chatDiv = window.parent.document.querySelector('[data-testid="stMarkdownContainer"]');
    if(chatDiv){
        chatDiv.scrollTop = chatDiv.scrollHeight;
    }
    </script>
    """,
    unsafe_allow_html=True
)
