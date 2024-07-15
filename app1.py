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

billing_keywords = [
    "invoice", "payment", "bill", "charge", "refund", "fee", "receipt", "cost", 
    "subscription", "credit", "debit", "balance", "overcharge", "discount", 
    "plan", "statement", "payment method", "due date", "transaction", "billing address", 
    "fiscal", "budget", "tax", "payment confirmation", "payment gateway", 
    "bank transfer", "auto-renewal", "late fee", "outstanding balance", "prepayment", 
    "rebate", "reimbursement", "service charge", "settlement", "wire transfer", 
    "chargeback", "overdue", "penalty", "fund", "authorization", "payment schedule", 
    "billing cycle", "account number", "direct debit", "installment", "online payment", 
    "processing fee", "annual fee", "monthly fee", "adjustment", "billing error", "order", "buy", "sell", "price"
]
technical_support_keywords = [
    "error", "issue", "problem", "bug", "technical", "crash", "failure", "glitch", 
    "malfunction", "troubleshoot", "fix", "support", "update", "installation", 
    "setup", "configuration", "connectivity", "performance", "hardware", "software", 
    "network", "server", "database", "login", "authentication", "password reset", 
    "firewall", "virus", "malware", "patch", "driver", "firmware", "compatibility", 
    "backup", "restore", "data loss", "encryption", "security", "wifi", "bluetooth", 
    "printer", "scanner", "monitor", "keyboard", "mouse", "webcam", "microphone", 
    "headset", "mobile app", "slow performance", "no sound", "freeze", "order", "buy", "sell", "price"
]
general_inquiries_keywords = [
    "information", "general", "question", "query", "contact", "help", "support", 
    "assistance", "details", "overview", "availability", "service", "product", 
    "policy", "procedure", "guideline", "FAQ", "feedback", "complaint", "suggestion", 
    "recommendation", "request", "customer service", "opening hours", "location", 
    "address", "phone number", "email", "website", "social media", "terms", 
    "conditions", "privacy policy", "return policy", "warranty", "guarantee", 
    "price", "quote", "estimate", "catalog", "brochure", "manual", "tutorial", 
    "training", "demonstration", "event", "webinar", "seminar", "conference", 
    "promotion", "special offer", "membership", "subscription", "order", "buy", "sell", "price"
]
category_keywords = {
    "Billing": billing_keywords,
    "Technical Support": technical_support_keywords,
    "General Inquiries": general_inquiries_keywords
}

def validate_input(category, user_input):
    keywords = category_keywords.get(category, [])
    for keyword in keywords:
        if keyword.lower() in user_input.lower():
            return True
    return False

# Initialize Streamlit app
st.set_page_config(page_title="Customer Support Chatbot")

st.header("Customer Support Chatbot")

# Ask for the user's name if not already provided
if 'name' not in st.session_state:
    with st.form(key='name_form'):
        name = st.text_input("What is your name?", key="name_input")
        submit_name = st.form_submit_button(label='Submit')
        if submit_name and name:
            st.session_state['name'] = name
            st.session_state['chat_history'] = [("Bot", f"Hello {name}, how can I assist you today?")]
            st.rerun()
else:
    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [("Bot", f"Hello {st.session_state['name']}, how can I assist you today?")]

    # Add sections for different types of support
    st.sidebar.header("Support Categories")
    categories = ["Billing", "Technical Support", "General Inquiries"]
    category = st.sidebar.selectbox("Select a category", categories)

    # Input text box for user input
    input = st.text_input(f"How can we help you {st.session_state['name']}?", key="input")
    submit = st.button("Ask")

    # If the submit button is clicked and there is input
    if submit and input:
        if validate_input(category, input):
            st.session_state['chat_history'].append((st.session_state['name'], input))
            response = get_gemini_response(f"[{category}] {input}")
            st.subheader("Response")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
        else:
            message = f"Sorry {st.session_state['name']}, can you please ask questions related to {category}. You can check the keywords in the code."
            st.write(message)
            st.session_state['chat_history'].append((st.session_state['name'], input))
            st.session_state['chat_history'].append(("Bot", message))

    # Display chat history
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    # Add logging (optional)
    if submit and input:
        with open("chat_log.txt", "a") as log_file:
            log_file.write(f"Category: {category}\nUser: {input}\nResponse: {chunk.text}\n\n")