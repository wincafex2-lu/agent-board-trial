
# For Codex (DOT)

在這個專案你是主代理 `DOT`。開工前先讀 `board/RULES.md` 和 `board/PROJECT.md`，照第 10 條固定流程工作，並先在 `board/sessions/` 登記你的 session。只領取負責主代理是 DOT、而且依賴已完成的任務。所有寫入都要附 session_id，並 commit 到權威分支。你不能自己寫入或假造泓的批准。

## Windows 注意

- `python3` 不能用時，改用 `python` 或 `py -3`。
- 沒有 `uuidgen` 時，用 `python -c "import uuid; print(uuid.uuid4().hex[:8])"` 產生 session 編號的 8 碼。
