import requests
from bs4 import BeautifulSoup


URL = "https://drexeldragons.com/sports/womens-basketball/stats/2021-22"

MISSING_NAMES = {
    "RPG": "Rebounds",
    "APG": "Assists",
    "TO/G": "Turnovers",
    "STL/G": "Steals",
    "BLK/G": "Blocks",
    "AVG": "Attendance",
}


def get_stats_for_team(site: str) -> dict:
    r = requests.get(site)
    soup = BeautifulSoup(r.text, features="html.parser")

    def float_or_original(value: str):
        try:
            return float(value)
        except ValueError:
            return value

    team_stats = []
    table = soup.find("table", {"class": "sidearm-table"})
    for row in table.find_all("tr")[1:]:
        children = [x for x in list(row.children) if x != "\n"]
        if len(children) == 3:
            stat = [x for x in children[0].text.split("\n") if x != ""]
            if "Margin" in stat:
                continue
            value = float_or_original(children[1].text)
            if len(stat) == 2:
                team_stats.append({"full": stat[0], "short": stat[1], "value": value})
            else:
                team_stats.append({"full": stat[0], "short": "", "value": value})

    for idx, stat in enumerate(team_stats):
        if stat["full"] == "Total":
            next_stat = team_stats[idx + 1]
            short_name = next_stat["short"]
            found = MISSING_NAMES[short_name]

            stat["full"] = found
            next_stat["full"] = f"{found} Per Game"

    ind_table = soup.find_all("table", {"class": "sidearm-table"})[1]

    player_stats = []
    for row in ind_table.find_all("tr")[2:-2]:
        name = row.find("a").text
        num = row.find_all("td")[0].text.lstrip("0")
        stats = {}
        for stat in row.find_all("td")[1:-1]:
            stat_name = stat["data-label"]
            stats[stat_name] = float(stat.text)
        player_stats.append({"name": name, "num": num, "stats": stats})

    return {"team": team_stats, "individual": player_stats}
