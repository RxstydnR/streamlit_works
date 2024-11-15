import pandas as pd
import streamlit as st

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages.base import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from retriever import SimpleTextRetriever
from prompts import contextualize_q_prompt, rag_prompt
from models import get_model

import uuid

# From here down is all the StreamLit UI.
st.set_page_config(
    page_title="LangChain RAG Demo", page_icon=":robot:",
    initial_sidebar_state="expanded"
    )

st.title("💬 RAG by 🦜🔗 library.")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

if "current_session_id" not in st.session_state:
    st.session_state["current_session_id"] = str(uuid.uuid4())

if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = "You are a helpful assistant."

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {st.session_state["current_session_id"]: {"messages": ChatMessageHistory(), "references": []}}

def get_session_history(session_id: str) -> dict:
    store = st.session_state["chat_history"]
    if session_id not in store:
        store[session_id] = {"messages": ChatMessageHistory(), "references": []}
    return store[session_id]

def set_session_history(session_id: str, chat_history, references):
    st.session_state["chat_history"][session_id] = {"messages": chat_history, "references": references}

@st.dialog("設定")
def config():
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password",)
    openai_api_key = "sk-xxxxx"
    if (not openai_api_key) or (not openai_api_key.startswith('sk-')):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
        st.write(f"Your OpenAI API Key starts with `{openai_api_key[:3]}`")
    
    st.text_area("System Prompt",value="You are a helpful assistant.",placeholder="Please input a system prompt",key="system_prompt")


with st.sidebar:
    # if st.button("Start New Chat", use_container_width=True, on_click=start_new_chat):
    if st.button("Start New Chat", use_container_width=True):
        new_session_id = str(uuid.uuid4())
        st.session_state["current_session_id"] = new_session_id
        st.session_state["chat_history"][new_session_id] = {"messages": ChatMessageHistory(), "references": []}
        st.rerun()

    st.button("設定", use_container_width=True, on_click=config)

    # モデル選択機能を追加
    model_option = st.selectbox(
        "モデルを選択してください",
        ("gpt-3.5-turbo", "gpt-4o"),
        index=1,
        key="model_selection"
    )
    st.divider()

    # 最新のチャット履歴を上位に表示する必要がある。
    chat_history_options = list(st.session_state["chat_history"].keys())[::-1]
    selected_session_id = st.selectbox(
        "チャット履歴を選択",
        options=chat_history_options,
        format_func=lambda x: f"Chat {x[:8]}",
        key="chat_history_selection"
    )
    
    if selected_session_id != st.session_state["current_session_id"]:
        st.session_state["current_session_id"] = selected_session_id
        st.rerun()

def get_question(input):
    if not input:
        return None
    elif isinstance(input,str):
        return input
    elif isinstance(input,dict) and 'question' in input:
        return input['question']
    elif isinstance(input,BaseMessage):
        return input.content
    else:
        raise Exception("string or dict with 'question' key expected as RAG chain input.")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
    

if "retriever" not in st.session_state:
    retriever = SimpleTextRetriever.from_texts([
        "apple is toxic.",
        "orange is treasure.",
        "grape is key to live forever.",
        "banana is a fruit.",
        "strawberry is red and sweet.",
        "blueberry is rich in antioxidants.",
        "mango is known as the king of fruits.",
        "pineapple contains an enzyme called bromelain.",
        "kiwi is a good source of vitamin C.",
        "watermelon is 92% water.",
    ])
    st.session_state["retriever"] = retriever

def main():
    # モデル選択を反映
    model = get_model(st.session_state.model_selection)
    retriever = st.session_state["retriever"]

    # retrieve chain
    retrieve_chain = RunnableLambda(get_question) | retriever
    condense_chain = contextualize_q_prompt | model
    rag_chain = rag_prompt | model
    
    # これまでのチャット履歴と参考情報を全て表示する
    current_session_id = st.session_state["current_session_id"]
    session_data = get_session_history(current_session_id)
    chat_history = session_data["messages"]
    references = session_data["references"]
    messages = chat_history.messages
    if len(messages) > 0:
        for i, message in enumerate(messages):
            if message.type == "human":
                st.chat_message("user").write(message.content)
            elif message.type in ["ai", "AIMessageChunk"]:
                with st.chat_message("ai"):
                    st.write(message.content)
                    with st.expander(f"See retrieved documents..."):
                        st.dataframe(references[i//2])
            else:
                raise NotImplementedError(f"message type: {message.type} is not expected.")

    # ユーザーの入力が送信された際に実行される処理
    if prompt := st.chat_input():

        # ユーザの入力を表示する
        st.chat_message("user").write(prompt)
        
        # AIの回答を表示する
        with st.chat_message("ai"):
                   
            if len(messages) > 0:
                # Condense question
                condensed_prompt = condense_chain.invoke({
                    "chat_history": chat_history.messages,
                    "question": prompt
                    })
            else:
                condensed_prompt = prompt

            # Retriever
            docs = retrieve_chain.invoke(condensed_prompt)
            
            # df_docsの作成
            df_docs = pd.DataFrame([
                {"content": doc.page_content, "metadata": doc.metadata}
                for doc in docs
            ])

            # RAG
            response = rag_chain.stream({
                "context": format_docs(docs),
                "question": condensed_prompt
            })
            final_response = st.write_stream(response)

            # 会話履歴と参考情報の追加
            chat_history.add_user_message(prompt)
            chat_history.add_ai_message(final_response)
            references.append(df_docs)
            set_session_history(current_session_id, chat_history, references)
            
            # 参考文献の表示
            with st.expander("See retrieved documents..."):
                st.dataframe(df_docs)
    
if __name__ == "__main__":
    main()