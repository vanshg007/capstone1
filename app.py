# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI library with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Customer Support Chatbot")

st.header("Customer Support Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Add sections for different types of support
st.sidebar.header("Support Categories")
categories = ["Billing", "Technical Support", "General Inquiries"]
category = st.sidebar.selectbox("Select a category", categories)

# Input text box for user input
input = st.text_input("How can we help you?", key="input")
submit = st.button("Ask")

# If the submit button is clicked and there is input
if submit and input:
    st.session_state['chat_history'].append(("You", input))
    response = get_gemini_response(f"[{category}] {input}")
    st.subheader("Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

# Add logging (optional)
if submit and input:
    with open("chat_log.txt", "a") as log_file:
        log_file.write(f"Category: {category}\nUser: {input}\nResponse: {chunk.text}\n\n")