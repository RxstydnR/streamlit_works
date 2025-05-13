from langchain_openai import OpenAI,ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# https://python.langchain.com/docs/integrations/chat/openai/
# from langchain_openai import ChatOpenAI
# reasoning = {
#     "effort": "medium",  # 'low', 'medium', or 'high'
#     "summary": "auto",  # 'detailed', 'auto', or None
# }
# llm = ChatOpenAI(
#     model="o4-mini",
#     use_responses_api=True,
#     model_kwargs={"reasoning": reasoning},
# )
# response = llm.invoke("What is 3^3?")
# # Output
# response.text()

def get_model(model_name="gpt-4o"):
    
    if model_name == "gpt-4o":
        chat_model = ChatOpenAI(
            temperature=0,
            # api_key=openai_api_key,
            streaming=True,
            verbose=False,
            model="gpt-4o"
        )
        return chat_model
    
    elif model_name == "o1":
        chat_model = ChatOpenAI(
            # api_key=openai_api_key,
            streaming=True,
            verbose=False,
            model="o1"
        )
        return chat_model

    elif model_name == "o3-mini":
        chat_model = ChatOpenAI(
            # api_key=openai_api_key,
            streaming=True,
            verbose=False,
            model="o3-mini"
        )
        return chat_model

    elif model_name == "gemini-2.5-flash":
        chat_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-preview-04-17",
            temperature=0,
            streaming=True,
        )
        return chat_model
    
    elif model_name == "gemini-2.5-pro":
        chat_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro-preview-05-06",
            temperature=0,
            streaming=True,
        )
        return chat_model

    else:
        raise NotImplementedError()
    

# llm_options = [
#     "gpt-4o",
#     "o1",
#     "o3-mini",
#     "gemini-2.5-flash",
#     "gemini-2.5-pro"
# ]