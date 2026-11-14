# 每日新聞頁面風格規範（「晨間電訊」）

> 給負責產生本 repo 頁面的 bot（Grok bot）：**每次產生或更新 `index.html`、`YYYY-MM-DD.html` 之前，先完整讀完這份文件，並嚴格遵守。** 風格要和每天寄出的 Gmail「Penguin 每日報報」信件一致。

## 0. 硬性規則

1. **全部使用行內 CSS**（每個元素自己帶 `style="..."`）。**不准有 `<style>` 區塊、不准引用外部 CSS／字型／icon 套件。** 頁面要能整份複製貼到 Gmail 也不跑版。
2. 品牌名是 **Penguin**（不是 Pengion）。標題格式：`Penguin 每日報報`；`<title>` 為 `Penguin 每日報報 · YYYY-MM-DD`。
3. 禁止的做法：漸層、陰影、圓角大於 10px、emoji 當裝飾（除了下面指定的 🗞️ 與 ⚠️）、`hover` 動畫、`position:sticky`。需要互動（日期切換）才可以用少量 `<script>`，且按鈕與下拉選單也要用行內樣式，配色比照本文件。
4. 頁面容器寬度上限 **680px**（見第 3 節），手機也要能讀，不可出現橫向捲軸。
5. 所有文字用繁體中文。每篇文章的連結、標題、日期必須對應原始來源，不可手抄錯位、不可編造。

## 1. 設計 token（色票與字型）

| 用途 | 值 |
|---|---|
| 頁面底色（紙外圍） | `#f2f0ea` |
| 內容紙色 | `#fffdf9` |
| 主文字／墨色 | `#1c1b19` |
| 次要文字 | `#6b6459` |
| 內文灰 | `#374151` |
| 分隔線／邊框 | `#ddd8cc` |
| 熱度／重點金 | `#9c6b12`（深：`#7a5209`） |
| 新舊比較底 | `#f6ecd9` |
| 評語底 | `#f5f3ff`（標籤色 `#5b21b6`） |
| 小額外閱讀底 | `#f7f5ef` |

**領域「郵戳色」輪替**（第 1、2、3… 個領域依序取色，用完從頭循環；只套用在三個地方：領域標籤底色、Top N 的編號、領域區塊上緣粗線）：

`#b3402f`（磚紅）→ `#2c5f7c`（藍）→ `#5b4a8a`（紫）→ `#5c6b3f`（橄欖）→ `#8a6d1f`（土黃）

字型（原樣照抄，不要換）：

- 無襯線內文：`-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif`
- 襯線標題與領域導言：`Georgia,'Noto Serif TC',serif`
- 等寬（標籤、日期、數字、熱度）：`ui-monospace,SFMono-Regular,Consolas,monospace`

## 2. 版面由上到下的順序

1. 外層紙（第 3 節）
2. **報頭**
3. 「已排除內容」小框（沒有就整塊省略）
4. 「⚠️ 抓取失敗」小框（沒有失敗來源就整塊省略）
5. **領域區塊**，依序重複。軟體工程／程式相關的領域永遠放第一，且摘要寫得最深。
6. **來源統計**長條圖
7. **頁尾**一行統計

## 3. 各區塊的標準寫法（複製這些骨架，只換內容）

### 3.1 外層

```html
<div style="padding:32px 12px;font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;background-color:#f2f0ea">
<div style="max-width:680px;margin:0 auto;background-color:#fffdf9;border:1px solid #ddd8cc">
  …所有區塊…
</div></div>
```

### 3.2 報頭

```html
<div style="padding:30px 30px 20px 30px;border-bottom:3px double #1c1b19;background-color:#fffdf9">
  <div style="font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;letter-spacing:2px;color:#6b6459;text-transform:uppercase;margin-bottom:10px">RSS FEED 主題分類與摘要</div>
  <div style="font-family:Georgia,'Noto Serif TC',serif;font-size:30px;font-weight:700;color:#1c1b19;line-height:1.2">Penguin 每日報報</div>
  <div style="font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;color:#6b6459;margin-top:12px;line-height:1.8">
    YYYY-MM-DD（週X）台北時間 HH:MM 發行　·　統計區間：過去 24 小時（約自 前一日 HH:MM 起算）<br>
    分類依實際內容動態分群，非固定 7 類標籤；Top N 依各領域文章量比例分配；有客觀熱度數據時優先採用<br>
    Hacker News 排名為 <strong style="color:#1c1b19">YYYY-MM-DD HH:MM 台北時間（HH:MM UTC）</strong> 當下快照
  </div>
</div>
```

### 3.3 「已排除內容」與「抓取失敗」小框

