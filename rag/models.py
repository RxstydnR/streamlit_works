from langchain_openai import OpenAI,ChatOpenAI

def get_model(model_name="gpt-4o"):
    if model_name == "gpt-3.5-turbo":
        chat_model = ChatOpenAI(
            temperature=0,
            # api_key=openai_api_key,
            streaming=True,
            verbose=False,
            model="gpt-3.5-turbo"
        )
        return chat_model
    elif model_name == "gpt-4o":
        chat_model = ChatOpenAI(
            temperature=0,
            # api_key=openai_api_key,
            streaming=True,
            verbose=False,
            model="gpt-4o"
        )
        return chat_model
    else:
        raise NotImplementedError()