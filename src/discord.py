import discord
from os.path import exists
import requests

client = discord.Client(intents=discord.Intents.all(), self_bot=True)


def scrape_users(token: str, limit: int, channel_id: int):
    authors = {}
    cleaned = []

    @client.event
    async def on_ready():
        try:
            if not exists("scraped.txt"):
                open("scraped.txt", "w").close()
            else:
                with open("scraped.txt", "w") as f:
                    f.truncate(0)
            print(f"connected to discord.py from {client.user}")
            channel = client.get_channel(int(channel_id))
            async for msg in channel.history(limit=int(limit)):
                if not msg.author.id in authors:
                    authors[msg.author.id] = msg.id

            messages = list(authors.values())
            for message in messages:
                cleaned.append(str(message))
            print(f"scraped {len(messages)} message authors")
            with open("scraped.txt", "w") as f:
                f.write("\n".join(cleaned))
            await client.close()
        except Exception as e:
            print({"error": e})

    client.run(token, bot=False)


def guild_checker(guild_id: str, tokens: list):
    in_guild = []

    for token in tokens:
        try:
            headers = {"Authorization": token}
            response = requests.get(
                f"https://discord.com/api/v10/guilds/{guild_id}",
                headers=headers,
            )
            match response.status_code:
                case 200:
                    in_guild.append(token)
                    break
        except Exception as e:
            print({"error": e})
            break
    if not in_guild:
        input({"error": "no tokens in guild"})
        return
    return in_guild[0]


def enable_bot(tokens: list, limit: int, guild_id: str, channel_id: str):
    try:
        token = guild_checker(guild_id, tokens)
        if not token:
            return
        scrape_users(token, limit, channel_id)
        while not exists("scraped.txt"):
            continue
    except Exception as e:
        print({"error": e})
        input()

