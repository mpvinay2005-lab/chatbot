import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

#Load environment variables
load_dotenv()

#confiure streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro",
    page_icon=":brain:", #favicon emoji
    layout= "centered"
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#set up google gemini-pro AI model
gen_ai.configure(api_key= GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-2.5-flash")
#Function to translate roles between Gemini-pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
#Initialize chat session in streamlit if not already present 
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


#Display the chatbot's title on the page
st.title("Gemini Pro- Chatbot")

#Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        if message.parts:
           st.markdown(message.parts[0].text)

#input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro..")
if user_prompt:
    #Add user's prompt to chat and display
    st.chat_message("user").markdown(user_prompt)

    #send user's message to Gemini-Pro  and get the response
    gemini_response= st.session_state.chat_session.send_message(user_prompt)

    #display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)



# gen_ai.configure(api_key=GOOGLE_API_KEY)

# for m in gen_ai.list_models():
#     print(m.name)