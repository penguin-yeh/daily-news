# daily-news

Penguin 每日報報的網頁版（GitHub Pages）。

**產生任何頁面前，請先讀 [STYLE.md](STYLE.md) 並照做**：「晨間電訊」風格、全部行內 CSS、Top N 方格卡片（有原文圖片就附圖）。

## 發佈方式

每天的新聞內容不再寄 email，改成直接發佈在 GitHub Pages：<https://penguin-yeh.github.io/daily-news/>

1. 當天內容整理成 `YYYY-MM-DD.html`（風格見 `STYLE.md`），再複製成 `index.html`（永遠是最新一天）。
2. commit 並 push 到 `main`（GitHub Pages 是 legacy 模式，從 main 根目錄直接部署，push 後會自動重新發布）。
3. 若產生頁面的 session 只能 push 到 `claude/*` 分支，`.github/workflows/sync-main.yml` 會自動把最新一天同步進 `main`，不需要手動操作或寄信通知。
