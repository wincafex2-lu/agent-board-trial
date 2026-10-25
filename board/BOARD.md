# 公告欄

最後更新：2026-10-25T16:40:07Z

| ID | rev | parent | depends_on | 任務 | 負責主代理 | 持有 session | claim_id | 租約到期 | 審查者 | 狀態 | 成果版本 | 交接單 | 最後回報 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRIAL-T001 | 9 | — | — | 修仙境界計算器（主任務，見 GOAL.md） | Claude | Claude-96dd1172 | Claude-96dd1172-c1 | 2026-10-25T17:01:32Z | 泓 | 執行中 | — | handoffs/TRIAL-T001.md | 原持有者回來：claim 未被收回，恢復執行中並續約；活動：處理租約過期（T003 收回鎖） |
| TRIAL-T002 | 12 | TRIAL-T001 | — | 數值表 data/realms.json（含 file:// 可載入的 realms.js） | DOT | DOT-58708687 | DOT-58708687-c1 | — | Claude | 完成 | v2 | handoffs/TRIAL-T002.md | 完成（v2）；鎖已結案移到 claims/_closed/ |
| TRIAL-T003 | 13 | TRIAL-T001 | TRIAL-T002 | 計算邏輯 calc.js 與自動測試 test.js | DOT | DOT-b2104360 | DOT-b2104360-c1 | 2026-10-25T17:08:19Z | Claude | 完成 | v2 | handoffs/TRIAL-T003.md | Claude-96dd1172 審查 v2 通過（c7596cf），任務完成 |
| TRIAL-T004 | 1 | TRIAL-T001 | TRIAL-T002, TRIAL-T003 | 瀏覽器畫面 index.html ＋ app.js | DOT | — | — | — | Claude | 待領取 | — | handoffs/TRIAL-T004.md | 等 TRIAL-T002、TRIAL-T003 完成才能領取 |
