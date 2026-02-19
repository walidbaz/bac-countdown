#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import sys
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.text import Text
from rich.console import Group, Console

# URL of the BAC countdown page
URL = "https://eddirasa.com/العد-التنازلي-لموعد-البكالوريا/"

arabic_to_english_month = {
    "جانفي": "January", "فيفري": "February", "مارس": "March",
    "أفريل": "April", "ماي": "May", "جوان": "June",
    "جويلية": "July", "أوت": "August", "سبتمبر": "September",
    "أكتوبر": "October", "نوفمبر": "November", "ديسمبر": "December"
}

def get_bac_date():
    try:
        r = requests.get(URL, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
        months_pattern = "|".join(arabic_to_english_month.keys())
        match = re.search(rf"(\d{{1,2}})\s+({months_pattern})", text)
        if not match: return None

        day, month_ar = match.groups()
        month_en = arabic_to_english_month.get(month_ar)
        now = datetime.now()
        bac_date = datetime.strptime(f"{day} {month_en} {now.year}", "%d %B %Y").replace(hour=8, minute=0)

        if bac_date < now:
            bac_date = bac_date.replace(year=now.year + 1)
        return bac_date
    except:
        return None

def generate_dashboard(days, hours, minutes, seconds, target_date):
    def make_panel(value, label, color):
        panel_text = Text()
        panel_text.append(f"\n{value}\n", style=f"bold {color}")
        panel_text.append(f"{label}\n", style="white")
        return Panel(Align.center(panel_text), border_style=color, padding=(1, 4))

    panels = [
        make_panel(days, "يوم", "bright_yellow"),
        make_panel(f"{hours:02d}", "ساعة", "dodger_blue1"),
        make_panel(f"{minutes:02d}", "دقيقة", "green"),
        make_panel(f"{seconds:02d}", "ثانية", "bright_cyan"),
    ]

    countdown_display = Columns(panels, align="center", expand=True)
    title = Text(f"\n🎓 BAC Date: {target_date.strftime('%d %B %Y')} 🎓\n", style="bold white", justify="center")

    # Vertically center the entire group on the screen
    return Align.center(Group(title, countdown_display), vertical="middle")

# --- Execution ---
console = Console()
bac_date = get_bac_date()

if not bac_date:
    console.print("[red]Error: Could not retrieve date.[/red]")
    sys.exit(1)

try:
    # 'screen=True' makes the terminal go fullscreen and hide everything else
    with Live(console=console, screen=True, auto_refresh=False) as live:
        while True:
            now = datetime.now()
            diff = bac_date - now
            total_seconds = int(diff.total_seconds())

            if total_seconds < 0:
                live.update(Align.center(Text("\n🎓 BAC date has passed! 🎓\n", style="bold green"), vertical="middle"))
                live.refresh()
                break

            d = total_seconds // 86400
            h = (total_seconds % 86400) // 3600
            m = (total_seconds % 3600) // 60
            s = total_seconds % 60

            live.update(generate_dashboard(d, h, m, s, bac_date))
            live.refresh()
            time.sleep(1)

except KeyboardInterrupt:
    pass # Exits cleanly back to terminal