兩者共用同一種外框（失敗框與排除框之間 `margin-top:14px`，第一個框 `margin-top:20px`）：

```html
<div style="border:1px solid #ddd8cc;border-radius:6px;padding:12px 16px;margin:20px 30px 0 30px;font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;font-size:12px;color:#6b6459;line-height:1.8;background-color:#fffdf9">
  <strong style="color:#1c1b19">已排除內容：</strong>…
</div>
```

失敗框內文以「⚠️ **本次共有 N 個來源抓取失敗**」開頭，每個失敗來源一行「・來源名：HTTP 狀態」。失敗不得假裝成「今天沒新聞」。

### 3.4 領域區塊

上緣粗線與標籤底色用該領域的郵戳色（下例是第 1 個領域 `#b3402f`）：

```html
<div style="padding:24px 30px;border-top:3px solid #b3402f;background-color:#fffdf9">
  <table style="border-collapse:collapse;margin:0 0 10px"><tr>
    <td style="background-color:#b3402f;border-radius:3px;padding:4px 10px"><span style="font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;color:#fff;letter-spacing:0.5px">領域名稱</span></td>
    <td style="padding:0 0 0 10px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;color:#6b6459">416 篇 → Top 10</td>
  </tr></table>
  <div style="font-family:Georgia,'Noto Serif TC',serif;font-size:14.5px;line-height:1.9;color:#1c1b19;margin:0 0 6px">領域導言（整體摘要，一段）</div>

  <!-- 3.5 Top N 方格、3.6 評語、3.7 小額外閱讀 依序放這裡 -->
</div>
```

### 3.5 Top N 文章：方格卡片（有圖就附圖）

這是版面上和舊信件不同的部分：**Top N 不再是一條一條的清單，改成方格卡片。** 卡片容器用行內 CSS grid，不需要 media query，手機會自動變單欄：

```html
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:12px 0 0">
  <!-- 每篇文章一張卡片 -->
  <div style="border:1px solid #ddd8cc;border-radius:6px;background-color:#fffdf9;overflow:hidden;display:flex;flex-direction:column">
    <!-- 有圖才放這個 <a><img>，沒有圖就整段省略，卡片從文字開始 -->
    <a href="文章網址"><img src="圖片網址" alt="文章標題" loading="lazy" style="display:block;width:100%;height:150px;object-fit:cover;border-bottom:1px solid #ddd8cc;background-color:#f7f5ef"></a>
    <div style="padding:12px 14px">
      <div style="font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;font-size:14px;line-height:1.6;margin:0 0 3px">
        <span style="font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12.5px;color:#b3402f;margin-right:6px;font-weight:700">1.</span>
        <a href="文章網址" style="color:#1c1b19;text-decoration:underline">【來源名】文章標題</a>
      </div>
      <div style="font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;color:#6b6459;margin:0 0 4px">[YYYY-MM-DD] · 來源名</div>
      <!-- 有客觀熱度數據才放這行（Hacker News 等） -->
      <div style="font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11.5px;color:#9c6b12;margin:2px 0 4px">依 Hacker News 熱度：439 讚 / 284 則留言</div>
      <div style="font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;font-size:13px;color:#374151;line-height:1.8">摘要（含為什麼重要）</div>
      <!-- 見 3.5.2：新舊比較框，適用時才放 -->
    </div>
  </div>
</div>
```

編號 `1.`、`2.`… 的顏色用該領域的郵戳色，不是固定紅色。

#### 3.5.1 圖片規則

- 圖片來源只用「該篇文章原始來源」提供的圖：RSS 的 `<enclosure>`、`<media:content>`、`<media:thumbnail>`；沒有的話，抓文章頁的 `og:image`（再退而求其次 `twitter:image`）。
- **沒有圖就不放圖**，不得拿別篇的圖、AI 生成圖、佔位圖或網站 logo 充數，也不准編造圖片網址。
- 圖片網址必須是 `https://` 且確實回得到圖片（抓取時 HTTP 200 且 `Content-Type` 為 `image/*`）；失敗就當沒有圖。
- 一律 `loading="lazy"`、`alt` 填文章標題、固定高度 150px 並 `object-fit:cover`。
- 同一個領域裡有圖與無圖的卡片並存沒關係，grid 會自己排好。

#### 3.5.2 「新舊比較」框（只有當文章是某技術、產品或規格的新版本／新做法時才放）

```html
<div style="background-color:#f6ecd9;border-left:3px solid #9c6b12;border-radius:0 6px 6px 0;padding:10px 14px;margin:8px 0 4px;font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;font-size:12.5px;color:#374151;line-height:1.8">
  <strong style="color:#7a5209">新舊比較：</strong>
  <strong>先前：</strong>…　<strong>新在哪：</strong>…　<strong>解決了什麼：</strong>…
</div>
```

