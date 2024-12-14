from schedule import repeat, every, run_pending
import time
import threading
import news_notifier

newsAiService = news_notifier.NewsAIService()
newsCollector = news_notifier.NewsCollector()
kakaoApi = news_notifier.KakaoApi()


# 매 18시간마다 토큰 갱신
@repeat(every(18).hours)
def refresh_token_scheduler():
    kakaoApi.refresh_token()


# 매일 18:00에 뉴스 알림
@repeat(every().day.at("18:00"))
def news_notify_scheduler():
    # 기사 수집
    articles = newsCollector.collect_articles(sources=["bbc-news", "cnn"])

    for article in articles:
        summary = summary_news(article["article"], article["url"])

    kakaoApi.send_message()

    # AI 서비스 호출
    # for article in articles:
    #     result = newsAiService.process_news(article["article"])


def summary_news(article: str, url: str):
    result = newsAiService.process_news(article)
    from news_notifier.utils import JsonBeautifier

    JsonBeautifier.printPretty(result)

    return f"""
        [ 원문 ]
        { result["data"]["translation"]["original"] }
        링크: { url }

        [ 번역 ]
        { result["data"]["translation"]["korean"] }

        [ 요약 ]
        { result["data"]["summary"]["korean"] }

        [ 어휘 ]
        { get_vocabulary_list(result) }
    """


def get_vocabulary_list(result):
    voca = ""
    for word_item in result["data"]["vocabulary"]:
        voca += f"""
        영단어: {word_item['word']}
        의미: {word_item['meaning']}
        예문: {word_item['example']}
        """
    return voca


def main():
    # 초기 로그인
    kakaoApi.login()

    news_notify_scheduler()

    print("스케줄러가 시작되었습니다. 종료하려면 Ctrl+C를 누르세요.")
    while True:
        run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()  # Call the main function
