"""
사용형태
form AI_service_call import NewsAIService

news_service = NewsAIService()

english_news = "string형태 영어뉴스 입력"

result = news_service.process_news(english_news) #python dict형태로 반환

result["data"]["translation"]["korean"] #한국어 번역 전문
result["data"]["translation"]["original"] #영어 원문
result["data"]["summary"["korean"] #한국어 요약본


"""


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from typing import Dict, Any
import os


class NewsAIService:

    def __init__(self):
        #load dotenv
        load_dotenv()

        #Set Langchain
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name=os.getenv("MODEL_NAME", "gpt-4o-mini")

        )

        # 출력 스키마 설정 (모델의 출력 형태 설정)
        response_schemas = [
            ResponseSchema(name="translation", description="Full Korean translation of the news article"),
            ResponseSchema(name="summary", description="Concise Korean summary in 3 sentences or less")
        ]

        # Create output parser
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # 프롬프트 템플릿 정의
        template = """You are a professional translator and summarizer specializing in English to Korean translation.

        Please process the provided English news article as follows:
        1. Translate the entire text into natural, fluent Korean
        2. Create a concise summary in Korean (maximum 3 sentences)

        {format_instructions}

        Guidelines:
        - Translation should be natural and idiomatic Korean
        - Summary should capture the key points in 3 sentences or less
        - Maintain formal/standard Korean language level
        - Preserve accurate news tone and context

        News article to process: {news_text}"""

        self.prompt = ChatPromptTemplate.from_template(template)

    def process_news(self, news_text):
        try:
            # 포맷 지침 가져오기
            format_instructions = self.output_parser.get_format_instructions()

            # 체인 생성 및 실행
            chain = self.prompt | self.llm
            result = chain.invoke({
                "format_instructions": format_instructions,
                "news_text": news_text
            })

            # 결과 파싱(JSON형태 리턴 -> Python Dict형태)
            parsed_output = self.output_parser.parse(result.content)

            return {
                "status": "success",
                "data": {
                    "translation": {
                        "original": news_text,
                        "korean": parsed_output["translation"]
                    },
                    "summary": {
                        "korean": parsed_output["summary"]
                    }
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"처리 중 오류 발생: {str(e)}",
                "data": None
            }

#테스트코드
if __name__ == "__main__":

    api_key = os.getenv("OPENAI_API_KEY")
    print("API_KEY \n",api_key)

    test_news = """
    Apple unveils new iPhone features focused on personal safety. 
    The tech giant announced today that upcoming iPhone models will include 
    enhanced emergency response capabilities and improved location tracking 
    during crisis situations. The new features will be available this fall.
    """

    news_service = NewsAIService()
    result = news_service.process_news(test_news)

    if result["status"] == "success":
        print("\n=== 원문 ===")
        print(result["data"]["translation"]["original"])
        print("\n=== 번역 ===")
        print(result["data"]["translation"]["korean"])
        print("\n=== 요약 ===")
        print(result["data"]["summary"]["korean"])
    else:
        print("Error:", result["message"])