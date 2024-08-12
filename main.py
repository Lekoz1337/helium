from os import path, makedirs
from src.menu import main

folders = ["data", "scraped"]
for folder in folders:
    makedirs(folder, exist_ok=True)

files = ["data/tokens.txt", "data/proxies.txt"]
for file in files:
    if not path.exists(file):
        open(file, "a").close()

if __name__ == "__main__":
    main()