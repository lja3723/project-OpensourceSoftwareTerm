from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

llm = ChatOpenAI()



class News_AI_service_call:

    def __init__(self):
        #load dotenv
        load_dotenv()

        #Set Langchain
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=os.getenv("MODEL_NAME", "gpt-4o-mini")
        )

        # Define prompts
        self.translation_summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional translator and summarizer. 
                    Given an English news article, you will:
                    1. Translate it into Korean
                    2. Create a concise summary in Korean

                    Format your response exactly as follows:
                    === 번역 ===
                    [전체 번역문]

                    === 요약 ===
                    [3줄 이내의 요약문]"""),
            ("human", "{news_text}")
        ])