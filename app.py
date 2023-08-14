#####################
# smartChat - app.py
#
# pip install streamlit streamlit-chat langchain python-dotenv
#
# create a .env file and put the following line of code in it:
#     OPENAI_API_KEY = "{your openai key}"
#
# replace {your openai key} with your key from OpenAI
#
# once you have created .env and added your own key, set use_env = 1 on line 69
# 
# To run the application: >streamlit run app.py
#####################

import os
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage,HumanMessage,AIMessage)

def init():
    clear_button = st.sidebar.button("New Chat", key="clear")

    with open("sidebar.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()

    st.sidebar.markdown(sidebar_content)

    clear_button2 = st.sidebar.button("New Chat", key="clear2")
    # reset everything
    if clear_button:
        st.session_state['messages'] = [
            SystemMessage(content="You are a helpful assistant.")
        ]
    if clear_button2:
        st.session_state['messages'] = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    st.sidebar.markdown("[Code on Github](https://github.com/mikecallahan/smartChat)")

def main():
    init()

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
    
    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]

    # capture the user's prompt
    user_input = st.chat_input("Your prompt: ", key="user_input")

    # handle user prompt
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')

if __name__ == '__main__':

    # when switching the value of use_env you must re-initialize the app
    # i.e python run mychat.py
    use_env=1
    st.set_page_config(page_title="Your own ChatGPT",page_icon="🤖")
    st.header("Welcome to smartChat")
    
    # if using .env 
    if use_env == 0:
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") != "{your openai key}":
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            main()
        else:
            st.error("Please add a valid OpenAI API key to the .env file and re-initialize the app.")
            exit()
    else:
        # if not using .env 
        OPENAI_API_KEY = st.sidebar.text_input("Your OpenAI API key", type="password")
        if not OPENAI_API_KEY:
            st.warning("Please add your OpenAI API key to continue.")
            init()
            st.stop()
        else:
           main()