#!/usr/bin/env python3
"""公告欄規則檢查。用法：python3 tools/verify_board.py [board 資料夾路徑]

錯誤（違反規則）會讓結束碼為 1；警告只提示，不影響結束碼。
只用 Python 標準函式庫。
"""
import json, os, re, sys
from datetime import datetime, timezone

STATES = {"草稿", "待領取", "已領取", "執行中", "阻塞", "待批准", "待審查", "退回修改",
          "完成", "失聯", "輸入已變更", "待核對", "失敗", "取消"}
ENDED = {"完成", "失敗", "取消"}
HELD = {"已領取", "執行中", "阻塞", "待批准", "待審查", "退回修改", "失聯", "輸入已變更"}
LEASE_TICKING = {"已領取", "執行中", "阻塞", "退回修改"}
EMPTY = {"", "—", "-"}
REQUIRED_EVENT = ["event_id", "project", "task_id", "type", "session_id", "occurred_at", "summary"]

errors, warnings = [], []
def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)

def table_rows(path):
    rows, header = [], None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if header is None:
            header = cells
        elif set("".join(cells)) <= set("-: "):
            continue
        else:
            rows.append(dict(zip(header, cells)))
    return rows

def kv_table(path):
    out = {}
    for r in table_rows(path):
        vals = list(r.values())
        if len(vals) >= 2:
            out[vals[0]] = vals[1]
    return out

def agent_of(session):
    return session.split("-")[0] if session and session not in EMPTY else None

def parse_time(s):
    s = s.strip()
    if not s or s in EMPTY:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%MZ"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return "bad"

def main(board):
    project = kv_table(os.path.join(board, "PROJECT.md"))
    prefix = project.get("任務前綴", "")
    if not re.fullmatch(r"[A-Z][A-Z0-9]*", prefix):
        err(f"PROJECT.md 的任務前綴「{prefix}」不是全大寫英文")

    rows = table_rows(os.path.join(board, "BOARD.md"))
    tasks = {}
    for r in rows:
        tid = r.get("ID", "")
        if tid in tasks:
            err(f"{tid}：看板有重複的列")
        tasks[tid] = r
        if not tid.startswith(prefix + "-T"):
            err(f"{tid}：編號前綴不是本專案的 {prefix}")
        st = r.get("狀態", "")
        if st not in STATES:
            err(f"{tid}：未知狀態「{st}」")
        if not r.get("rev", "").isdigit():
            err(f"{tid}：rev 不是數字")
        holder = r.get("持有 session", "")
        if st in ENDED and holder not in EMPTY and os.path.exists(os.path.join(board, "claims", tid)):
            warn(f"{tid}：已{st}，但 claims/ 仍有有效鎖，記得結案清鎖")
        if st in HELD and holder in EMPTY:
            err(f"{tid}：狀態「{st}」需要持有者，但持有 session 是空的")
        if st in HELD and holder not in EMPTY and not os.path.exists(os.path.join(board, "claims", tid)):
            err(f"{tid}：看板寫持有者 {holder}，但 claims/{tid} 不存在（鎖檔遺失或被刪除）")
        if st == "待領取" and holder not in EMPTY:
            err(f"{tid}：待領取卻有持有者 {holder}")
        rv = r.get("審查者", "")
        if rv not in EMPTY and rv == agent_of(holder) and rv != "泓":
            warn(f"{tid}：審查者 {rv} 和持有者屬於同一個主代理，請確認不是自審")
        exp = parse_time(r.get("租約到期", ""))
        if exp == "bad":
            warn(f"{tid}：租約到期時間格式看不懂，請用 2026-10-25T16:00:00Z")
        elif exp and st in LEASE_TICKING and exp < datetime.now(timezone.utc):
            warn(f"{tid}：租約已在 {r.get('租約到期')} 過期，應記錄 lease_expired 並標為失聯")

    for tid, r in tasks.items():
        for dep in [d.strip() for d in r.get("depends_on", "").split(",") if d.strip() not in EMPTY]:
            if dep not in tasks:
                err(f"{tid}：depends_on 指向不存在的 {dep}")
            elif r.get("狀態") in HELD | {"完成"} and tasks[dep].get("狀態") != "完成":
                err(f"{tid}：已被領取或完成，但依賴 {dep} 還是「{tasks[dep].get('狀態')}」")
        par = r.get("parent", "")
        if par not in EMPTY and par not in tasks:
            err(f"{tid}：parent 指向不存在的 {par}")

    claims_dir = os.path.join(board, "claims")
    for name in sorted(os.listdir(claims_dir)) if os.path.isdir(claims_dir) else []:
        path = os.path.join(claims_dir, name)
        if not os.path.isfile(path) or name.startswith(".") or name.startswith("_"):
            continue
        try:
            c = json.loads(open(path, encoding="utf-8").read())
        except Exception:
            err(f"claims/{name}：不是有效 JSON")
            continue
        r = tasks.get(name)
        if not r:
            err(f"claims/{name}：看板上沒有這個任務")
            continue
        if c.get("claim_id") != r.get("claim_id") or c.get("session_id") != r.get("持有 session"):
            err(f"{name}：claim 檔（{c.get('claim_id')}／{c.get('session_id')}）和看板（{r.get('claim_id')}／{r.get('持有 session')}）不一致")

    seen, submitted, passed = set(), {}, {}
    ev_path = os.path.join(board, "events.jsonl")
    for i, line in enumerate(open(ev_path, encoding="utf-8"), 1):
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except Exception:
            err(f"events.jsonl 第 {i} 行不是有效 JSON")
            continue
        miss = [k for k in REQUIRED_EVENT if k not in e]
        if miss:
            err(f"events.jsonl 第 {i} 行缺欄位：{', '.join(miss)}")
            continue
        if e["event_id"] in seen:
            err(f"events.jsonl 第 {i} 行：event_id {e['event_id']} 重複")
        seen.add(e["event_id"])
        if e["project"] != prefix:
            err(f"events.jsonl 第 {i} 行：project 是 {e['project']}，不是本專案 {prefix}")
        tid = e["task_id"]
        if e["type"] == "artifact_submitted":
            submitted[tid] = (e.get("artifact_version"), e["session_id"])
            passed.pop(tid, None)  # 新版本送審，舊的通過紀錄失效
        if e["type"] == "reviewed":
            check_review(i, e, tasks.get(tid, {}), submitted.get(tid), passed)

    check_approval_use(board, project, tasks)

    for tid, r in tasks.items():
        if r.get("狀態") == "完成":
            if tid not in passed:
                err(f"{tid}：標為完成，但找不到審查通過的事件")
            elif r.get("成果版本") != passed[tid]:
                err(f"{tid}：看板成果版本 {r.get('成果版本')} 和審查通過的版本 {passed[tid]} 不同")

