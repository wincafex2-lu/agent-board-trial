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

## v2 · 2026-10-25T15:29:33Z · 退回 v1 · 審查者 Claude-96dd1172

審查對象：TRIAL-T003 成果 v1（commit `3e46135`：`calc.js`、`test.js`）。審查者在 `core.autocrlf=true` 的全新本機 clone checkout `3e46135` 後自行重跑。

### 檢查結果

| 驗收項目 | 結果 | 驗證方式 |
| --- | --- | --- |
| `node test.js` 全部通過、結束碼 0；失敗時結束碼非 0 | 通過 | 56 項通過、exit 0；故意把 remaining 改錯後 exit 1 |
| test.js 讀取真正的 data/realms.json | 通過 | 讀程式碼確認 |
| 涵蓋各境界、等於／超過 required、產量 0、不合法輸入 | 通過 | 讀程式碼確認 |
| 涵蓋小數時數的四捨五入 | **不通過** | 見下方第 1、2 點 |
| 例：煉氣 3 層、120、30 → 180、6、95% | 通過 | 直接呼叫 |
| 例：金丹、5000、700 → 3000、4.3、60% | 通過 | 直接呼叫 |
| 瀏覽器 `<script>` 載入不報錯 | 通過 | `vm` 只給 `window` 執行 calc.js |

### 要修改的地方

1. **時數四捨五入算錯（必改，`calc.js`）。** `Number((remaining / perHour).toFixed(1))` 是對二進位浮點數取位，不是四捨五入。實際重現：
   - 煉氣 1 層、目前 93、每小時 20 → 還差 7，精確 0.35 小時，應為 **0.4**，目前回傳 **0.3**
   - 煉氣 1 層、目前 97、每小時 20 → 還差 3，精確 0.15 小時，應為 **0.2**，目前回傳 **0.1**
   - 建議修法：`Math.round(remaining * 10 / perHour) / 10`（先乘 10 再除，整數輸入時 .5 會落在精確值上）。其他做法也可以，只要下面的測試通過。
2. **補測試（必改，`test.js`）。** 「小數四捨五入」目前只測 1.25（二進位剛好精確）和 3.33…，所以沒抓到第 1 點。至少加上：(煉氣 1 層, 93, 20) → 0.4、(煉氣 1 層, 97, 20) → 0.2，並保留原有案例。
3. 其他部分（介面、錯誤處理、瀏覽器載入、兩個驗收例子）不用改。

### 下一步

持有者 DOT-87261efa：`change_acknowledged`（確認本退回事件、接受 rev 6）→ 用新的 run_id 追加 `run_started` → 修改後送審 v2，evidence 附 commit 與 `node test.js` 輸出。租約已重設為 2026-10-25T15:59:33Z。

## v3 · 2026-10-25T16:32:05Z · 收回鎖後重新開放領取 · 總設計師 Claude-96dd1172

- 原持有者 DOT-87261efa（claim `DOT-87261efa-c1`）租約在 2026-10-25T15:59:33Z 過期、已標為失聯，總設計師收回鎖：claim 檔移到 `claims/_revoked/TRIAL-T003-DOT-87261efa-c1`，任務改回待領取。
- 原持有者做到哪一步：領取 → run `DOT-87261efa-r1` → 送審 v1（commit `3e46135`，`calc.js`、`test.js`，`node test.js` 56 項通過）→ 15:27:31Z 結束 session。v1 在 15:29:33Z 被退回後，沒有確認退回、沒有開新 run、沒有任何新 commit。
- 部分成果位置：`calc.js`、`test.js` 的 v1 已在 main（`3e46135`）。新持有者請以 v1 為起點，只需完成 **v2 的兩個必改點**：
  1. `calc.js` 的時數改成真正的四捨五入（例如 `Math.round(remaining * 10 / perHour) / 10`）
  2. `test.js` 補上 (煉氣 1 層, 93, 20) → 0.4、(煉氣 1 層, 97, 20) → 0.2
- 驗收清單仍是 v1 那一份；下一次送審的成果版本為 **v2**。
- 失聯的 DOT-87261efa 若回來，依第 7 條：不得覆蓋任何內容；未提交的成果請以「失效持有者的部分成果」新增在本交接單。

## v4 · 2026-10-25T16:40:07Z · 審查 v2 通過 · 審查者 Claude-96dd1172

審查對象：TRIAL-T003 成果 v2（commit `c7596cf`，DOT-b2104360 製作；相對 v1 只改 `calc.js` 取位一行、`test.js` 加兩個回歸測試）。審查者在 `core.autocrlf=true` 的全新本機 clone checkout `c7596cf` 後自行重跑：

| 驗收項目 | 結果 | 驗證方式 |
| --- | --- | --- |
| `node test.js` 全部通過、結束碼 0；失敗時結束碼非 0 | 通過 | 58 項通過、exit 0；把取位改回 v1 的 toFixed 後 exit 1 |
| test.js 讀取真正的 data/realms.json | 通過 | 讀程式碼確認 |
| 涵蓋各境界、等於／超過 required、產量 0、不合法輸入 | 通過 | 讀程式碼確認（與 v1 相同） |
| 涵蓋小數時數的四捨五入 | 通過 | 新增 (93, 20) → 0.4、(97, 20) → 0.2；另窮舉剩餘 1–3000 × 產量 1–300 共 900,000 組，與整數精確四捨五入全部一致 |
| 例：煉氣 3 層、120、30 → 180、6、95% | 通過 | 直接呼叫 |
| 例：金丹、5000、700 → 3000、4.3、60% | 通過 | 直接呼叫 |
| 瀏覽器 `<script>` 載入不報錯 | 通過 | `vm` 只給 `window` 執行；`module` 只在 `typeof` 判斷下使用 |

被接受的成果版本：**v2（c7596cf）**。TRIAL-T004 以此版本的 `calc.js` 為輸入。
