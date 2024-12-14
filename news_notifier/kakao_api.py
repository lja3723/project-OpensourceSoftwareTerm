
import os
import webbrowser
import threading
import signal
import time
import requests
import json
from flask import Flask, request
from dotenv import load_dotenv


"""
kakao_api = KakaoApi()

# 로그인 (사용자 인증 및 토큰 저장)
kakao_api.login()

# 토큰 갱신 (refresh token을 사용하여 access token 갱신)
kakao_api.refresh_token()

# 로그아웃 (카카오 로그아웃 및 토큰 파일 삭제)
kakao_api.logout()

# 메시지 전송 (카카오톡 메시지 전송)
kakao_api.send_message("보낼 메시지 내용")
"""


class KakaoApi:
    def __init__(self):
        load_dotenv(verbose=True)
        self.rest_api_key = os.getenv('KAKAO_REST_API_KEY')
        self.redirect_full_uri = os.getenv('KAKAO_REDIRECT_FULL_URI')
        self.redirect_uri = os.getenv('KAKAO_REDIRECT_URI')
        self.token_save_filename = 'token.json'

    def __load_tokens(self) -> tuple[str, str]:
        try:
            with open(self.token_save_filename, 'r') as token_file:
                tokens = json.load(token_file)
                return tokens.get('refresh_token'), tokens.get('access_token')
        except FileNotFoundError:
            return None, None

    def __save_tokens_from(self, response: dict):
        old_refresh_token, old_access_token = self.__load_tokens()
        access_token, refresh_token = response.get('access_token'), response.get('refresh_token')

        with open(self.token_save_filename, 'w') as token_file:
            json.dump({
                'access_token': access_token if access_token is not None else old_access_token,
                'refresh_token': refresh_token if refresh_token is not None else old_refresh_token
            }, token_file, indent=4)

    def __get_access_token(self) -> str:
        _, access_token = self.__load_tokens()
        if not access_token:
            raise ValueError("access_token이 존재하지 않습니다. 재로그인이 필요합니다.")
        return access_token

    def __get_refresh_token(self) -> str:
        refresh_token, _ = self.__load_tokens()
        if not refresh_token:
            raise ValueError("refresh_token이 존재하지 않습니다. 재로그인이 필요합니다.")
        return refresh_token

    def __valid_json_response(self, response) -> dict:
        if not 200 <= response.status_code < 400:
            from .utils import JsonBeautifier
            JsonBeautifier.printPretty(response.json())
            response.raise_for_status()
        else:
            return response.json()

    ##############################################################################################################

    def login(self):
        # authorization code 요청
        url = "https://kauth.kakao.com/oauth/authorize?" \
            + "response_type=code&client_id=" + self.rest_api_key \
            + "&redirect_uri=" + self.redirect_full_uri \
            + "&scope=talk_message"
        print("login url: ", url)
        webbrowser.open(url)

        class RedirectProcessServer:
            def __init__(self):
                load_dotenv(verbose=True)
                self.app = Flask(__name__)
                self.redirect_uri = os.getenv('KAKAO_REDIRECT_URI')
                self.host = os.getenv("REDIRECT_PROCESS_SERVER_HOST")
                self.port = os.getenv("REDIRECT_PROCESS_SERVER_PORT")
                self.code = None

                # setup route
                @self.app.route(self.redirect_uri)
                def handle_request():
                    self.code = request.args.get('code')
                    threading.Thread(target=self.__shutdown_server).start()
                    return "카카오 로그인에 성공하였습니다. 본 페이지를 닫아주세요.", 200

            def __shutdown_server(self):
                time.sleep(1)
                os.kill(os.getpid(), signal.SIGINT)

            def get_code(self):
                self.app.run(host=self.host, port=self.port)
                return self.code

        code = RedirectProcessServer().get_code()

        # authorization code로 access token & refresh token 요청
        response = self.__valid_json_response(requests.post(
            url="https://kauth.kakao.com/oauth/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
            },
            data={
                "grant_type": "authorization_code",
                "client_id": self.rest_api_key,
                "redirect_uri": self.redirect_full_uri,
                "code": code
            }))
        self.__save_tokens_from(response)

    def refresh_token(self):
        response = self.__valid_json_response(requests.post(
            url="https://kauth.kakao.com/oauth/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
            },
            data={
                "grant_type": "refresh_token",
                "client_id": self.rest_api_key,
                "refresh_token": self.__get_refresh_token()
            }))
        self.__save_tokens_from(response)

    def logout(self):
        self.__valid_json_response(requests.post(
            url="https://kapi.kakao.com/v1/user/logout",
            headers={
                "Contnet-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f"Bearer {self.__get_access_token()}"
            }))
        os.remove(self.token_save_filename)

    def send_message(self, content: str):
        max_length = 1000
        content_list = [content[i:i + max_length] for i in range(0, len(content), max_length)]

        for split_content in content_list:
            self.__valid_json_response(requests.post(
                url="https://kapi.kakao.com/v2/api/talk/memo/default/send",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                    "Authorization": f"Bearer {self.__get_access_token()}"
                },
                data={
                    "template_object": json.dumps({
                        "object_type": "text",
                        "text": split_content,
                        "link": {"web_url": "localhost"},
                        "button_title": "본문 보러가기"
                    })
                }))
