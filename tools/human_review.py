#!/usr/bin/env python3
"""讓泓本人把審查結果寫進公告欄。只改 board/BOARD.md 和 board/events.jsonl，不會 commit 或 push。

用法（在 repo 根目錄，先 git pull）：
  python tools/human_review.py TRIAL-T001 通過 v1 "親自打開頁面試算一輪，全部正確"
  python tools/human_review.py TRIAL-T001 退回 v1 "要改什麼，寫具體"

寫入的 session_id 一律是「泓」。代理不得執行這支程式。
只用 Python 標準函式庫。
"""
import json, os, re, secrets, sys
from datetime import datetime, timedelta, timezone

def main():
    if len(sys.argv) != 5 or sys.argv[2] not in ("通過", "退回"):
        print(__doc__)
        return 2
    tid, result, ver, note = sys.argv[1:]
    board = "board"
    bpath, epath = os.path.join(board, "BOARD.md"), os.path.join(board, "events.jsonl")
    lines = open(bpath, encoding="utf-8").read().split("\n")
    header = None
    for i, line in enumerate(lines):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if cells[0] == tid:
            row, idx = dict(zip(header, cells)), i
            break
    else:
        print(f"找不到任務 {tid}")
        return 1
    if row["審查者"] != "泓":
        print(f"{tid} 的審查者是「{row['審查者']}」，不是泓，不能用這支程式審查")
        return 1
    if row["狀態"] != "待審查":
        print(f"{tid} 目前狀態是「{row['狀態']}」，只有「待審查」可以審查")
        return 1
    if row["成果版本"] != ver:
        print(f"{tid} 送審的是 {row['成果版本']}，你要審的是 {ver}，版本不一致")
        return 1

    now = datetime.now(timezone.utc).replace(microsecond=0)
    ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    rev = int(row["rev"])
    new = dict(row)
    new["rev"] = str(rev + 1)
    new["狀態"] = "完成" if result == "通過" else "退回修改"
    new["最後回報"] = f"泓 審查 {ver} {result}：{note}".replace("|", "／")
    changes = {"狀態": [row["狀態"], new["狀態"]], "最後回報": [row["最後回報"], new["最後回報"]]}
    if result == "通過":
        new["租約到期"] = "—"
    else:
        minutes = 120
        proj = open(os.path.join(board, "PROJECT.md"), encoding="utf-8").read()
        m = re.search(r"\|\s*租約時間\s*\|\s*(\d+)\s*(分鐘|小時)", proj)
        if m:
            minutes = int(m.group(1)) * (60 if m.group(2) == "小時" else 1)
        new["租約到期"] = (now + timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
    if new["租約到期"] != row["租約到期"]:
        changes["租約到期"] = [row["租約到期"], new["租約到期"]]
    lines[idx] = "| " + " | ".join(new[h] for h in header) + " |"
    for i, l in enumerate(lines):
        if l.startswith("最後更新："):
            lines[i] = f"最後更新：{ts}"
            break
    event = {
        "event_id": f"泓-{now.strftime('%Y%m%dT%H%M%S')}-{secrets.token_hex(2)}",
        "project": tid.split("-")[0], "task_id": tid, "type": "reviewed", "session_id": "泓",
        "occurred_at": ts, "rev_before": rev, "rev_after": rev + 1,
        "artifact_version": ver, "result": result, "changes": changes,
        "summary": f"泓 親自審查 {ver}：{result}。{note}",
    }
    open(bpath, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    with open(epath, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f"已寫入：{tid} {row['狀態']} → {new['狀態']}（rev {rev} → {rev + 1}）")
    print("接著請執行：")
    print("  python tools/verify_board.py board")
    print("  git add board")
    print(f'  git -c user.name=泓 -c user.email=hong@local.invalid commit -m "board: reviewed {tid} by 泓"')
    print("  git push origin main")
    return 0

if __name__ == "__main__":
    sys.exit(main())
