from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(
    page_title="Q&A Bot 🤖",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# App Header with Emoji
st.markdown("""
    <h1 style='text-align: center;'>Q&A Bot 🤖</h1>
    <p style='text-align: center; font-size: 18px;'>Ask anything and let Gemini LLM provide the answers! 🎨</p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar customization
st.sidebar.markdown("""
    ## 🔧 Features:
    - Chat with an advanced LLM (Gemini Pro).
    - Stream responses for a dynamic experience.
    - Keep track of chat history.
    
    **💡 Tip:** Use clear and concise questions for the best answers!
    
    <hr>
    ❤️ Built with Streamlit & Google Generative AI
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input and buttons
st.text_input("Your Question 🔎:", key="input", placeholder="Type your question here...", label_visibility="visible")
submit = st.button("Ask 🔔")

# Process user input and display response
if submit and st.session_state.input:
    user_input = st.session_state.input
    st.session_state['chat_history'].append(("You", user_input))

    with st.spinner("Fetching response 🔄..."):
        response = get_gemini_response(user_input)
        bot_response = ""  # To store the full response
        for chunk in response:
            bot_response += chunk.text
        st.session_state['chat_history'].append(("Bot", bot_response))

    st.success("Response received! 🚀")

# Display Chat History
st.markdown("### 🕝 Chat History")
if st.session_state['chat_history']:
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.markdown(f"**{role} 🙋🏼:** {text}")
        else:
            st.markdown(f"**{role} 🤖:** {text}")
else:
    st.info("No chat history yet. Start asking questions! 🔍")

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 14px;'>
    ❤️ Powered by <strong>Google Generative AI</strong> & Streamlit. 🌐
    </p>
""", unsafe_allow_html=True)
