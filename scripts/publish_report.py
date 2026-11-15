#!/usr/bin/env python3
publish_report.py — 把日報存成 reports/YYYY-MM-DD.html（鏡像自 skill-rss-classifier/scripts/publish_report.py，兩邊保持一致）。

用法：
    python3 scripts/publish_report.py /tmp/digest.html --date 2026-11-15
    python3 scripts/publish_report.py --rebuild-index      # 只重建 reports/index.html
    python3 scripts/publish_report.py /tmp/digest.html --date 2026-11-15 --reports-dir /path/to/daily-news/reports
        # 發佈到另一個 repo（daily-news）的 reports/；也可用環境變數 RSS_REPORTS_DIR

規則：
- 每天一個檔案。**絕不覆蓋既有的日報**：若 reports/YYYY-MM-DD.html 已存在（同一天重跑），
  改存成 YYYY-MM-DD-2.html、-3.html…
- reports/index.html 是唯一會被重寫的檔案，列出 reports/ 底下所有日期頁面（新到舊）。
- 輸入若只是 HTML 片段（render_email.py 的輸出），會包成完整文件（含 <title> 與 viewport）。
- 輸出檔不得含 <style> 區塊（全部行內 CSS），也不得含被跳脫的標籤，否則直接報錯。
- 輸出路徑（最後一行 stdout）給呼叫端 git add 用。
"""
import argparse
import html
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = Path(os.environ.get("RSS_REPORTS_DIR") or ROOT / "reports")
NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(\d+))?\.html$")
WEEKDAYS = "一二三四五六日"

PAPER_BG, CARD_BG, INK, SOFT_INK, HAIRLINE = "#f2f0ea", "#fffdf9", "#1c1b19", "#6b6459", "#ddd8cc"
SANS = "-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Noto Serif TC',serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"


def wrap_document(body: str, date: str) -> str:
    if re.search(r"<html[\s>]", body, re.I):
        return body
    return (
        '<!DOCTYPE html>\n<html lang="zh-Hant"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>Penguin 每日報報 · {html.escape(date)}</title></head>"
        f'<body style="margin:0;background-color:{PAPER_BG}">{body}</body></html>\n'
    )


def check(doc: str) -> None:
    if re.search(r"<style[\s>]", doc, re.I):
        raise SystemExit("報告含有 <style> 區塊；全部樣式必須是行內 CSS")
    if "&lt;div" in doc or "&lt;table" in doc or "&lt;p&gt;" in doc:
        raise SystemExit("報告含有被跳脫過的 HTML 標籤（&lt;div 等），疑似內容被 escape")
    if "<a " not in doc:
        raise SystemExit("報告沒有任何連結，疑似內容不完整")


def free_name(date: str) -> Path:
    REPORTS.mkdir(exist_ok=True)
    p = REPORTS / f"{date}.html"
    n = 2
    while p.exists():
        p = REPORTS / f"{date}-{n}.html"
        n += 1
    return p


def rebuild_index() -> Path:
    REPORTS.mkdir(exist_ok=True)
    files = sorted(
        (f for f in REPORTS.iterdir() if NAME_RE.match(f.name)),
        key=lambda f: (NAME_RE.match(f.name).group(1), int(NAME_RE.match(f.name).group(2) or 1)),
        reverse=True,
    )
    rows = []
    for f in files:
        d, n = NAME_RE.match(f.name).groups()
        try:
            wd = f"（週{WEEKDAYS[datetime.strptime(d, '%Y-%m-%d').weekday()]}）"
        except ValueError:
            wd = ""
        suffix = f"　第 {n} 版" if n else ""
        rows.append(
            f'<div style="padding:10px 0;border-top:1px solid {HAIRLINE};font-family:{SANS};font-size:15px">'
            f'<a href="{f.name}" style="color:{INK};text-decoration:underline">{d}{wd}</a>'
            f'<span style="font-family:{MONO};font-size:11.5px;color:{SOFT_INK}">{suffix}</span></div>'
        )
    body = (
        f'<div style="padding:32px 12px;font-family:{SANS};background-color:{PAPER_BG}">'
        f'<div style="max-width:680px;margin:0 auto;background-color:{CARD_BG};border:1px solid {HAIRLINE}">'
        f'<div style="padding:30px 30px 20px;border-bottom:3px double {INK}">'
        f'<div style="font-family:{MONO};font-size:11px;letter-spacing:2px;color:{SOFT_INK};text-transform:uppercase">RSS FEED 主題分類與摘要</div>'
        f'<div style="font-family:{SERIF};font-size:30px;font-weight:700;color:{INK};line-height:1.2;margin-top:10px">Penguin 每日報報</div>'
        f'<div style="font-family:{MONO};font-size:12px;color:{SOFT_INK};margin-top:12px">共 {len(files)} 期，新到舊</div></div>'
        f'<div style="padding:12px 30px 24px">{"".join(rows) or "<div style=padding:20px>尚無報告</div>"}</div>'
        "</div></div>"
    )
    out = REPORTS / "index.html"
    out.write_text(wrap_document(body, "index").replace("每日報報 · index", "每日報報"), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html_file", nargs="?")
    ap.add_argument("--date", help="YYYY-MM-DD（台北時間的今天）")
    ap.add_argument("--rebuild-index", action="store_true")
    ap.add_argument("--reports-dir", help="輸出資料夾（預設 ./reports；可指向 daily-news checkout 的 reports/）")
    a = ap.parse_args()
    if a.reports_dir:
        global REPORTS
        REPORTS = Path(a.reports_dir).resolve()
    if a.rebuild_index and not a.html_file:
        print(rebuild_index())
        return
    if not a.html_file or not a.date:
        ap.error("需要 html_file 與 --date")
    datetime.strptime(a.date, "%Y-%m-%d")
    doc = wrap_document(Path(a.html_file).read_text(encoding="utf-8"), a.date)
    check(doc)
    out = free_name(a.date)
    out.write_text(doc, encoding="utf-8")
    rebuild_index()
    print(out)


if __name__ == "__main__":
    sys.exit(main())
