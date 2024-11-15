from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain import hub

# 過去の会話履歴を元に質問文を作り替える
contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is.\
"""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
# rag chain
rag_prompt = hub.pull("rlm/rag-prompt")