#!/usr/bin/env python3
"""format_comparison.py — 把「新舊比較」框從一整段擠在一起，改成條列式（先前／新在哪／解決了什麼 各一行）。

用法：
    python3 scripts/format_comparison.py              # 處理 repo 根目錄的 20*.html 與 index.html
    python3 scripts/format_comparison.py reports      # 處理指定資料夾

冪等：已經是條列式（框內有 <ul>）的會略過。只改「新舊比較」框內部，其他內容不動。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOX = re.compile(r'(<div style="background-color:#f6ecd9[^>]*>)(.*?)(</div>)', re.S)
LABELS = ("先前：", "新在哪：", "解決了什麼：")
HEAD = re.compile(r'^\s*<strong style="color:#[0-9a-fA-F]{6}">新舊比較：</strong>', re.S)


def convert(inner: str):
    if "<ul" in inner or not HEAD.match(inner):
        return None
    head = HEAD.match(inner).group(0).strip()
    rest = inner[HEAD.match(inner).end():]
    parts = re.split(r"<strong>(先前：|新在哪：|解決了什麼：)</strong>", rest)
    # parts = [前導, label1, text1, label2, text2, ...]
    items = []
    for label, text in zip(parts[1::2], parts[2::2]):
        text = text.strip().strip("　").strip()
        if text:
            items.append(f'<li style="margin:2px 0"><strong>{label}</strong>{text}</li>')
    if not items:
        return None
    return f'{head}<ul style="margin:6px 0 0;padding-left:18px">{"".join(items)}</ul>'


# 舊式合集頁：「新舊比較：…」直接接在摘要文字後面（沒有獨立的框）。
INLINE = re.compile(r">([^<>]*?)新舊比較：([^<>]*)(?=<)")


def convert_inline(m):
    intro, body = m.group(1), m.group(2)
    # 比較內容到第一個「。」為止；後面（例如「RSS 報評語：」）原樣保留在列表之後
    cut = body.find("。")
    comp, rest = (body[: cut + 1], body[cut + 1:]) if cut >= 0 else (body, "")
    parts = [x.strip().rstrip("。").strip() for x in comp.split("；") if x.strip()]
    if len(parts) < 2:
        return None
    labels = ["先前：", "新在哪："] + ["補充："] * (len(parts) - 2)
    lis = "".join(f'<li style="margin:2px 0"><strong>{l}</strong>{t}</li>' for l, t in zip(labels, parts))
    return (f'>{intro}<br><strong>新舊比較：</strong><ul style="margin:6px 0 6px;padding-left:18px">{lis}</ul>{rest}')


def process(path: Path) -> int:
    s = path.read_text(encoding="utf-8")
    count = 0

    def repl_inline(m):
        nonlocal count
        new = convert_inline(m)
        if new is None:
            return m.group(0)
        count += 1
        return new

    s = INLINE.sub(repl_inline, s)

    def repl(m):
        nonlocal count
        new = convert(m.group(2))
        if new is None:
            return m.group(0)
        count += 1
        return m.group(1) + new + m.group(3)

    out = BOX.sub(repl, s)
    if count:
        path.write_text(out, encoding="utf-8")
    return count


def main() -> None:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    target = target if target.is_absolute() else ROOT / target
    files = sorted(target.glob("20*.html")) + ([target / "index.html"] if (target / "index.html").exists() else [])
    total = 0
    for f in files:
        n = process(f)
        if n:
            print(f"{f.name}: {n}")
        total += n
    print(f"converted {total} box(es)")


if __name__ == "__main__":
    main()
