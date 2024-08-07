import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel
from langchain_core.output_parsers import StrOutputParser
from typing import AsyncIterable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import messages_from_dict
from typing import List, Iterable, Any, AsyncIterable, Dict

openai_api_key = "sk-"

# FastAPI instance
app = FastAPI()

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
            api_key=openai_api_key,
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

# logging.info(f"Received request: {completion_request}")

from pydantic import BaseModel
class Inputs(BaseModel):
    system:str
    history:List
    input:str

# parameterも含めて投げたい
# エラー回避
# https://stackoverflow.com/questions/64236572/fastapi-typeerror-object-of-type-modelmetaclass-is-not-json-serializable
@app.post("/stream", response_model=Inputs)
def stream(inputs:Inputs):
    chain = get_chain()
    
    # 受け取った history を Message オブジェクトに変換
    history = messages_from_dict(inputs.history)

    streaming = chain.stream({
        "system":inputs.system,
        "history":history,
        "input":inputs.input
    })
    return StreamingResponse(streaming, media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
