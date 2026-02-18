#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import os

URL = "https://eddirasa.com/العد-التنازلي-لموعد-البكالوريا/"

arabic_to_english_month = {
    "جانفي": "January",
    "فيفري": "February",
    "مارس": "March",
    "أفريل": "April",
    "ماي": "May",
    "جوان": "June",
    "جويلية": "July",
    "أوت": "August",
    "سبتمبر": "September",
    "أكتوبر": "October",
    "نوفمبر": "November",
    "ديسمبر": "December"
}

r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")
text = soup.get_text()

months_pattern = "|".join(arabic_to_english_month.keys())
match = re.search(rf"(\d{{1,2}})\s+({months_pattern})", text)
if not match:
    print("Could not detect BAC date from page.")
    exit(1)

day, month_ar = match.groups()
month_en = arabic_to_english_month.get(month_ar)

if not month_en:
    print(f"Unknown month: {month_ar}")
    exit(1)

now = datetime.now()


bac_hour = 8
bac_minute = 0

bac_date = datetime.strptime(f"{day} {month_en} {now.year}", "%d %B %Y")
bac_date = bac_date.replace(hour=bac_hour, minute=bac_minute)

if bac_date < now:
    bac_date = bac_date.replace(year=now.year + 1)

try:
    while True:
        now = datetime.now()
        diff = bac_date - now
        total_seconds = int(diff.total_seconds())

        if total_seconds < 0:
            print("🎓 BAC date has passed!")
            break

        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"🎓 BAC Date: {bac_date.strftime('%d %B %Y %H:%M')}")
        print(f"⏳ Countdown: {days} days, {hours:02} hours, {minutes:02} minutes, {seconds:02} seconds")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nCountdown stopped by user.")