def check_review(i, e, r, sub, passed):
    tid, sid = e["task_id"], e["session_id"]
    if agent_of(sid) != r.get("審查者") and sid != "泓":
        err(f"{tid}：第 {i} 行的審查者是 {sid}，但看板指定的審查者是 {r.get('審查者')}")
    if not sub:
        err(f"{tid}：第 {i} 行審查之前沒有任何 artifact_submitted")
        return
    ver, producer = sub
    if sid == producer or sid == r.get("持有 session"):
        err(f"{tid}：第 {i} 行是自審，審查者 {sid} 就是製作或持有成果的 session")
    if e.get("artifact_version") != ver:
        err(f"{tid}：第 {i} 行審查的是 {e.get('artifact_version')}，但最新送審版本是 {ver}")
        return
    if e.get("result") == "通過":
        passed[tid] = ver
    elif e.get("result") == "退回":
        passed.pop(tid, None)  # 退回後，之前的通過紀錄失效
    else:
        err(f"{tid}：第 {i} 行的 result 必須是「通過」或「退回」")

APPROVAL_FIELDS = ["類型", "任務與成果版本", "確切動作", "對象與範圍", "內容雜湊", "費用上限",
                   "批准者", "記錄者", "批准來源", "有效期限", "狀態"]

def check_approval_doc(name, a):
    ok = True
    for f in APPROVAL_FIELDS:
        v = a.get(f, "")
        if not v or v.startswith("〔"):
            err(f"{name}：缺少「{f}」")
            ok = False
    if a.get("批准者") and a.get("批准者") != "泓":
        err(f"{name}：批准者只能是泓，現在是「{a.get('批准者')}」")
        ok = False
    exp = parse_time(a.get("有效期限", ""))
    if a.get("有效期限") and (exp is None or exp == "bad"):
        err(f"{name}：有效期限格式錯誤，請用 2026-10-25T16:00:00Z")
        ok = False
    if a.get("狀態") and a.get("狀態") not in ("有效", "已使用", "已撤銷", "過期"):
        err(f"{name}：未知狀態「{a.get('狀態')}」")
        ok = False
    h = a.get("內容雜湊", "")
    if h and h != "無" and not re.fullmatch(r"[0-9a-f]{64}", h):
        err(f"{name}：內容雜湊必須是 64 位小寫十六進位 SHA-256，或寫「無」")
        ok = False
    return ok

