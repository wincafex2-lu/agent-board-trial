# 交接單 TRIAL-T002

## v1 · 2026-10-25 · 建立者 Claude-96dd1172

| 欄位 | 內容 |
| --- | --- |
| 任務 ID | TRIAL-T002 |
| 父任務 | TRIAL-T001 |
| depends_on | — |
| 負責主代理／審查者 | DOT／Claude |
| 目標 | 把 GOAL.md 的假資料做成數值表 `data/realms.json`，並產生瀏覽器在 file:// 下也能載入的 `data/realms.js` |
| 輸入來源 | `GOAL.md` 的數值表（照用） |
| 限制與不得做的事 | 只能新增或修改 `data/` 和 `scripts/build-realms.js`；只用 Node 內建模組，不用 npm 套件；不改 `board/` 以外別人的任務列；不得對外動作 |
| 交付格式 | `data/realms.json`（權威資料）、`scripts/build-realms.js`、由它產生的 `data/realms.js`；送審時在 `artifact_submitted` 的 evidence 寫 commit hash |
| 回報位置 | BOARD.md 的 TRIAL-T002 列，以及 events.jsonl |

### 資料格式（下游 T003、T004 依這個格式寫，要改請先回報）

```json
{
  "stages": [
    {"realm": "煉氣", "layer": 1, "required": 100, "success_rate": 0.95},
    {"realm": "煉氣", "layer": 9, "required": 900, "success_rate": 0.95},
    {"realm": "築基", "layer": null, "required": 2000, "success_rate": 0.80},
    {"realm": "金丹", "layer": null, "required": 8000, "success_rate": 0.60},
    {"realm": "元嬰", "layer": null, "required": 30000, "success_rate": 0.40}
  ]
}
```

- `stages` 依修煉順序排列，共 12 筆：煉氣 1–9 層、築基、金丹、元嬰（上面只列出部分）。
- `required`：在這一階要累積多少修為才能往下一階突破；`success_rate`：從這一階突破的成功率，0 到 1 的小數。
- `data/realms.js` 內容為 `window.REALMS = <realms.json 的內容>;`，只能由 `node scripts/build-realms.js` 產生，不手改。
- 原因：Chrome 在 file:// 下會擋掉 `fetch` 本機 JSON，畫面要用 `<script src="data/realms.js">` 載入。

### 驗收清單

- [ ] `data/realms.json` 是有效 JSON，`stages` 剛好 12 筆，順序是煉氣 1–9、築基、金丹、元嬰
- [ ] 煉氣第 n 層的 `required` 是 100 × n；築基 2000、金丹 8000、元嬰 30000
- [ ] 成功率：煉氣 0.95、築基 0.80、金丹 0.60、元嬰 0.40
- [ ] 執行 `node scripts/build-realms.js` 後，`data/realms.js` 的內容和 `realms.json` 一致（重跑後 `git diff` 沒有變化）
- [ ] 沒有新增 `package.json` 依賴、沒有 `node_modules/`

<!-- 之後的交接、退回、失效持有者的部分成果，都在下面新增 ## v2、## v3，不修改上面的內容 -->

## v2 · 2026-10-25T15:17:32Z · 退回 v1 · 審查者 Claude-96dd1172

審查對象：TRIAL-T002 成果 v1（commit 5a84b28：`data/realms.json`、`data/realms.js`、`scripts/build-realms.js`）

### 檢查結果

| 驗收項目 | 結果 | 審查者自行驗證的方式 |
| --- | --- | --- |
| 有效 JSON、12 筆、順序煉氣 1–9、築基、金丹、元嬰 | 通過 | Node v24.22.1 讀取 realms.json 逐筆比對 |
| 煉氣 100 × n；築基 2000、金丹 8000、元嬰 30000 | 通過 | 同上 |
| 成功率 0.95／0.80／0.60／0.40 | 通過 | 同上 |
| realms.js 內容和 realms.json 一致 | 通過 | 用 `vm` 執行 realms.js，比對 `window.REALMS` 與 realms.json |
| 重跑 `node scripts/build-realms.js` 後沒有變化 | **不通過** | 見下方 |
| 沒有 package.json 依賴、沒有 node_modules/ | 通過 | 兩者都不存在 |

### 要修改的地方

1. **重跑產生器後工作目錄不乾淨（必改）。** 在 Windows（`core.autocrlf=true`，repo 沒有 `.gitattributes`）checkout 後，`data/realms.js` 的工作目錄行尾是 CRLF；`build-realms.js` 寫出的是 LF。所以只要重跑一次，`git status --short` 就顯示 ` M data/realms.js`（`git diff` 內容雖然是空的）。驗收清單的意思是「重跑後 repo 不出現任何變更」，目前不符合。
   - 修法：新增 `data/.gitattributes`，至少寫 `realms.js text eol=lf`（建議 `realms.json` 也一起設 `text eol=lf`），讓 checkout 和產生器都用 LF。這個檔在 `data/` 裡，沒有超出本任務的檔案範圍。
   - 驗證方式：commit 後執行 `git rm --cached -r data && git reset --hard`（或重新 clone）讓 data/ 依新屬性重新 checkout，再跑 `node scripts/build-realms.js`，`git status --short` 必須完全沒有輸出。送審時把這段指令和輸出寫進 evidence 或交接單。
2. 資料內容、格式、`realms.js` 的產生方式都不需要改，請不要變動數值。

### 下一步

持有者 DOT-58708687：`change_acknowledged`（確認本退回事件、接受 rev 6）→ 用新的 run_id 追加 `run_started` → 修改後送審 v2。租約已重設為 2026-10-25T15:47:32Z。
