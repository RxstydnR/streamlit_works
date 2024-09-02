# pip install streamlit_js_eval
import os
import pandas as pd
from typing import List, Iterable, Any, AsyncIterable, Dict

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAI,ChatOpenAI

import streamlit as st
from streamlit_js_eval import streamlit_js_eval
screen_width = streamlit_js_eval(js_expressions='screen.width')
screen_height = streamlit_js_eval(js_expressions='screen.height')


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

def get_model(model_name="gpt-3.5"):
    if model_name == "gpt-3.5":
        chat_model = ChatOpenAI(
            temperature=0,
            # api_key=openai_api_key,
            streaming=True,
            verbose=False
        )
    elif model_name=="gpt-4o":
        chat_model = ChatOpenAI(
            temperature=0,
            # api_key=openai_api_key,
            streaming=True,
            verbose=False
        )
    else:
        raise NotImplementedError()
    
    return chat_model

def build_prompt():
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system","{system}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    return prompt_template

def get_chain():
    prompt = build_prompt()
    model = get_model(model_name="gpt-4o")
    chain = prompt | model | StrOutputParser()
    return chain

##############################
# MERMAID RENDERING FUNCTION #
##############################
import streamlit_mermaid as stmd
def render_mermaid(mermaid_flowchart):
    stmd.st_mermaid(mermaid_flowchart, height=f"{int(screen_height/5*3)}px")

##############################
# Session State #
##############################
# セッション状態の初期化
if 'df' not in st.session_state:
    st.session_state.df = None

if 'chain' not in st.session_state:
    st.session_state.chain = get_chain()

session_id = "user0"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}

if "selected_columns" not in st.session_state:
    st.session_state.selected_columns = []

if "prompt_template" not in st.session_state:
    st.session_state.prompt_template = ""

if "prompt_type" not in st.session_state:
    st.session_state.prompt_type = ""

if "use_data_index" not in st.session_state:
    st.session_state.use_data_index = None

if "response_streaming" not in st.session_state:
    st.session_state.response_streaming = None  


st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

# st.markdown("""
#         <style>
#                #root > div:nth-child(1) > div.withScreencast > div > div > div > section:nth-child(2) {
#                     height: 3rem !important;
#                 }
#         </style>
#         """, unsafe_allow_html=True)

tab1,tab2,tab3,tab4 = st.tabs(["データ","分析","会話","フローチャート"])

# データのアップロードと確認
with tab1:
    uploaded_file = st.file_uploader("Excel or CSVファイルをアップロード", type=["xlsx", "csv"])
    if uploaded_file is None:
        st.warning("ファイルをアップロードしてください。")
        st.stop()
    else:
        try:
            if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                st.session_state.df = pd.read_excel(uploaded_file)
            else:
                st.session_state.df = pd.read_csv(uploaded_file)

            st.success("ファイルが正常にアップロードされました。")
            # 新しいファイルがアップロードされたら会話をリセット
            # st.session_state.conversation = setup_langchain()

            st.divider()
            
            # カラムの選択
            st.write("##### 分析に使用するカラムを選択してください")
            selected_columns = st.multiselect(
                "分析に使用するカラムを選択してください", 
                label_visibility = "collapsed",
                options = st.session_state.df.columns,
                default=st.session_state.df.columns.tolist(),
                key="selected_columns"
            )

            st.write("##### 選択されたカラムのプレビュー")
            # st.dataframe(st.session_state.df[selected_columns])
            df_show = st.session_state.df
            df_show["use"] = True
            selected_data_index = st.data_editor(df_show)["use"]
            st.session_state.use_data_index = selected_data_index

        except Exception as e:
            st.sidebar.error(f"ファイルの読み込み中にエラーが発生しました: {e}")    

# 会話の設定
with tab2:
    # プロンプトの選択
    prompt_type = st.selectbox("利用するプロンプトを選択してください", ["Q&A整理", "フローチャート", "追加質問の作成"])
    st.session_state.prompt_type = prompt_type
    # プロンプト入力欄
    prompt_template = ""
    if prompt_type == "Q&A整理":
        prompt_template = f"以下のデータを要約してください:\n"
    elif prompt_type == "フローチャート":
        prompt_template = f"以下のQ&Aに基づき、処理フローをマーメイド記法で整理してください。1回目の分岐において並列的な処理は極力減らしてください。2個目以降は特に制約はないです。:\n"
    elif prompt_type == "追加質問の作成":
        prompt_template = f"以下のデータについて質問に答えてください:\n"
    # st.session_state.prompt_template = prompt_template

    # ファイルの内容をプロンプトに追加
    sheet_content = ""
    #sheet_content += f"{col}: {', '.join(str(x) for x in st.session_state.df[col].tolist())}\n"
    use_df = st.session_state.df[st.session_state.use_data_index]
    for i in range(len(use_df)):
        add_content = ""
        for c in st.session_state.selected_columns:
            add_content += f"\n{c}: {use_df.iloc[i][c]}"
        sheet_content += add_content
        sheet_content += "\n"
    st.session_state.prompt_template = prompt_template + "\n\n#Q&A:\n"+sheet_content

    user_input = st.text_area("入力されるプロンプト", value=st.session_state.prompt_template, height=800)#)
    submit = st.button("実行")

with tab3:
    if len(st.session_state.selected_columns)<=0:
        st.warning("使用するカラムを選択してください。")
    else:

        messages_container = st.container(height=int(screen_height/5*3))
        
        # これまでのチャット履歴を全て表示する
        messages = get_session_history(session_id).messages
        with messages_container:
            if len(messages)>0:
                for i in range(len(messages)):
                    if messages[i].type == "human":
                        st.chat_message("user").write(messages[i].content)
                    elif (messages[i].type == "ai") or (messages[i].type == "AIMessageChunk"):
                        st.chat_message("ai").write(messages[i].content)
                    else:
                        raise NotImplementedError(f"message type: {messages[i].type} is not expected.")
                    
        if (query := st.chat_input()) or submit:

            if query == None:
                query = user_input
            
            # ユーザの入力を表示する
            with messages_container:
                st.chat_message("user").write(query)
                # st.chat_message("user").write("submitted")
                
                # AIの回答を表示する
                with st.chat_message("ai"):
                
                    # history を変換
                    history = get_session_history(session_id).messages
                
                    inputs = {
                        "system":"""You're an assistant to help a user.""",
                        "history":history,
                        "input":query
                    }
                    
                    chain = st.session_state.chain
                    response_streaming = chain.stream(inputs)
                    final_response = st.write_stream(response_streaming)
        
                    add_message_to_session_history(session_id, text=query, message_type="human")
                    add_message_to_session_history(session_id, text=final_response, message_type="ai")


with tab4:
    
    mermaid_text = st.text_area("入力されるプロンプト", height=300, placeholder="フローチャートを入力してください。")
    with st.container(height=int(screen_height/5*3)):   
        render_mermaid(mermaid_text)
    # if st.session_state.response_streaming:
    #     final_response = st.write_stream(st.session_state.response_streaming)
    #     add_message_to_session_history(session_id, text=final_response, message_type="ai")
    # st.markdown(st.session_state.prompt_type)
    # if st.session_state.prompt_type == "フローチャート":
        # render_mermaid()