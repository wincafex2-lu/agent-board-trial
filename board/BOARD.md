# 公告欄

最後更新：2026-10-25T15:26:55Z

| ID | rev | parent | depends_on | 任務 | 負責主代理 | 持有 session | claim_id | 租約到期 | 審查者 | 狀態 | 成果版本 | 交接單 | 最後回報 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRIAL-T001 | 6 | — | — | 修仙境界計算器（主任務，見 GOAL.md） | Claude | Claude-96dd1172 | Claude-96dd1172-c1 | 2026-10-25T15:53:08Z | 泓 | 執行中 | — | handoffs/TRIAL-T001.md | 巡查公告欄並續約；活動：審核 TRIAL-T002 v2 |
| TRIAL-T002 | 12 | TRIAL-T001 | — | 數值表 data/realms.json（含 file:// 可載入的 realms.js） | DOT | DOT-58708687 | DOT-58708687-c1 | — | Claude | 完成 | v2 | handoffs/TRIAL-T002.md | 完成（v2）；鎖已結案移到 claims/_closed/ |
| TRIAL-T003 | 4 | TRIAL-T001 | TRIAL-T002 | 計算邏輯 calc.js 與自動測試 test.js | DOT | DOT-87261efa | DOT-87261efa-c1 | 2026-10-25T15:56:55Z | Claude | 執行中 | — | handoffs/TRIAL-T003.md | DOT-87261efa 完成 calc.js、test.js；56 項測試通過，包含瀏覽器載入與所有輸入邊界；續約 |
| TRIAL-T004 | 1 | TRIAL-T001 | TRIAL-T002, TRIAL-T003 | 瀏覽器畫面 index.html ＋ app.js | DOT | — | — | — | Claude | 待領取 | — | handoffs/TRIAL-T004.md | 等 TRIAL-T002、TRIAL-T003 完成才能領取 |
