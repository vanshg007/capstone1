# Customer Support Chatbot

This is a customer support chatbot built using Streamlit and Google's Generative AI (Gemini Pro). The chatbot can handle queries related to Billing, Technical Support, and General Inquiries.

## Features

- Ask for the user's name before starting the chat.
- Supports three categories: Billing, Technical Support, and General Inquiries.
- Validates user input based on predefined keywords for each category.
- Displays chat history.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/customer-support-chatbot.git
    cd customer-support-chatbot
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your environment variables by creating a `.env` file in the root directory of the project and add your Google API key:

    ```
    GOOGLE_API_KEY=your_google_api_key
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app1.py
    ```

2. Open your browser and go to the chatbot.

3. Enter your name and proceed with the chat.
