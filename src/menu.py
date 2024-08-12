from .console import prompt, Render
from websocket import WebSocket
from .discord import enable_bot
from .functions import Raider
from .session import Data
from json import load
from time import sleep
import threading

with open("config.json", encoding="utf-8") as f:
    config = load(f)
proxy = config["proxies"]


class Menu:
    def __init__(self):
        self.raider = Raider(proxy)
        self.options = {
            "1": self.joiner,
            "2": self.leaver,
            "3": self.spammer,
            "4": self.checker,
            "5": self.reactor,
            "6": self.formatter,
            "7": self.button,
            "8": self.accept,
            "9": self.guild,
            "10": self.bio,
            "11": self.join_vc,
            "12": self.poll_spammer,
            "13": self.invite_spammer,
            "14": self.thread,
            "16": self.caller,
            "19": self.onboard,
        }
        with open("data/tokens.txt", "r", encoding="utf-8") as f:
            self.tokens = f.read().splitlines()

    def main_menu(self, _input=None):
        if _input:
            input()
        Render().run()
        choice = input(prompt("Choice"))
        if choice in self.options:
            Render().render_ascii()
            self.options[choice]()
        else:
            self.main_menu()

    def run(self, func, args):
        delay = input(prompt("delay"))
        if not delay:
            delay = 0
        try:
            delay = float(delay)
        except:
            delay = 0
        threads = []
        Render().render_ascii()
        for arg in args:
            sleep(delay)
            thread = threading.Thread(target=func, args=arg)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        input("\n ~/> press enter to continue ")
        self.main_menu()

    def joiner(self):
        invite = input(prompt("Invite"))
        fingerprint = Data.fingerprint()
        args = [(token, invite, fingerprint) for token in self.tokens]
        self.run(self.raider.joiner, args)

    def invite_spammer(self):
        guild_id = input(prompt("Guild ID"))

        args = [(token, guild_id) for token in self.tokens]
        self.run(self.raider.invite_spammer, args)

    def leaver(self):
        guild = input(prompt("Guild ID"))
        args = [(token, guild) for token in self.tokens]
        self.run(self.raider.leaver, args)

    def poll_spammer(self):
        channel_id = input(prompt("Channel ID"))
        message = input(prompt("Message"))

        args = [(token, channel_id, message) for token in self.tokens]
        self.run(self.raider.poll_spammer, args)

    def spammer(self):
        channel_id = input(prompt("Channel ID"))
        message = input(prompt("Message"))
        massping = input(prompt("Massping", True))

        if "y" in massping:
            bypass = input(prompt("guidelines reply abuse", True)).lower()
            guild_id = input(prompt("Guild ID"))
            if not "y" in bypass:
                count = input(prompt("Pings Amount"))
                scrape_channel = input(prompt("scrape channel id"))
                if scrape_channel == "":
                    scrape_channel = channel_id
                self.raider.member_scrape(guild_id, scrape_channel, self.tokens)
                args = [
                    (token, channel_id, message, guild_id, True, count)
                    for token in self.tokens
                ]
                self.run(self.raider.spammer, args)
            else:
                limit = input(prompt("messages limit"))
                enable_bot(self.tokens, int(limit), guild_id, channel_id)
                args = [
                    (token, channel_id, message, guild_id, False, False, True)
                    for token in self.tokens
                ]
                self.run(self.raider.spammer, args)
        else:
            args = [(token, channel_id, message) for token in self.tokens]
            self.run(self.raider.spammer, args)

    def checker(self):
        self.raider.token_checker(self.tokens)

    def reactor(self):
        message = input(prompt("Message Link"))
        flood = input(prompt("Flood Mode", True))
        if "y" in flood.lower():
            args = [(token, message) for token in self.tokens]
            self.run(self.raider.spam_reactions, args)
        else:
            self.raider.reactor_main(message, self.tokens)

    def formatter(self):
        self.raider.format_tokens(self.tokens)

    def button(self):
        message = input(prompt("Message Link"))
        bot_id = input(prompt("Bot ID"))
        Render().render_ascii()
        self.raider.button_bypass(message, self.tokens, bot_id)

    def accept(self):
        guild_id = input(prompt("Guild ID"))
        self.raider.accept_rules(guild_id, self.tokens)

    def guild(self):
        guild_id = input(prompt("Guild ID"))
        self.raider.guild_checker(guild_id, self.tokens)

    def bio(self):
        bio = input(prompt("Bio"))
        args = [(token, bio) for token in self.tokens]
        self.run(self.raider.bio_changer, args)

    def join_vc(self):
        guild_id = input(prompt("guild id"))
        channel = input(prompt("channel id"))

        args = [(token, WebSocket(), guild_id, channel) for token in self.tokens]
        self.run(self.raider.voice_spammer, args)

    def thread(self):
        channel_id = input(prompt("Channel ID"))
        message = input(prompt("Message"))
        args = [(token, channel_id, message) for token in self.tokens]
        self.run(self.raider.thread_spammer, args)

    def caller(self):
        user_id = input(prompt("User ID"))
        args = [(WebSocket(), token, user_id) for token in self.tokens]
        self.run(self.raider.call_spammer, args)

    def onboard(self):
        guild_id = input(prompt("Guild ID"))
        self.raider.onboard_bypass(guild_id, self.tokens)


def main():
    return Menu().main_menu()
