# 公告欄

最後更新：2026-10-25T15:21:12Z

| ID | rev | parent | depends_on | 任務 | 負責主代理 | 持有 session | claim_id | 租約到期 | 審查者 | 狀態 | 成果版本 | 交接單 | 最後回報 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRIAL-T001 | 5 | — | — | 修仙境界計算器（主任務，見 GOAL.md） | Claude | Claude-96dd1172 | Claude-96dd1172-c1 | 2026-10-25T15:45:59Z | 泓 | 執行中 | — | handoffs/TRIAL-T001.md | 巡查公告欄並續約；活動：審核 TRIAL-T002 v1 |
| TRIAL-T002 | 9 | TRIAL-T001 | — | 數值表 data/realms.json（含 file:// 可載入的 realms.js） | DOT | DOT-58708687 | DOT-58708687-c1 | 2026-10-25T15:51:12Z | Claude | 執行中 | v1 | handoffs/TRIAL-T002.md | DOT-58708687 Windows 重新 checkout 後連跑兩次產生器，git status 均乾淨 |
| TRIAL-T003 | 1 | TRIAL-T001 | TRIAL-T002 | 計算邏輯 calc.js 與自動測試 test.js | DOT | — | — | — | Claude | 待領取 | — | handoffs/TRIAL-T003.md | 等 TRIAL-T002 完成才能領取 |
| TRIAL-T004 | 1 | TRIAL-T001 | TRIAL-T002, TRIAL-T003 | 瀏覽器畫面 index.html ＋ app.js | DOT | — | — | — | Claude | 待領取 | — | handoffs/TRIAL-T004.md | 等 TRIAL-T002、TRIAL-T003 完成才能領取 |
