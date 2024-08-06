import os
import requests
from typing import List, Iterable, Any, AsyncIterable, Dict

import streamlit as st
from dotenv import load_dotenv

from langchain import hub
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_openai import OpenAI,ChatOpenAI

# From here down is all the StreamLit UI.
st.set_page_config(page_title="LangChain Simple Chat Demo", page_icon=":robot:")
st.title("💬 Chatbot by 🦜🔗 library.")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

session_id = "user0"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}

@st.experimental_dialog("Are you sure to delete all chat history?")
def delete_chat_history():
    if st.button("Yes"):
        store = st.session_state["chat_history"]
        if len(store[session_id].messages)>0:
            store[session_id].clear()
            st.rerun()
        else:
            st.warning("No chat history.")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password",)
    openai_api_key = "sk-"
    if (not openai_api_key) or (not openai_api_key.startswith('sk-')):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        st.write(f"Your OpenAI API Key starts with `{openai_api_key[:3]}`")
        st.stop()
    system_prompt = st.text_area("System Prompt",value="",placeholder="Please input a system prompt")

    if st.button("Delete Chat History"):
        delete_chat_history()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    store = st.session_state["chat_history"]
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def add_message_to_session_history(session_id: str, text: str, message_type: str) -> BaseChatMessageHistory:
    store = st.session_state["chat_history"]
    if message_type=="human":
        store[session_id].add_user_message(text)
    elif message_type=="ai":
        store[session_id].add_ai_message(text)
    else:
        raise NotImplementedError(f"type:{message_type} in invalid.")
    st.session_state["chat_history"] = store
    return None

def add_user_message_to_session_history(session_id: str, text: str) -> BaseChatMessageHistory:
    store = st.session_state["chat_history"]
    store[session_id].add_user_message(text)
    st.session_state["chat_history"] = store[session_id]
    return None

def send_message(inputs: Dict):# -> AsyncIterable[str]:
    URL = "http://127.0.0.1:8000/stream"  
    response = requests.post(URL, json=inputs, stream=True)
    for chunk in response.iter_content(chunk_size=None):
        if chunk: 
            yield chunk.decode()

def main():
    
    # これまでのチャット履歴を全て表示する
    messages = get_session_history(session_id).messages
    if len(messages)>0:
        for i in range(len(messages)):
            if messages[i].type == "human":
                st.chat_message("user").write(messages[i].content)
            elif (messages[i].type == "ai") or (messages[i].type == "AIMessageChunk"):
                st.chat_message("ai").write(messages[i].content)
            else:
                raise NotImplementedError(f"message type: {messages[i].type} is not expected.")
            
    # ユーザーの入力が送信された際に実行される処理
    if query := st.chat_input():

        # ユーザの入力を表示する
        st.chat_message("user").write(query)
        
        # AIの回答を表示する
        with st.chat_message("ai"):
            from langchain.schema import messages_to_dict

            # history を変換
            history = get_session_history(session_id).messages
            serializable_history = messages_to_dict(history)
            # 以下のエラー回避
            # このエラーは、JSON シリアライズできないオブジェクト（この場合は langchain の HumanMessage）を API に送信しようとしたために発生しています。この問題を解決するには、HumanMessage オブジェクトを JSON シリアライズ可能な形式に変換する必要があります。

            # LCELのconfigの外出し機能があるからstatelessでいけそう。
            inputs = {
                "system":"""You're an assistant to help a user.""",
                "history":serializable_history,
                "input":query
            }
            response = send_message(inputs)
            st.write_stream(response)
            # st.write_stream(stream_data(response))

        # response = "demo"# responseをstrに変換する処理
        add_message_to_session_history(session_id, text=query, message_type="human")
        add_message_to_session_history(session_id, text=query, message_type="ai")
    
if __name__ == "__main__":
    main()