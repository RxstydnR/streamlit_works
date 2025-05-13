import os
import pandas as pd
from typing import List, Iterable, Any

import streamlit as st
from dotenv import load_dotenv

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_models import get_model

# From here down is all the StreamLit UI.
st.set_page_config(
    page_title="🚀 A streamlit chatbot powered by OpenAI LLM", page_icon=":streamlit:",
    initial_sidebar_state='collapsed'
    )

# st.title("💬 RAG by 🦜🔗 library.")
# st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")


from styles.background import MAIN_APP_CONTENTS_CSS, CHAT_MESSAGE_CSS, SIDEBAR_CSS
from styles.fadein import CHAR_FADEIN_ANIMATION_CSS

st.markdown("""
<style>
    .stAppViewBlockContainer {
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)
st.markdown(MAIN_APP_CONTENTS_CSS, unsafe_allow_html=True)
st.markdown(CHAT_MESSAGE_CSS, unsafe_allow_html=True)
st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
st.markdown(CHAR_FADEIN_ANIMATION_CSS, unsafe_allow_html=True)


session_id = "user0"

llm_options = [
    "gpt-4o",
    "o1",
    "o3-mini",
    "gemini-2.5-flash",
    "gemini-2.5-pro"
]


@st.experimental_dialog("Are you sure to delete all chat history?")
def delete_chat_history():
    if st.button("Yes"):
        store = st.session_state["chat_history"]
        if len(store[session_id].messages)>0:
            store[session_id].clear()
            st.rerun()
        else:
            st.warning("No chat history.")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}

# def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
def get_session_history(session_id: str):
    store = st.session_state["chat_history"]
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def set_session_history(session_id: str, chat_history):
    store = st.session_state["chat_history"]
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    store[session_id] = chat_history


with st.sidebar:
    st.selectbox("LLM model", llm_options, index=0, key="llm")

    system_prompt = st.text_area("System Prompt",value="",placeholder="Please input a system prompt")
    if st.button("Delete Chat History"):
        delete_chat_history()


def main():

    llm = get_model(st.session_state["llm"])
    
    # これまでのチャット履歴を全て表示する
    # messages = get_session_history(user_id, conversation_id)
    chat_history = get_session_history(session_id)
    messages = chat_history.messages
    if len(messages)>0:
        # st.info(messages[i].type)
        for i in range(len(messages)):
            if messages[i].type == "human":
                st.chat_message("user").write(messages[i].content)
            elif (messages[i].type == "ai") or (messages[i].type == "AIMessageChunk"):
                st.chat_message("ai").write(messages[i].content)
            else:
                raise NotImplementedError(f"message type: {messages[i].type} is not expected.")
    

    # ユーザーの入力が送信された際に実行される処理
    if prompt := st.chat_input():

        # ユーザの入力を表示する
        st.chat_message("user").write(prompt)
        chat_history.add_user_message(prompt)
        
        # AIの回答を表示する
        with st.chat_message("ai"):
                
            # RAG)
            # st.write(chat_history.messages)
            response = llm.stream(chat_history.messages)
            final_response = st.write_stream(response)
            
            # 会話履歴の追加
            chat_history.add_ai_message(final_response)
            set_session_history(session_id,chat_history)
    
if __name__ == "__main__":
    main()