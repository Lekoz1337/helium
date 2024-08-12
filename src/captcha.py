from .console import log, C
from requests import post
from time import sleep


class CapMonster:
    def __init__(self, client_key: str) -> None:
        self.key = client_key

    def get_task_id(self, invite: str, data: str):
        url = "https://api.capmonster.cloud/createTask"
        json_data = {
            "clientKey": self.key,
            "task": {
                "type": "HCaptchaTaskProxyless",
                "websiteURL": f"https://discord.com/invite/{invite}",
                "websiteKey": "e2f713c5-b5ce-41d0-b65f-29823df542cf",
                "data": data,
                "userAgent": "Discord-Android/126021",
            },
        }
        response = post(url, json=json_data)
        return response.json().get("taskId")

    def get_captcha_response(self, invite: str, data: str):
        taskId = self.get_task_id(invite, data)
        if not taskId:
            print("no task id detected")
            return

        url = "https://api.capmonster.cloud/getTaskResult"
        json_data = {
            "clientKey": self.key,
            "taskId": int(taskId),
        }
        while True:
            response = post(url, json=json_data)
            if response.json().get("solution"):
                print("solved")
                return response.json()["solution"]["gRecaptchaResponse"]