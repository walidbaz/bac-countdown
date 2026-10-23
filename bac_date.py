#!/usr/bin/env python3
import sys
import tty
import termios
import select
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import arabic_reshaper
from bidi.algorithm import get_display

URL = https://www.bac-story.com/tools/countdown"

arabic_to_english_month = {
    "جانفي": "January", "فيفري": "February", "مارس": "March",
    "أفريل": "April", "ماي": "May", "جوان": "June",
    "جويلية": "July", "أوت": "August", "سبتمبر": "September",
    "أكتوبر": "October", "نوفمبر": "November", "ديسمبر": "December"
}

SYMBOLS = {
    0: [[1,1,1], [1,0,1], [1,0,1], [1,0,1], [1,1,1]],
    1: [[0,0,1], [0,0,1], [0,0,1], [0,0,1], [0,0,1]],
    2: [[1,1,1], [0,0,1], [1,1,1], [1,0,0], [1,1,1]],
    3: [[1,1,1], [0,0,1], [1,1,1], [0,0,1], [1,1,1]],
    4: [[1,0,1], [1,0,1], [1,1,1], [0,0,1], [0,0,1]],
    5: [[1,1,1], [1,0,0], [1,1,1], [0,0,1], [1,1,1]],
    6: [[1,1,1], [1,0,0], [1,1,1], [1,0,1], [1,1,1]],
    7: [[1,1,1], [0,0,1], [0,0,1], [0,0,1], [0,0,1]],
    8: [[1,1,1], [1,0,1], [1,1,1], [1,0,1], [1,1,1]],
    9: [[1,1,1], [1,0,1], [1,1,1], [0,0,1], [1,1,1]],
}

class Term:
    @staticmethod
    def clear_screen():
        sys.stdout.write("\x1b[2J")

    @staticmethod
    def cursor_hide():
        sys.stdout.write("\x1b[?25l")

    @staticmethod
    def cursor_show():
        sys.stdout.write("\x1b[?25h")

    @staticmethod
    def cursor_move(row, col):
        sys.stdout.write(f"\x1b[{row};{col}H")

    @staticmethod
    def rgb_fg(r, g, b, text):
        return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

    @staticmethod
    def get_size():
        import shutil
        size = shutil.get_terminal_size((80, 24))
        return size.columns, size.lines

def get_bac_date():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
        r = requests.get(URL, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        main_content = soup.find(id="post-body") or soup.find(class_="post-body") or soup
        text = main_content.get_text()

        months_pattern = "|".join(arabic_to_english_month.keys())
        match = re.search(rf"(\d{{1,2}})\s+({months_pattern})", text)
        if not match: return None

        day, month_ar = match.groups()
        month_en = arabic_to_english_month.get(month_ar)
        now = datetime.now()
        bac_date = datetime.strptime(f"{day} {month_en} {now.year}", "%d %B %Y").replace(hour=8, minute=0, second=0)

        if bac_date < now:
            bac_date = bac_date.replace(year=now.year + 1)
        return bac_date
    except Exception:
        now = datetime.now()
        return datetime(now.year, 6, 7, 8, 0)

def build_clock_matrix(digits, block_w, block_h):
    fill_char = "█"
    output_rows = ["", "", "", "", ""]

    sequence = [
        ('num', digits[0]), ('num', digits[1]), ('num', digits[2]), ('space', 1),
        ('colon', None),
        ('space', 1), ('num', digits[3]), ('num', digits[4]), ('space', 1),
        ('colon', None),
        ('space', 1), ('num', digits[5]), ('num', digits[6]), ('space', 1),
        ('colon', None),
        ('space', 1), ('num', digits[7]), ('num', digits[8])
    ]

    for r_idx in range(5):
        row_str = ""
        for item_type, val in sequence:
            if item_type == 'num':
                for pixel in SYMBOLS[val][r_idx]:
                    row_str += (fill_char * block_w) if pixel == 1 else (" " * block_w)
                row_str += " " * block_w
            elif item_type == 'space':
                row_str += " " * (block_w * val)
            elif item_type == 'colon':
                row_str += (fill_char * block_w) if r_idx in (1, 3) else (" " * block_w)
        output_rows[r_idx] = row_str

    final_matrix = []
    for row in output_rows:
        for _ in range(block_h):
            final_matrix.append(row)
    return final_matrix

def fix_arabic_text(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def main():
    bac_date = get_bac_date()
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setraw(sys.stdin.fileno())
        Term.cursor_hide()
        Term.clear_screen()

        while True:
            if select.select([sys.stdin], [], [], 0.0)[0]:
                char = sys.stdin.read(1)
                if char in ('q', 'Q', '\x03'):
                    break

            now = datetime.now()
            diff = bac_date - now
            total_seconds = int(diff.total_seconds())

            if total_seconds < 0:
                Term.clear_screen()
                Term.cursor_move(10, 10)
                print(Term.rgb_fg(46, 204, 113, fix_arabic_text("🎓 بدأت فترة امتحانات البكالوريا! بالتوفيق! 🎓")))
                break

            d = min(999, total_seconds // 86400)
            h = (total_seconds % 86400) // 3600
            m = (total_seconds % 3600) // 60
            s = total_seconds % 60

            digits = [d//100, (d%100)//10, d%10, h//10, h%10, m//10, m%10, s//10, s%10]

            width, height = Term.get_size()

            block_w = max(1, width // 48)
            block_h = max(1, block_w // 2)

            matrix_rows = build_clock_matrix(digits, block_w, block_h)
            matrix_width = len(matrix_rows[0])
            matrix_height = len(matrix_rows)

            start_col = max(1, (width - matrix_width) // 2)
            start_row = max(1, (height - matrix_height) // 2 - 2)

            Term.clear_screen()

            for idx, row in enumerate(matrix_rows):
                Term.cursor_move(start_row + idx, start_col)
                sys.stdout.write(Term.rgb_fg(224, 224, 227, row))

            label_row = start_row + matrix_height + 1

            triple_digit_width = 11 * block_w
            double_digit_width = 7 * block_w
            separator_width = 3 * block_w

            subtitles = ["يوم", "ساعة", "دقيقة", "ثانية"]

            for i, text in enumerate(subtitles):
                if i == 0:
                    group_center = start_col + (triple_digit_width // 2)
                else:
                    group_offset = triple_digit_width + separator_width + ((i - 1) * (double_digit_width + separator_width))
                    group_center = start_col + group_offset + (double_digit_width // 2)

                fixed_word = fix_arabic_text(text)
                word_col = max(1, group_center - (len(text) // 2))

                Term.cursor_move(label_row, word_col)
                sys.stdout.write(Term.rgb_fg(176, 176, 181, fixed_word))

            banner_row = label_row + 2
            date_str = f"🎓 BAC Target Date: {bac_date.strftime('%d %B %Y')} 🎓"
            Term.cursor_move(banner_row, max(1, (width - len(date_str)) // 2))
            sys.stdout.write(Term.rgb_fg(245, 245, 247, date_str))

            footer_str = f"BAC countdown | Matrix Block: {block_w}x{block_h} | Press 'q' to quit"
            Term.cursor_move(height - 1, max(1, (width - len(footer_str)) // 2))
            sys.stdout.write(Term.rgb_fg(112, 112, 117, footer_str))

            sys.stdout.flush()
            time.sleep(1)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        Term.cursor_show()
        Term.clear_screen()
        Term.cursor_move(1, 1)

if __name__ == "__main__":
    main()
