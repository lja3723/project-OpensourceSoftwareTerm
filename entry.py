from news_notifier import news_collector as nc
from news_notifier.kakao_api import KakaoApi
import time


def main():
    kakao_api = KakaoApi()
    # kakao_api.login()
    # kakao_api.refresh_token()
    kakao_api.send_message()
    # kakao_api.logout()


if __name__ == "__main__":
    main()  # Call the main function
