import os
from urllib.request import urlopen
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from django.apps import apps
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


URL = "https://drexeldragons.com/sports/womens-basketball/roster"


def get_roster(url: str, baseurl: str, team):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    players_table = soup.find("ul", {"class": "sidearm-roster-players"})
    for player in players_table.find_all("li", {"class": "sidearm-roster-player"}):
        img = player.find("img")["data-src"]
        raw_name = player.find("div", {"class": "sidearm-roster-player-name"})
        name = raw_name.text.strip()[2:].strip()
        first_name, last_name = name.split(" ", maxsplit=1)

        number = player.find(
            "span", {"class": "sidearm-roster-player-jersey-number"}
        ).text.strip()
        position = player.find(
            "span",
            {"class": "sidearm-roster-player-position-long-short hide-on-small-down"},
        ).text.strip()
        hometown = player.find(
            "span", {"class": "sidearm-roster-player-hometown"}
        ).text.strip()
        height = player.find(
            "span", {"class": "sidearm-roster-player-height"}
        ).text.strip()
        high_school = player.find(
            "span", {"class": "sidearm-roster-player-highschool"}
        ).text.strip()

        img_url = urljoin(baseurl, img.rstrip("?width=80"))
        img_tmp = NamedTemporaryFile(delete=True)
        with urlopen(img_url) as uo:
            img_tmp.write(uo.read())
            img_tmp.flush()
        img = File(img_tmp)

        Player = apps.get_model("showrunner", "Player")

        player = Player(
            first_name=first_name,
            last_name=last_name,
            team=team,
            uniform=int(number),
            height=height,
            position=position,
            hometown=hometown,
            high_school=high_school,
        )
        fname = f"{first_name}_{last_name}_{team.school.team_name}.jpg"
        player.image.save(fname, img)
        player.save()
