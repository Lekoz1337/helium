from os import system, get_terminal_size
from colorist import ColorHex as h
from datetime import datetime

C = {
    "green": h("#65fb07"),
    "red": h("#Fb0707"),
    "yellow": h("#FFCD00"),
    "magenta": h("#b207f5"),
    "blue": h("#00aaff"),
    "cyan": h("#aaffff"),
    "gray": h("#8a837e"),
    "white": h("#DCDCDC"),
    "pink": h("#c203fc"),
    "light_blue": h("#07f0ec"),
}


class Render:
    def __init__(self):
        self.size = get_terminal_size().columns

    def render_ascii(self):
        system("cls")
        edges = ["╗", "║", "╚", "╝", "═", "╔"]
        title = f"""
{'██╗  ██╗███████╗██╗     ██╗██╗   ██╗███╗   ███╗'.center(self.size)}
{'██║  ██║██╔════╝██║     ██║██║   ██║████╗ ████║'.center(self.size)}
{'███████║█████╗  ██║     ██║██║   ██║██╔████╔██║'.center(self.size)}
{'██╔══██║██╔══╝  ██║     ██║██║   ██║██║╚██╔╝██║'.center(self.size)}
{'██║  ██║███████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║'.center(self.size)}
{'╚═╝  ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝     ╚═╝'.center(self.size)}"""
        for edge in edges:
            title = title.replace(edge, f"{C['light_blue']}{edge}{C['white']}")
        print(title)

    def raider_options(self):
        edges = ["─", "╭", "│", "╰", "╯", "╮", "»", "«"]
        title = f"""
{'╭────────────────────────────────────────────────────────────────────────────────────────────────╮'.center(self.size)}
{'│ «01» Joiner            «06» Token Formatter    «11» Voice Joiner        «16» Call Spammer      │'.center(self.size)}
{'│ «02» Leaver            «07» Button Click       «12» Poll Spammer        «17» ???               │'.center(self.size)}
{'│ «03» Spammer           «08» Accept Rules       «13» Invite Spammer      «18» ???               │'.center(self.size)}
{'│ «04» Token Checker     «09» Guild Check        «14» Thread Spammer      «19» Onboard Bypass    │'.center(self.size)}
{'│ «05» Emoji Reaction    «10» Bio Changer        «15» ???                 «20» ???               │'.center(self.size)}
{'╰────────────────────────────────────────────────────────────────────────────────────────────────╯'.center(self.size)}
"""
        for edge in edges:
            title = title.replace(edge, f"{C['light_blue']}{edge}{C['white']}")
        print(title)

    def run(self):
        options = [self.render_ascii(), self.raider_options()]
        ([option] for option in options)


def log(text=None, color=None, token=None, log=None):
    response = f"{C['cyan']}[{datetime.now().strftime('%H:%M:%S')}]{C['white']} "
    if text:
        response += f"{color}[{text}]{C['white']} "
    if token:
        response += str(token)
    if log:
        response += f" {C['gray']}({log}){C['white']}"
    print(response)


def prompt(text, ask=None):
    response = f"[{C['light_blue']}{text.lower()}{C['white']}"
    if ask:
        response += f"? {C['gray']}(y/n){C['white']}]: "
    else:
        response += f"]: "
    return response
