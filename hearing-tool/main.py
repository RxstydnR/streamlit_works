import os
import requests
from typing import List, Iterable, Any, AsyncIterable, Dict

import pandas as pd
import streamlit as st

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

# !Todo
# - sidebarのやつをデータタブに移動し
# - sidebarはchat用にする
# - sidebar の面積を大きくする。
# - メインにはmermaidの結果のみを出すようにする。


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
            api_key=openai_api_key,
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
import streamlit.components.v1 as components
import streamlit_mermaid as stmd
def render_mermaid(mermaid_flowchart):
    # <div class="mermaid-container" style="overflow-y: auto; max-height: 750px;">
    # components.html(
    # st.html(
    #     f"""
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    #     <script src="https://cdn.jsdelivr.net/npm/mermaid@latest/dist/mermaid.min.js"></script>
    #     <div class="mermaid-container" style="overflow-y: auto;">
    #         <div class="mermaid">
    #         {mermaid_flowchart}
    #         </div>
    #     </div>
    #     <script>
    #         mermaid.initialize({{
    #             startOnLoad: true,
    #             fontFamily: 'monospace, sans-serif',
    #             flowchart: {{
    #                 htmlLabels: true,
    #                 useMaxWidth: true,
    #             }},
    #             securityLevel: 'loose',
    #         }});
    #         mermaid.parseError = function(err, hash) {{
    #             console.error('Mermaid error:', err);
    #         }};
    #     </script>
    #     """,
    #     # height=2000,
    # )
    stmd.st_mermaid(mermaid_flowchart, height="1000px")

# セッション状態の初期化
if 'df' not in st.session_state:
    st.session_state.df = None

if 'chain' not in st.session_state:
    st.session_state.chain = get_chain()

session_id = "user0"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}


# サイドバーでファイルアップロード
with st.sidebar:
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
        with st.sidebar:
            st.success("ファイルが正常にアップロードされました。")
            # 新しいファイルがアップロードされたら会話をリセット
            # st.session_state.conversation = setup_langchain()

            # プロンプトの選択
            prompt_type = st.selectbox("利用するプロンプトを選択してください", ["Q&A整理", "フローチャート", "追加質問の作成"])

            # プロンプト入力欄
            prompt_template = ""
            if prompt_type == "Q&A整理":
                prompt_template = f"以下のデータを要約してください:\n"
            elif prompt_type == "フローチャート":
                prompt_template = f"以下のQ&Aに基づき、処理フローをマーメイド記法で整理してください。1回目の分岐において並列的な処理は極力減らしてください。2個目以降は特に制約はないです。:\n"
            elif prompt_type == "追加質問の作成":
                prompt_template = f"以下のデータについて質問に答えてください:\n"

    except Exception as e:
        st.sidebar.error(f"ファイルの読み込み中にエラーが発生しました: {e}")

# タブの作成
tab0, tab1, tab2 = st.tabs(["データ","分析","xxx"])

with tab0:
    if st.session_state.df is not None:
        # カラムの選択
        selected_columns = st.multiselect("分析に使用するカラムを選択してください", st.session_state.df.columns, default=st.session_state.df.columns.tolist())

        # 選択されたカラムのデータフレームを表示
        if st.toggle("データフレーム全体を表示", value=False):
            st.write("##### 選択されたカラムのプレビュー（全体）")
            # st.dataframe(st.session_state.df[selected_columns])
            df_show = st.session_state.df
            df_show["use"] = True
            dd = st.data_editor(df_show)
        else:
            st.write("##### 選択されたカラムのプレビュー（上位5行）")
            st.dataframe(st.session_state.df[selected_columns].head())
            

with tab1:        
    if len(selected_columns)<=0:
        st.warning("使用するカラムを選択してください。")
        st.stop()
    else:
        # ファイルの内容をプロンプトに追加
        sheet_content = ""
        for col in selected_columns:
            #sheet_content += f"{col}: {', '.join(str(x) for x in st.session_state.df[col].tolist())}\n"
            for i in range(len(st.session_state.df)):
                add_content = ""
                for c in st.session_state.df.columns.tolist():
                    add_content += f"\n{c}: {st.session_state.df.iloc[i][c]}"
                sheet_content += add_content
                sheet_content += "\n"
            # {', '.join(str(x) for x in )}\n"
        prompt_template += "\n\n#Q&A:\n"+sheet_content

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
        
        with st.sidebar:
            with st.popover("Prompt"):
                # st.markdown("")
                # name = st.text_input("What's your name?")
                user_input = st.text_area("プロンプトを入力してください", value=prompt_template, height=800)#)
            submit = st.button("実行")
        
        # ユーザーの入力が送信された際に実行される処理
        if not submit:
            st.info("実行してください。")
        elif submit:
            # query := st.chat_input(placeholder=prompt_template):
            query = user_input
            
            # ユーザの入力を表示する
            st.chat_message("user").write(query)
            
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

        elif query := st.chat_input(placeholder=prompt_template):
            query = query
            
            # ユーザの入力を表示する
            st.chat_message("user").write(query)
            
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
        
with tab2:
    mermaid_text = """graph TD
A[工事計画の立案を始める] --> B[プロジェクトの規模や複雑さの評価]
B --> C[リスク評価]
C --> D[工程表の作成手順]
D --> E[資源配分]
E --> F[予算管理]
F --> G[品質管理]
G --> H[ステークホルダーとのコミュニケーション計画]
H --> I[変更管理プロセス]
I --> J[プロジェクト完了時の評価]
J --> K[工事現場の安全管理]
K --> L[環境への配慮]
L --> M[下請け業者の選定と管理]
M --> N[工事の進捗管理]
N --> O[技術的な問題や障害への対処]
O --> P[品質検査のプロセス]
P --> Q[工事に必要な許認可の取得プロセス]
Q --> R[天候や自然災害のリスクへの対応]
R --> S[資材の調達と在庫管理]
S --> T[プロジェクト完了後の保証期間中の対応]
    """
    render_mermaid(mermaid_text)

    