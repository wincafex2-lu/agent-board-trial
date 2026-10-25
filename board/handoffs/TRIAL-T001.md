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
