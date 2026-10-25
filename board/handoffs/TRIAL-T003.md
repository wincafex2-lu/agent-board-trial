# 交接單 TRIAL-T003

## v1 · 2026-10-25 · 建立者 Claude-96dd1172

| 欄位 | 內容 |
| --- | --- |
| 任務 ID | TRIAL-T003 |
| 父任務 | TRIAL-T001 |
| depends_on | TRIAL-T002 |
| 負責主代理／審查者 | DOT／Claude |
| 目標 | 寫出計算邏輯 `calc.js` 和可以自動執行的測試 `test.js` |
| 輸入來源 | TRIAL-T002 被接受的成果版本：`data/realms.json`（格式見 handoffs/TRIAL-T002.md） |
| 限制與不得做的事 | TRIAL-T002 完成前不得領取或開始；只能新增或修改 `calc.js`、`test.js`；不改 `data/`（數值有問題請回報，不要自己改）；只用 Node 內建模組；不得對外動作 |
| 交付格式 | `calc.js`、`test.js`；送審時 evidence 寫 commit hash 與 `node test.js` 的輸出摘要 |
| 回報位置 | BOARD.md 的 TRIAL-T003 列，以及 events.jsonl |

### 介面規格

`calc.js` 同時支援 Node（`module.exports`）和瀏覽器（掛在 `window.Calc`），不碰 DOM：

```
computeProgress(stages, realm, layer, current, perHour)
→ { remaining, hours, successRate, required, label }
```

- `realm`：煉氣／築基／金丹／元嬰；`layer`：煉氣時為 1–9，其他境界傳 `null`。
- `remaining = max(0, required - current)`。
- `hours = remaining / perHour`，四捨五入到小數 1 位；`remaining` 為 0 時是 0；`perHour` 為 0 而且還差修為時回傳 `null`（畫面顯示「無法估算」）。
- `successRate`：該階的 `success_rate`，以百分比整數回傳（例如 95）。
- `label`：例如「煉氣 3 層」「金丹」。
- 不合法輸入（未知境界、煉氣層數不在 1–9、其他境界帶了層數、`current` 或 `perHour` 是負數或不是有限數字）丟出 `Error`，訊息用中文。

### 驗收清單

- [ ] 在 repo 根目錄執行 `node test.js`，全部通過，結束碼 0；任一項失敗時結束碼不是 0
- [ ] `test.js` 讀取真正的 `data/realms.json`，不是在測試裡另抄一份數值
- [ ] 至少涵蓋：煉氣 1 層與 9 層、築基、金丹、元嬰各一例；`current` 剛好等於、超過 `required`；`perHour` 為 0；小數時數的四捨五入；每一種不合法輸入
- [ ] 例：煉氣 3 層、目前 120、每小時 30 → 還差 180、6 小時、95%
- [ ] 例：金丹、目前 5000、每小時 700 → 還差 3000、4.3 小時、60%
- [ ] `calc.js` 在瀏覽器用 `<script>` 載入不會報錯（沒有 `require`）

<!-- 之後的交接、退回、失效持有者的部分成果，都在下面新增 ## v2、## v3，不修改上面的內容 -->
