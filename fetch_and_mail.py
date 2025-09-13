import os
import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

SENDER = "blakewkz@gmail.com"  # 发件人邮箱
RECEIVER = "blakewkz@gmail.com"  # 收件人邮箱
SUBJECT = " 比赛时间更新"
TEAMS = {
    "Dota2": ["Xtreme_Gaming", "Team_Tidebound"],
    "CS2": ["Lynn_Vision_Gaming", "TYLOO", "The_MongolZ", "Team_Spirit"]
} 
GAME_TO_URL = {"Dota2":"dota2", "CS2": "counterstrike"}

games = []
dates = []

def fetch_match_time(game_category, url):
    global games, dates
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    node = soup 
    node = node.find("div", class_="fo-nttax-infobox panel")
    if not node:
        return
    nodes = node.find_all("table", class_="wikitable wikitable-striped infobox_matches_content")

    for node in nodes:
        left_team = node.find("td", class_="team-left").get_text(strip=True)
        right_team = node.find("td", class_="team-right").get_text(strip=True)
        time = node.find("span", class_="timer-object timer-object-countdown-only")["data-timestamp"]
        utc_dt = datetime.fromtimestamp(int(time), tz=timezone.utc).astimezone(ZoneInfo("Australia/Sydney"))
        games.append(f"{game_category} - {left_team} vs {right_team}")
        dates.append(utc_dt)

def get_all_match_times():
    global games, dates
    for game_category, teams in TEAMS.items():
        game_url = f"https://liquipedia.net/{GAME_TO_URL[game_category]}/"
        for team in teams:
            fetch_match_time(game_category, f"{game_url}{team}")
    
    # Pair and sort by date
    sorted_games = [(game, date) for (date, game) in sorted(zip(dates, games), key=lambda x: x[0])]
    
    # Get current time with same tzinfo as your dates
    now = datetime.now(sorted_games[0][1].tzinfo) if sorted_games else datetime.now()
    
    # Filter only future matches
    upcoming_games = [(game, date) for game, date in sorted_games if date > now]
    
    # Build message
    message = ""
    for game, date in upcoming_games:
        message += f"{game}: {date.strftime('%A, %Y-%m-%d %H:%M %Z')}\n\n"
    
    return message


def send_email(message):
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    msg["Subject"] = datetime.now().strftime("%Y-%m-%d") + SUBJECT

    body = message
    msg.attach(MIMEText(body, "plain", "utf-8"))

    email_password = os.getenv("EMAIL_PASSWORD")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER, email_password)
        server.sendmail(SENDER, RECEIVER, msg.as_string())

if __name__ == "__main__":
    message = get_all_match_times()
    send_email(message)
