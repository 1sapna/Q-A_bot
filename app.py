from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Check if the API key is available
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Error: GOOGLE_API_KEY not found in the environment variables. Please set it in the .env file.")
else:
    # Configure Google API with the secret GOOGLE_API_KEY
    genai.configure(api_key=api_key)

    # Function to load Gemini Pro model and get responses
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])

    def get_gemini_response(question):
        try:
            response = chat.send_message(question, stream=True)
            return response
        except Exception as e:
            st.error(f"Error while generating response: {e}")
            return []

    # Initialize Streamlit app with an attractive frontend
    st.set_page_config(page_title="Q-A_bot", page_icon=":robot_face:")

    st.markdown("""
        <style>
        .header {
            font-size: 40px;
            font-weight: bold;
            color: #2F80ED;
            text-align: center;
        }
        .subheader {
            font-size: 20px;
            font-weight: bold;
            color: #2F80ED;
        }
        .chat-container {
            background-color: #f0f4f8;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 10px;
        }
        .message-user {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .message-bot {
            background-color: #dfe6e9;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header and page title
    st.markdown('<p class="header">Q-A_bot 🤖</p>', unsafe_allow_html=True)
    st.markdown("<h2 class='subheader'>Ask your questions below! 💬</h2>", unsafe_allow_html=True)

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Input form for asking a question
    input_question = st.text_input("Your Question: 🤔", key="input")
    submit = st.button("Ask the Question! ✨")

    if submit and input_question:
        # Get Gemini response
        response = get_gemini_response(input_question)

        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_question))
        
        st.subheader("The Response is: 🧠")
        with st.expander("Show Response", expanded=True):
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))

    # Chat History Display
    st.subheader("Chat History 🗨️")
    with st.container():
        for role, text in st.session_state['chat_history']:
            if role == "You":
                st.markdown(f'<div class="message message-user">{role}: {text}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message message-bot">{role}: {text}</div>', unsafe_allow_html=True)
