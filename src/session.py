from requests import get, exceptions
from tls_client import Session
from json import dump, load
from random import choice
from time import sleep
from os import path

if not path.exists("config.json"):
    json_data = {"proxies": False}
    with open("config.json", "w") as f:
        dump(json_data, f, indent=4)

with open("config.json", "r", encoding="utf-8") as f:
    info = load(f)
support = info.get("proxies", {})


class Data:
    def __init__(self, proxy=None) -> None:
        with open("data/proxies.txt", "r", encoding="utf-8") as f:
            self.proxies = f.read().splitlines()
        self.enabled = proxy

        self.headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US,pl;q=0.9",
            "referer": "https://discord.com/channels/@me/1196084008010928178",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9035 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Europe/Paris",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTUyIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTUyIENocm9tZS8xMjQuMC42MzY3LjI0MyBFbGVjdHJvbi8zMC4xLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjMwLjEuMCIsImNsaWVudF9idWlsZF9udW1iZXIiOjMwNjIwOCwibmF0aXZlX2J1aWxkX251bWJlciI6NDkwNTcsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0=",
        }

        self.headers_poll = {
            "accept": "*/*",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "pl",
            "x-discord-timezone": "Europe/Warsaw",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI0LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vZGlzY29yZC5jb20vIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiZGlzY29yZC5jb20iLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyODYzNDksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0=",
            "Referer": "https://discord.com/channels/@me/1221800749919371334",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

    @classmethod
    def fingerprint(cls):
        while True:
            try:
                response = (
                    get("http://discord.com/api/v9/experiments")
                    .json()
                    .get("fingerprint", {})
                )
                return response
            except exceptions.ConnectionError:
                sleep(5)
            except Exception as e:
                print(f"{e} (get_discord_cookies)")
                break

    def cookies(self):
        while True:
            try:
                response = get("https://discord.com", headers=self.headers).cookies
                return response.get_dict()
            except exceptions.ConnectionError:
                sleep(5)
            except Exception as e:
                print(f"{e} (get_discord_cookies)")
                break

    def build_session(self):
        cookies = self.cookies()
        session = Session("chrome120", random_tls_extension_order=True)
        session.cookies.update(cookies)
        if self.enabled:
            proxy = choice(self.proxies)
            session.proxies.update({"http": proxy, "https": proxy})
        return session
