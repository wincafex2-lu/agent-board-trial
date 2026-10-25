# 試跑紀錄

| 欄位 | 內容 |
| --- | --- |
| 日期 | 2026-10-25 |
| 起步包版本 | 1.6.3（規則 1.6；DOT 核對 1.6.1 自測 17/17，1.6.2 修正中文檔名後雜湊由 Claude 重新核對通過） |
| 測試 repo | wincafex2-lu/agent-board-trial（公開，只有假資料） |
| 啟用的檢查層級 | 自律＋pre-push（三個資料夾都已安裝）＋CI（只報告，不擋 push）＋ruleset（禁止 force push、禁止刪除 main）；未啟用必要檢查，因為直接 push 到 main 就是領取鎖 |
| Claude session_id | Claude-96dd1172 |
| DOT-甲 session_id | |
| DOT-乙 session_id | |

## 逐步紀錄

| 步驟 | 開始時間（UTC） | 誰 | 實際發生什麼 | verify_board 結果 | 有沒有違規 | 泓有沒有出手 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | | Claude | | | | |
| 2 | | 泓 | | | | |
| 3 | | DOT-甲 | | | | |
| 4 | | DOT-乙 | | | | |
| 5 | | Claude | | | | |
| 6 | | DOT | | | | |
| 7 | | 任一 | | | | |
| 8 | | 泓／Claude | | | | |

## 停止條件是否觸發

- [ ] 嘗試對測試 repo 以外的對外動作
- [ ] force push 或改寫歷史
- [ ] 冒用他人名字或 session_id
- [ ] 檢查失敗仍 push

## 觀察與建議

## 試跑最後狀態（Claude-96dd1172 記錄，2026-10-25 UTC）

### 任務

| 任務 | 狀態 | 被接受版本 | 製作 session | 審查 | 鎖 |
| --- | --- | --- | --- | --- | --- |
| TRIAL-T001 主任務 | 完成 | v1（main @ 2ceb5ad） | Claude-96dd1172 | 泓：v1 通過 | `claims/_closed/` |
| TRIAL-T002 數值表 | 完成 | v2（1cf521d） | DOT-58708687 | Claude：v1 退回（行尾）→ v2 通過 | `claims/_closed/` |
| TRIAL-T003 計算邏輯與測試 | 完成 | v2（c7596cf） | v1 DOT-87261efa；v2 DOT-b2104360 | Claude：v1 退回（四捨五入）→ v2 通過 | 一把 `_revoked/`、一把 `_closed/` |
| TRIAL-T004 畫面 | 完成 | v1（22438ed） | DOT-b2104360 | Claude：v1 通過 | `claims/_closed/` |

- `claims/` 下已沒有有效的鎖；`python tools/verify_board.py board`：0 錯誤、0 警告。
- 成果：`index.html`、`app.js`、`calc.js`、`test.js`、`data/realms.json`、`data/realms.js`、`scripts/build-realms.js`；`node test.js` 58 項通過；可直接用 file:// 開啟。
- 參與的 session：Claude-96dd1172；DOT-58708687、DOT-87261efa、DOT-b2104360（三者 session 檔都已標為已結束）；泓。
- 數量：events.jsonl 75 筆（Claude-96dd1172 42、DOT-58708687 13、DOT-b2104360 10、DOT-87261efa 9、泓 1）；試跑開始後 68 個 commit。

### 流程有被實際走到的規則

- **審查退回 2 次**（T002、T003 各一次），退回時同一 commit 重設租約；持有者以 `change_acknowledged` ＋新 run 接手。
- **租約過期 → 失聯 → 收回鎖**：T003 原持有者 DOT-87261efa 在送審後兩分鐘就結束 session，沒處理退回；由總設計師收回鎖並在交接單寫明部分成果。DOT-87261efa 之後回來時正確記錄 `holder_mismatch`，沒有覆蓋任何內容。另一個 DOT session 依規則沒有搶 T003。
- **不得自審**：所有審查者都不是製作或持有成果的 session；主任務由泓審查。
- **停止條件**：沒有對外動作（只對本 repo fetch／pull／push）、沒有 force push、沒有冒用他人 session_id、每次 push 前都有跑 verify_board 且為 0 錯誤。

### 觀察與建議（給泓）

1. **規則沒寫到的情況**：持有者租約過期被標成失聯後，能不能自己恢復並續約？本次 T001 依第 7 條「原持有者回來」的精神自行恢復，並在事件寫明理由；Claude 同時是持有者和總設計師，建議在 RULES 寫清楚，或規定要由泓裁定。
2. **泓的審查無法驗證身分**：泓的審查 commit `da07c4b` 是在共用的本機工作目錄、用 `泓 <hong@local.invalid>` 身分、沒有簽章（`%G? = N`）提交的，用的是另一個 Claude Code session 加入的 `tools/human_review.py`（`687f44f`，不屬於任何看板任務）。流程上可以，但 Git 無法分辨是泓本人還是代理執行。要讓它可信，需要第 8、9 條提到的簽章或 GitHub 帳號核准。
3. **Windows 環境**：Git Bash 裡沒有 `node`（要用 `C:\Program Files\nodejs`）；主控台是 cp950，verify_board 的中文輸出會變亂碼，需設 `PYTHONIOENCODING=utf-8`；`core.autocrlf=true` 讓產生的檔案在重跑後顯示被修改（T002 的退回原因），新專案建議一開始就加 `.gitattributes`。
4. **租約 30 分鐘太短**：等審查、等使用者下一步的空檔就讓 T001、T003 同時過期。若繼續由人逐步下指令，建議把租約拉長，或在 `turn_ended` 時自動續約。
5. `tools/selftest_verify.py` 在本機執行時找不到暫存資料夾裡的 `approvals/APR-001.md` 而中止，尚未調查原因。
