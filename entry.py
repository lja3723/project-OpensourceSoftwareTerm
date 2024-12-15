from schedule import repeat, every, run_pending
import time
import news_notifier
from news_notifier import utils
import random

newsAiService = news_notifier.NewsAIService()
newsCollector = news_notifier.NewsCollector()
kakaoApi = news_notifier.KakaoApi()


# 매 18시간마다 토큰 갱신
@repeat(every(18).hours)
def refresh_token_scheduler():
    print("토큰 갱신 스케줄러가 실행됩니다.")
    kakaoApi.refresh_token()


# 매일 18:00에 뉴스 알림
@repeat(every().day.at("18:00"))
def news_notify_scheduler():
    print("뉴스 알림 스케줄러가 실행됩니다.")
    # 기사 수집 후 랜덤하게 3개의 기사 선택
    articles = newsCollector.collect_articles(sources=["bbc-news", "cnn"])
    articles = random.sample(articles, min(len(articles), 3))

    # 뉴스 가공 및 메시지 작성
    messages = ["오늘의 영어뉴스를 요약해왔어요! 원문과 번역을 확인하고 핵심 어휘도 확인해보세요 :D"]
    num_prefix = ["첫", "두", "세"]
    for i, article in enumerate(articles):
        # AI 서비스 호출
        print(f"{num_prefix[i]} 번째 뉴스 요약을 시작합니다.")
        summary = summary_news(article["article"], article["url"])
        messages.append(f"{num_prefix[i]} 번째 뉴스:{summary}")
        print(f"{num_prefix[i]} 번째 뉴스 요약이 완료되었습니다.")

    # 카카오톡을 통해 메시지 전송
    for message in messages:
        kakaoApi.send_message(message)
    print("뉴스 알림이 성공적으로 전송되었습니다.")


def summary_news(article: str, url: str):
    result = newsAiService.process_news(article)
    return utils.dedent(
        f"""
        [ 원문 링크 ]

        {url}


        [ 요약 ]

        {result["data"]["summary"]["korean"]}


        [ 핵심 어휘 ] {get_vocabulary_list(result)}


        [ 번역 ]

        {result["data"]["translation"]["korean"]}""")


def get_vocabulary_list(result):
    voca = ""
    for word_item in result["data"]["vocabulary"]:
        voca += utils.dedent(f"""

            영단어: {word_item['word']}
            의미: {word_item['meaning']}
            예문: {word_item['example']}""")
    return voca


def main():
    # 초기 로그인
    print("영신문 요약기 프로그램을 실행하였습니다. 본 프로그램은 nohup을 사용한 백그라운드 실행을 권장합니다.")
    print("초기 로그인을 위해 브라우저가 실행됩니다.", end=" ")
    input("아무 키나 누르세요...")
    kakaoApi.login()

    # 스케줄러 테스트
    print("스케줄러 등록 함수 실행 테스트를 실행합니다.")
    refresh_token_scheduler()
    news_notify_scheduler()

    print("스케줄러가 시작되었습니다. 프로그램을 종료하려면 Ctrl+C를 누르세요.")
    while True:
        run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()  # Call the main function
