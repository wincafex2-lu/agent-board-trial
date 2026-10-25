# 試跑紀錄

| 欄位 | 內容 |
| --- | --- |
| 日期 | 2026-10-25 |
| 起步包版本 | 1.6.3（規則 1.6；DOT 核對 1.6.1 自測 17/17，1.6.2 修正中文檔名後雜湊由 Claude 重新核對通過） |
| 測試 repo | wincafex2-lu/agent-board-trial（公開，只有假資料） |
| 啟用的檢查層級 | 自律＋pre-push（三個資料夾都已安裝）＋CI（只報告，不擋 push）＋ruleset（禁止 force push、禁止刪除 main）；未啟用必要檢查，因為直接 push 到 main 就是領取鎖 |
| Claude session_id | |
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
