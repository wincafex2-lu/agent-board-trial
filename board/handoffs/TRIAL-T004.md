# 交接單 TRIAL-T004

## v1 · 2026-10-25 · 建立者 Claude-96dd1172

| 欄位 | 內容 |
| --- | --- |
| 任務 ID | TRIAL-T004 |
| 父任務 | TRIAL-T001 |
| depends_on | TRIAL-T002, TRIAL-T003 |
| 負責主代理／審查者 | DOT／Claude |
| 目標 | 做出用瀏覽器直接打開就能用的畫面 `index.html` ＋ `app.js` |
| 輸入來源 | TRIAL-T002 被接受的 `data/realms.js`；TRIAL-T003 被接受的 `calc.js`（介面見 handoffs/TRIAL-T003.md） |
| 限制與不得做的事 | 兩個依賴都完成前不得領取或開始；只能新增或修改 `index.html`、`app.js`；不改 `calc.js`、`data/`（有問題請回報）；不用任何 CDN 或外部字型、圖片、腳本，全部離線可用；不得對外動作 |
| 交付格式 | `index.html`、`app.js`；送審時 evidence 寫 commit hash，並在交接單新增版本寫手動測試結果 |
| 回報位置 | BOARD.md 的 TRIAL-T004 列，以及 events.jsonl |

### 驗收清單

- [ ] 直接雙擊 `index.html`（file://，不開伺服器）就能使用，主控台沒有錯誤
- [ ] 載入順序：`data/realms.js` → `calc.js` → `app.js`；畫面不自己重算公式，一律呼叫 `Calc.computeProgress`
- [ ] 可以選境界（煉氣、築基、金丹、元嬰）；選煉氣時才出現 1–9 層的選單
- [ ] 可以輸入目前修為與每小時修為產量
- [ ] 顯示：到下一層還差多少修為、大約要掛機幾小時、突破成功率
- [ ] 每小時產量為 0 時顯示「無法估算」；不合法輸入顯示中文錯誤訊息，不是空白或 NaN
- [ ] 例：煉氣 3 層、目前 120、每小時 30 → 畫面顯示還差 180、約 6 小時、95%
- [ ] 手機寬度（約 375px）也能正常操作，不需要橫向捲動

<!-- 之後的交接、退回、失效持有者的部分成果，都在下面新增 ## v2、## v3，不修改上面的內容 -->

## v2 · 2026-10-25T16:45:24Z · 實作與驗證 · DOT-b2104360

- session_id: DOT-b2104360；成果版本 v1，檔案 index.html、app.js。
- 使用 Edge headless 直接開啟 file:///E:/trial-dot-a/index.html，未啟動伺服器。主控台與 pageerror 均無錯誤，沒有外部請求。
- 載入順序 data/realms.js → calc.js → app.js；計算呼叫 Calc.computeProgress，未修改上游資料或計算程式。
- 瀏覽器操作驗證：煉氣 3 層 120/30 → 180、約 6 小時、95%；金丹 5000/700 → 3000、約 4.3 小時、60%；煉氣 9 層產量 0 → 無法估算；築基達標且產量 0 → 0 小時；元嬰超標 → 0 小時；0.35/0.15 回歸案例 → 0.4/0.2。
- 目前修為及產量各測空白、負數，均顯示中文錯誤並隱藏舊結果；切換非煉氣境界會隱藏並停用層數選單。
- 375px 寬度實際操作通過，scrollWidth 不超過 innerWidth。人工檢視 375px 與 1100px 截圖：欄位、按鈕、結果完整且無裁切。未以人工雙擊驗證，使用瀏覽器自動化直接開啟相同 file:// 路徑。
- node test.js：58 項通過、exit 0；git diff --check 通過。
