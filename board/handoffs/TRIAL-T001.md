# 交接單 TRIAL-T001

## v1 · 2026-10-25 · 建立者 Claude-96dd1172

| 欄位 | 內容 |
| --- | --- |
| 任務 ID | TRIAL-T001 |
| 父任務 | — |
| depends_on | — |
| 負責主代理／審查者 | Claude／泓 |
| 目標 | 在 repo 內做出用瀏覽器直接打開就能用的修仙境界計算器（GOAL.md），不部署 |
| 輸入來源 | `GOAL.md`；`board/PROJECT.md` |
| 子任務 | TRIAL-T002 數值表 → TRIAL-T003 計算邏輯與測試 → TRIAL-T004 瀏覽器畫面 |
| 限制與不得做的事 | 不部署、不上傳到任何其他網站；不安裝需要登入或付費的套件（本專案只用 Node 內建功能，不用 npm 套件）；對外操作關閉 |
| 交付格式 | 整合成果：`index.html`、`app.js`、`calc.js`、`data/realms.json`、`test.js`，加上整合說明（送審時寫在本交接單新版本） |
| 回報位置 | BOARD.md 的 TRIAL-T001 列，以及 events.jsonl |

### 驗收清單

- [ ] TRIAL-T002、TRIAL-T003、TRIAL-T004 都是「完成」，且沒有子任務處於阻塞、待批准、失聯、待核對
- [ ] 在 repo 根目錄執行 `node test.js`，結束碼為 0
- [ ] 直接雙擊 `index.html`（file://，不開伺服器）即可使用，瀏覽器主控台沒有錯誤
- [ ] 四個境界與煉氣 1–9 層都能選；顯示「還差多少修為」「大約掛機幾小時」「突破成功率」，數值和 GOAL.md 的假資料一致
- [ ] 整個過程沒有對外動作，`python tools/verify_board.py board` 沒有錯誤
- [ ] 泓親自打開頁面試算一輪並驗收

<!-- 之後的交接、退回、失效持有者的部分成果，都在下面新增 ## v2、## v3，不修改上面的內容 -->

## v2 · 2026-10-25T16:50:34Z · 送審整合成果 v1 給泓 · 持有者 Claude-96dd1172

### 整合成果 v1

成果版本 v1 ＝ `main` 在 commit `2ceb5ad` 時的下列檔案（之後如有任何變動就不是 v1）：

| 檔案 | git blob（`git rev-parse 2ceb5ad:<檔案>`） |
| --- | --- |
| `index.html` | `b4449f2d8ef174c714ff1032e49dbc1a8586a33f` |
| `app.js` | `4f9b70812479e13221f9b2f421bd2ed2b42e88a6` |
| `calc.js` | `4a7e0737ac4e6692ea8e1cf9ba13ccbebd626fc0` |
| `test.js` | `845be51249629a6a607d34b71527a51a0ecd3b06` |
| `data/realms.json` | `13dfb724079630e98a862bd290edf95e531eb941` |
| `data/realms.js` | `a082a3ba05fc492eda58146afea42325eb6ec344` |
| `data/.gitattributes` | `e67f061c13744b4ed133fe47ca4672069a5f5a3c` |
| `scripts/build-realms.js` | `975aeabef8e63973bad44a7884a8ae11e1cc03eb` |

| 子任務 | 被接受版本 | 審查 |
| --- | --- | --- |
| TRIAL-T002 數值表 | v2（1cf521d） | v1 退回（行尾）→ v2 通過 |
| TRIAL-T003 計算邏輯與測試 | v2（c7596cf） | v1 退回（四捨五入）→ 原持有者失聯、鎖被收回 → 新持有者 v2 通過 |
| TRIAL-T004 畫面 | v1（22438ed） | v1 通過 |

### 父任務完成條件（RULES 第 7 條）

- 子任務 T002、T003、T004 全部「完成」，鎖都已結案清鎖；沒有子任務處於阻塞、待批准、失聯、待核對。
- 送審前在全新 clone 自行整合驗證：`node test.js` 58 項通過；重跑 `node scripts/build-realms.js` 後 `git status` 乾淨；headless Chrome 直接開 file:// 無主控台錯誤；`python tools/verify_board.py board` 0 錯誤 0 警告。
- 全程沒有對外動作，只對本 repo 做 fetch／pull／push，沒有 force push。

### 泓的驗收步驟

1. `git pull`，確認 `main` 包含 commit `2ceb5ad`，看板上 TRIAL-T001 是「待審查」、成果版本 v1。
2. 在 repo 根目錄執行 `node test.js`，最後一行應為「全部通過：58 項測試」，結束碼 0。
3. 在檔案總管雙擊 `index.html`（不要開伺服器）。開啟後應直接顯示：煉氣 1 層 · 還差 100 · 約 3.3 小時 · 95%。
4. 試算並核對：
   - 煉氣、第 3 層、目前 120、每小時 30 → 還差 180、約 6 小時、95%
   - 金丹、目前 5000、每小時 700 → 還差 3000、約 4.3 小時、60%
   - 元嬰、目前 0、每小時 1000 → 還差 30000、約 30 小時、40%
   - 每小時改成 0 → 預估時間顯示「無法估算」
   - 目前修為清空或填負數 → 出現中文錯誤訊息
   - 切到築基／金丹／元嬰時，「煉氣層數」選單會消失
5. （可選）按 F12 看主控台沒有紅字；把視窗縮到手機寬度，不需要左右捲動。
6. 驗收結果請由泓本人寫入：通過就在看板把 TRIAL-T001 改為「完成」並追加 `reviewed`（result「通過」、artifact_version「v1」、session_id「泓」）；不通過則改為「退回修改」並寫明要改什麼。代理不會代寫泓的審查。
