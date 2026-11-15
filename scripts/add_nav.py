#!/usr/bin/env python3
"""add_nav.py — 幫根目錄的 YYYY-MM-DD.html 與 index.html 加上（或更新）「前一天／日期選單／後一天」導覽列。

用法：python3 scripts/add_nav.py        （在 repo 根目錄執行；冪等，可重複執行）

- 導覽列用 <!--nav-->…<!--/nav--> 標記，重跑只會替換標記內的內容，不會重複加。
- index.html 視為「最新一天」的副本：選單選到最新日期，後一天停用。
- 頁面若已自帶舊式導覽（id="sel"，舊的多日合集頁），不動它。
- 全部行內 CSS，翻頁用一般連結、日期選單用行內 onchange（不需要 <script> 或外部檔）。
- 每次產生新頁面後（以及同步進 main 後）都要跑一次，讓舊頁面的「後一天」連到新頁面。
"""
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})\.html$")
WEEKDAYS = "一二三四五六日"
# 風格 token（與 STYLE.md 一致）
BG, CARD, INK, MUTE, LINE = "#f2f0ea", "#fffdf9", "#1c1b19", "#6b6459", "#ddd8cc"
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"
MAXW = "820px"
START, END = "<!--nav-->", "<!--/nav-->"


def label(d: str) -> str:
    dt = datetime.strptime(d, "%Y-%m-%d")
    return f"{dt.month}/{dt.day}（{WEEKDAYS[dt.weekday()]}）"


def link(href, text, enabled):
    base = (f"font-family:{MONO};font-size:12px;border:1px solid {LINE};border-radius:4px;"
            f"padding:6px 10px;text-decoration:none;")
    if enabled:
        return f'<a href="{href}" style="{base}color:{INK};background-color:{CARD}">{text}</a>'
    return f'<span style="{base}color:{MUTE};background-color:{CARD};opacity:.45">{text}</span>'


def nav_html(dates, current):
    i = dates.index(current)
    older = dates[i + 1] if i + 1 < len(dates) else None   # dates 為新到舊
    newer = dates[i - 1] if i > 0 else None
    opts = "".join(
        f'<option value="{d}.html"{" selected" if d == current else ""}>{label(d)}</option>' for d in dates
    )
    sel = (f'<select aria-label="選擇日期" onchange="location.href=this.value" '
           f'style="font-family:{MONO};font-size:12px;color:{INK};background-color:{CARD};'
           f'border:1px solid {LINE};border-radius:4px;padding:6px 8px;min-width:9em">{opts}</select>')
    return (
        f'{START}<nav style="max-width:{MAXW};margin:0 auto;padding:10px 12px;display:flex;gap:8px;'
        f'align-items:center;justify-content:space-between;background-color:{BG}">'
        f'{link((older or "") + ".html" if older else "", "◀ 前一天", bool(older))}{sel}'
        f'{link((newer or "") + ".html" if newer else "", "後一天 ▶", bool(newer))}</nav>{END}'
    )


def apply(path: Path, dates, current) -> bool:
    s = original = path.read_text(encoding="utf-8")
    if 'id="sel"' in s:          # 舊式合集頁，自帶導覽
        return False
    block = nav_html(dates, current)
    # 清掉標記以外、手工加過的舊導覽（<nav>…</nav>），避免出現兩條
    parts = re.split("(" + re.escape(START) + r".*?" + re.escape(END) + ")", s, flags=re.S)
    s = "".join(p if p.startswith(START) else re.sub(r"<nav\b.*?</nav>", "", p, flags=re.S) for p in parts)
    if START in s:
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, s, count=1, flags=re.S)
    else:
        m = re.search(r"<body[^>]*>", s, re.I)
        if not m:
            return False
        new = s[: m.end()] + block + s[m.end():]
    if new == original:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    dates = sorted((m.group(1) for f in ROOT.iterdir() if (m := DATED.match(f.name))), reverse=True)
    if not dates:
        print("no dated pages"); return
    changed = []
    for d in dates:
        if apply(ROOT / f"{d}.html", dates, d):
            changed.append(f"{d}.html")
    idx = ROOT / "index.html"
    if idx.exists() and apply(idx, dates, dates[0]):
        changed.append("index.html")
    print("updated:", ", ".join(changed) or "(none)")


if __name__ == "__main__":
    sys.exit(main())
