# daily-news

Penguin 每日報報的網頁版（GitHub Pages）。

**產生任何頁面前，請先讀 [STYLE.md](STYLE.md) 並照做**：「晨間電訊」風格、全部行內 CSS、Top N 方格卡片（有原文圖片就附圖）。

## 發佈方式

每天的新聞內容不再寄 email，改成直接發佈在 GitHub Pages：<https://penguin-yeh.github.io/daily-news/>

1. 當天內容整理成 `YYYY-MM-DD.html`（風格見 `STYLE.md`），再複製成 `index.html`（永遠是最新一天）。
2. commit 並 push 到 `main`（GitHub Pages 是 legacy 模式，從 main 根目錄直接部署，push 後會自動重新發布）。
3. 若產生頁面的 session 只能 push 到 `claude/*` 分支，`.github/workflows/sync-main.yml` 會自動把最新一天同步進 `main`，不需要手動操作或寄信通知。

## 日期切換（前一天／選單／後一天）

每個日期頁面與 `index.html` 最上方都有導覽列。它由 `scripts/add_nav.py` 產生（冪等、行內 CSS）：**每次產生新頁面後必須執行 `python3 scripts/add_nav.py`**，舊頁面的「後一天」才會連到新頁面。`sync-main.yml` 也會在 push 後自動跑一次，所以即使漏跑也會補上。
