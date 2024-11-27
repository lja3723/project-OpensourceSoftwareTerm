from dotenv import load_dotenv
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI()

llm.invoke("Hello, world!")


class News_AI_service_call:

    def __init__(self):
        #Set Langchain
        self.llm = ChatOpenAI()

