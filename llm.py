from langchain_openai import ChatOpenAI
import streamlit as st
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# from config import OPENAI_API_KEY

llm = ChatOpenAI(
    openai_api_key = OPENAI_API_KEY,
    model = "gpt-3.5-turbo-0125",
    temperature = 0.3,
    max_tokens = 512,
    top_p = 0.9
)

# import os
# from langchain.llms import HuggingFaceHub
# from config import HUGGINGFACEHUB_API_TOKEN       
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

# llm = HuggingFaceHub(
#     repo_id="HuggingFaceH4/zephyr-7b-beta",
#     model_kwargs={"temperature": 0.3}
# )