資訊不足以做嚴謹比較時，照實寫「本文未提供足夠脈絡」，不要硬編。

### 3.6 評語（每個領域的最後一塊，一定要有）

```html
<div style="background-color:#f5f3ff;border-radius:10px;padding:16px 18px;margin:20px 0 18px">
  <strong style="color:#5b21b6">評語：</strong>
  <span style="color:#374151;font-size:13.5px;line-height:1.9;font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif">把該領域 Top N 並排來看的觀察、張力與判斷。</span>
</div>
```

### 3.7 🗞️ 小額外閱讀（用來讓每個來源至少出現 3 篇）

用單欄清單，不做成方格：

```html
<div style="background-color:#f7f5ef;border:1px dashed #ddd8cc;border-radius:8px;padding:12px 16px;margin:14px 0 0">
  <div style="font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;font-size:12.5px;color:#6b6459;margin:0 0 8px">🗞️ <strong style="color:#1c1b19">小額外閱讀：</strong>以下文章為滿足各來源至少 3 篇代表性的要求而列出，部分非今日文章，已標註實際日期：</div>
  <div style="font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;font-size:12.5px;color:#1c1b19;line-height:1.9">
  ・<a href="文章網址" style="color:#1c1b19;text-decoration:underline">文章標題</a> <span style="color:#6b6459">— 一句話說明（日期：YYYY-MM-DD）</span><br>
  </div>
</div>
```

### 3.8 來源統計（長條圖，用表格畫，不用圖片或 JS）

每個來源一列。填色格寬度 = 該來源篇數 ÷ 最大篇數（百分比），剩下的空白格補足 100%：

```html
<div style="padding:24px 30px;border-top:1px solid #ddd8cc;background-color:#fffdf9">
  <h2 style="font-family:Georgia,'Noto Serif TC',serif;font-size:19px;font-weight:700;color:#1c1b19;margin:0 0 4px">來源統計</h2>
  <div style="font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif;font-size:12px;color:#6b6459;margin:0 0 4px">Top N + 小額外閱讀 合計（依來源分佈，非代表主要精選列表本身平均分佈）</div>
  <table width="100%" style="border-collapse:collapse;margin-top:10px">
    <tr>
      <td style="width:130px;padding:5px 8px;font-size:12.5px;color:#1c1b19;white-space:nowrap;font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif">來源名</td>
      <td style="padding:5px 8px">
        <table width="100%" style="border-collapse:collapse"><tr>
          <td style="width:83%;background-color:#1c1b19;height:11px;border-radius:2px;font-size:0;line-height:0">&nbsp;</td>
          <td style="width:17%;font-size:0;line-height:0">&nbsp;</td>
        </tr></table>
      </td>
      <td style="width:28px;padding:5px 8px;font-size:12.5px;color:#6b6459;text-align:right;font-family:-apple-system,BlinkMacSystemFont,'PingFang TC','Microsoft JhengHei','Noto Sans TC',Helvetica,Arial,sans-serif">5</td>
    </tr>
  </table>
</div>
```

### 3.9 頁尾

```html
<div style="padding:16px 30px;border-top:1px solid #ddd8cc;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;color:#6b6459;text-align:center;background-color:#fffdf9">Penguin 每日報報 · 共 N 篇文章 · N 個領域 · 已排除 N 個成人內容來源 · N 個來源抓取失敗</div>
```

## 4. 產生頁面前後的檢查清單

- [ ] 頁面中完全沒有 `<style>` 標籤、沒有 `class=` 依賴樣式。
- [ ] 所有顏色都來自第 1 節的色票；領域郵戳色依序輪替，只用在標籤、Top N 編號、區塊上緣粗線。
- [ ] 軟體工程／程式領域在第一個，並且有評語。
- [ ] 每張卡片有可點的標題連結與 `[YYYY-MM-DD]` 日期；連結、標題、日期三者對應同一篇原文。
- [ ] 有圖的卡片圖片網址是真的、可載入；沒圖的卡片沒有放任何佔位圖。
- [ ] 每個成功抓取的來源都有至少 3 篇（Top N 加小額外閱讀）；失敗來源列在「抓取失敗」框。
- [ ] 來源統計的長條寬度總和正確，頁尾數字和內文一致。
- [ ] 手機寬度（約 375px）下單欄顯示、無橫向捲軸。

## 5. 本 repo 的檔案約定

- 每天一個 `YYYY-MM-DD.html`，同時把最新一天複製成 `index.html`。
- 已存在的舊日期頁面不用回頭改，除非明確被要求；新風格從當天起套用。
- commit 訊息格式維持 `Daily news YYYY-MM-DD`。
