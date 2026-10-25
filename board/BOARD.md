# 公告欄

最後更新：2026-10-25T16:45:54Z

| ID | rev | parent | depends_on | 任務 | 負責主代理 | 持有 session | claim_id | 租約到期 | 審查者 | 狀態 | 成果版本 | 交接單 | 最後回報 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRIAL-T001 | 10 | — | — | 修仙境界計算器（主任務，見 GOAL.md） | Claude | Claude-96dd1172 | Claude-96dd1172-c1 | 2026-10-25T17:10:15Z | 泓 | 執行中 | — | handoffs/TRIAL-T001.md | T002、T003 完成；剩 T004 待 DOT 領取；活動：等待 |
| TRIAL-T002 | 12 | TRIAL-T001 | — | 數值表 data/realms.json（含 file:// 可載入的 realms.js） | DOT | DOT-58708687 | DOT-58708687-c1 | — | Claude | 完成 | v2 | handoffs/TRIAL-T002.md | 完成（v2）；鎖已結案移到 claims/_closed/ |
| TRIAL-T003 | 14 | TRIAL-T001 | TRIAL-T002 | 計算邏輯 calc.js 與自動測試 test.js | DOT | DOT-b2104360 | DOT-b2104360-c1 | — | Claude | 完成 | v2 | handoffs/TRIAL-T003.md | 完成（v2）；鎖已結案移到 claims/_closed/ |
| TRIAL-T004 | 5 | TRIAL-T001 | TRIAL-T002, TRIAL-T003 | 瀏覽器畫面 index.html ＋ app.js | DOT | DOT-b2104360 | DOT-b2104360-c2 | 2026-10-25T17:15:24Z | Claude | 待審查 | v1 | handoffs/TRIAL-T004.md | DOT-b2104360 送審 v1：22438ed，等待 Claude 審查 |
