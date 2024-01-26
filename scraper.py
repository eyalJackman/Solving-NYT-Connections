from bs4 import BeautifulSoup
import requests
import re
from itertools import product
import json
import numpy as np
import pandas as pd


URL = (
    lambda month, day, year: f"https://connectionsanswers.com/nyt-connections-{month}-{day}-{year}-answers/"
)

months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "decemeber",
]
days = range(1, 32)
years = ["2023", "2024"]


json_data = []
for page in product(months, days, years):
    month, day, year = page
    page = requests.get(URL(*page))
    try:
        page.raise_for_status()
    except Exception as exc:
        continue
    else:
        soup = BeautifulSoup(page.content, "html.parser")
        entries = soup.find("div", class_="entry-content")

        # Tag format, i.e. <p>...</p>
        groups = entries.find_all("p", class_="has-background")

        # List format, i.e. ["{GROUP} - Level 1, {GROUP} - Level 2, ..."]
        groups = [group.text.strip().split(" – ")[0] for group in groups]

        group_words = []
        word_lists = entries.find_all("ul")
        for word_list in word_lists:
            group_words.append([word.text.strip() for word in word_list.find_all("li")])
        connection = [
            [group, group_words] for group, group_words in zip(groups, group_words)
        ]
        connection.append(f"{month} {day}, {year}")
        json_data.append(connection)

json_str = json.dumps(json_data)
with open("connections_data.json", "w") as f:
    f.write(json_str)
