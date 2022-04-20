# %%
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from showrunner.models import Conference, School

# %%
URL = "https://usteamcolors.com/colonial-athletic-association/"

# %%
r = requests.get(URL)
soup = BeautifulSoup(r.text)

# %%
title = soup.find("div", {"class": "us-teams"}).find("h1")
conf_name = title.text.rstrip(" Colors")

conf = Conference(name=conf_name)
conf.save()

# %%
teams = soup.find_all("a", {"class": "card-image"})
urls = [x["href"] for x in teams]

# %%
pages = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
for team_url in urls:
    print(team_url)
    r = requests.get(team_url, headers=headers)
    if r.status_code == 200:
        tsoup = BeautifulSoup(r.text)
        pages.append(tsoup)
        time.sleep(2)

# %%
for page in pages:
    orig_title: str = page.find("h1", {"class": "title"}).text.replace(" Colors", "")
    school_name = orig_title.replace("College", "").replace(" of ", "").replace("University", "").replace("-", " ").replace(" and ", " & ").replace("  ", " ").strip()

    subtitle: str = page.find("h2").text.replace(" color codes: RGB, CMYK, Pantone, Hex", "")
    team_name = subtitle.replace(orig_title, "").replace(school_name, "").replace(" and ", " & ").strip()

    for word in school_name.split():
        team_name = team_name.replace(f"{word}", "").strip()

    container = page.find("div", {"class": "colors"})
    tables = container.find_all("table")
    primary = tables[0].find_all("td")[1].text
    if len(tables) > 1:
        secondary = tables[1].find_all("td")[1].text
    else:
        secondary = None

    logo = page.find("img", {"class": "team-logo"})["src"]
    img_tmp = NamedTemporaryFile(delete=True)
    with urlopen(logo) as uo:
        img_tmp.write(uo.read())
        img_tmp.flush()
    img = File(img_tmp)

    team = School(school_name=school_name, team_name=team_name, conference=conf, primary_color=primary, secondary_color=secondary)
    fname = f"{school_name}{team_name}.png"
    team.logo.save(fname, img)
    team.save()

    print(school_name, "-", team_name, primary, secondary)

# %%