def check_approval_use(board, project, tasks):
    adir = os.path.join(board, "approvals")
    if not os.path.isdir(adir):
        return
    ops_open = project.get("對外操作", "").startswith("開放")
    for name in sorted(os.listdir(adir)):
        if name.startswith("APR-") and name.endswith(".md"):
            check_approval_doc(name, kv_table(os.path.join(adir, name)))
    for name in sorted(os.listdir(adir)):
        if not name.endswith(".use"):
            continue
        apr = name[:-4]
        try:
            u = json.loads(open(os.path.join(adir, name), encoding="utf-8").read())
        except Exception:
            err(f"approvals/{name}：不是有效 JSON")
            continue
        if not ops_open:
            err(f"approvals/{name}：對外操作目前是關閉，不得領用批准")
        doc = os.path.join(adir, apr + ".md")
        if not os.path.exists(doc):
            err(f"approvals/{name}：找不到對應的批准檔 {apr}.md")
            continue
        a = kv_table(doc)
        parts = a.get("任務與成果版本", "").replace("，", " ").replace(",", " ").split()
        task = parts[0] if parts else ""
        apr_ver = next((re.sub(r"^成果", "", p) for p in parts[1:] if re.search(r"v\d+", p)), "")
        if a.get("狀態") not in ("有效", "已使用"):
            err(f"{apr}：狀態是「{a.get('狀態')}」，不能被領用")
        if u.get("task_id") != task:
            err(f"{apr}：領用的任務 {u.get('task_id')} 和批准的任務 {task} 不同")
        r = tasks.get(task, {})
        if u.get("session_id") != r.get("持有 session") or u.get("claim_id") != r.get("claim_id"):
            err(f"{apr}：領用者 {u.get('session_id')} 不是任務 {task} 目前的持有者（{r.get('持有 session')}），沒有執行資格")
        rec = a.get("記錄者", "")
        if rec not in ("泓", "") and rec != u.get("session_id"):
            err(f"{apr}：這是 {rec} 代記的批准，只有該 session 能用，{u.get('session_id')} 不能用")
        for f in ("approval_id", "task_id", "session_id", "claim_id", "run_id", "artifact_version", "payload_sha256", "used_at"):
            if f not in u:
                err(f"{apr}：.use 缺少欄位 {f}")
        exp, used = parse_time(a.get("有效期限", "")), parse_time(u.get("used_at", ""))
        if exp is None or exp == "bad":
            err(f"{apr}：批准檔沒有有效的期限，不能領用")
        elif used is None or used == "bad":
            err(f"{apr}：.use 的 used_at 格式錯誤")
        elif used > exp:
            err(f"{apr}：領用時間 {u.get('used_at')} 已超過有效期限")
        if apr_ver and u.get("artifact_version") != apr_ver:
            err(f"{apr}：批准的是 {apr_ver}，領用時卻是 {u.get('artifact_version')}，版本不同要重新批准")
        if apr_ver and r.get("成果版本") != apr_ver:
            err(f"{apr}：任務目前的成果版本是 {r.get('成果版本')}，不是批准的 {apr_ver}")
        h = a.get("內容雜湊", "")
        if h and h != "無" and u.get("payload_sha256") != h:
            err(f"{apr}：要送出的內容雜湊和批准的不一致，內容變了要重新批准")

if __name__ == "__main__":
    board = sys.argv[1] if len(sys.argv) > 1 else "board"
    main(board)
    for w in warnings:
        print("警告：" + w)
    for e in errors:
        print("錯誤：" + e)
    print(f"檢查完成：{len(errors)} 個錯誤，{len(warnings)} 個警告")
    sys.exit(1 if errors else 0)
