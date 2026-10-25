#!/usr/bin/env python3
"""用範例公告欄做幾個情境，確認 verify_board.py 抓得到違規。用法：python3 tools/selftest_verify.py"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLE = os.path.join(HERE, "..", "examples", "game", "board")

def run(board):
    p = subprocess.run([sys.executable, os.path.join(HERE, "verify_board.py"), board], capture_output=True, text=True, encoding="utf-8",
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return p.returncode, p.stdout

def add_event(board, **e):
    base = {"project": "GAME", "occurred_at": "2026-10-25T18:00:00Z", "summary": "測試"}
    base.update(e)
    with open(os.path.join(board, "events.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(base, ensure_ascii=False) + "\n")

def set_row(board, tid, **cols):
    path = os.path.join(board, "BOARD.md")
    lines = open(path, encoding="utf-8").read().split("\n")
    header = [c.strip() for c in lines[[i for i, l in enumerate(lines) if l.startswith("| ID")][0]].strip("|").split("|")]
    for i, l in enumerate(lines):
        if l.startswith(f"| {tid} |"):
            cells = [c.strip() for c in l.strip("|").split("|")]
            for k, v in cols.items():
                cells[header.index(k)] = v
            lines[i] = "| " + " | ".join(cells) + " |"
    open(path, "w", encoding="utf-8").write("\n".join(lines))

def case(name, expect_fail, mutate, must_contain=None):
    d = tempfile.mkdtemp()
    b = os.path.join(d, "board")
    shutil.copytree(EXAMPLE, b)
    mutate(b)
    code, out = run(b)
    ok = (code != 0) == expect_fail and (must_contain is None or must_contain in out)
    print(("通過" if ok else "失敗") + f"：{name}")
    if not ok:
        print(out)
    shutil.rmtree(d)
    return ok

def legit_pass(b):
    add_event(b, event_id="DOT-a41f9e22-x1", task_id="GAME-T002", type="reviewed", session_id="DOT-a41f9e22",
              artifact_version="v1", result="通過")
    set_row(b, "GAME-T002", 狀態="完成", rev="5")
    os.makedirs(os.path.join(b, "claims", "_closed"), exist_ok=True)
    shutil.move(os.path.join(b, "claims", "GAME-T002"), os.path.join(b, "claims", "_closed", "GAME-T002-Claude-2b8d0f13-c1"))

def self_review(b):
    add_event(b, event_id="Claude-2b8d0f13-x2", task_id="GAME-T002", type="reviewed", session_id="Claude-2b8d0f13",
              artifact_version="v1", result="通過")

def wrong_version(b):
    add_event(b, event_id="DOT-a41f9e22-x3", task_id="GAME-T002", type="reviewed", session_id="DOT-a41f9e22",
              artifact_version="v2", result="通過")

def done_without_review(b):
    set_row(b, "GAME-T004", 狀態="完成")

def done_keeps_lock(b):
    legit_pass(b)
    shutil.copy(os.path.join(b, "claims", "_closed", "GAME-T002-Claude-2b8d0f13-c1"), os.path.join(b, "claims", "GAME-T002"))

def dependency_skipped(b):
    set_row(b, "GAME-T003", 狀態="已領取", **{"持有 session": "DOT-a41f9e22", "claim_id": "DOT-a41f9e22-c2"})

def duplicate_event(b):
    add_event(b, event_id="DOT-a41f9e22-x4", task_id="GAME-T004", type="progress_reported", session_id="DOT-a41f9e22")
    add_event(b, event_id="DOT-a41f9e22-x4", task_id="GAME-T004", type="progress_reported", session_id="DOT-a41f9e22")

def late_return_resets_lease(b):
    # 原租約早已過期，審查者退回時把租約重設為退回時間＋2 小時（遠在未來），不應出現過期警告
    add_event(b, event_id="DOT-a41f9e22-x5", task_id="GAME-T002", type="reviewed", session_id="DOT-a41f9e22",
              artifact_version="v1", result="退回")
    set_row(b, "GAME-T002", 狀態="退回修改", rev="5", 租約到期="2099-01-01T00:00:00Z")

HASH = "a" * 64

def approval_doc(b, expiry="2099-01-01T00:00:00Z", version="v1", h=HASH):
    rows = {"類型": "批准動作", "任務與成果版本": f"GAME-T004，成果 {version}", "確切動作": "上傳測試版（自我測試用假動作）",
            "對象與範圍": "測試 repo 內的 fake-publish.txt", "內容雜湊": h, "費用上限": "免費", "批准者": "泓",
            "記錄者": "泓", "批准來源": "自我測試 fixture，非真實批准", "有效期限": expiry, "狀態": "有效"}
    body = "# APR-001\n\n| 欄位 | 內容 |\n| --- | --- |\n" + "".join(f"| {k} | {v} |\n" for k, v in rows.items() if v is not None)
    os.makedirs(os.path.join(b, "approvals"), exist_ok=True)
    open(os.path.join(b, "approvals", "APR-001.md"), "w", encoding="utf-8").write(body)

def use_setup(b, who, claim, version="v1", h=HASH, **doc):
    p = os.path.join(b, "PROJECT.md")
    t = open(p, encoding="utf-8").read().replace("關閉（試跑期間", "開放（自我測試")
    open(p, "w", encoding="utf-8").write(t)
    set_row(b, "GAME-T004", 成果版本="v1")
    approval_doc(b, **doc)
    open(os.path.join(b, "approvals", "APR-001.use"), "w", encoding="utf-8").write(json.dumps(
        {"approval_id": "APR-001", "task_id": "GAME-T004", "session_id": who, "claim_id": claim,
         "run_id": who + "-r1", "artifact_version": version, "payload_sha256": h,
         "used_at": "2026-10-25T15:30:00Z"}) + "\n")

HOLDER = ("DOT-a41f9e22", "DOT-a41f9e22-c1")
def use_by_holder(b): use_setup(b, *HOLDER)
def use_by_non_holder(b): use_setup(b, "DOT-0badbeef", "DOT-0badbeef-c1")
def use_missing_expiry(b): use_setup(b, *HOLDER, expiry=None)
def use_bad_expiry(b): use_setup(b, *HOLDER, expiry="明天")
def use_wrong_version(b): use_setup(b, *HOLDER, version="v2")
def use_wrong_hash(b): use_setup(b, *HOLDER, h="b" * 64)

def stale_pass_after_resubmit(b):
    # v1 通過後又送審 v2，看板卻用 v1 的通過標完成
    add_event(b, event_id="DOT-a41f9e22-y1", task_id="GAME-T002", type="reviewed", session_id="DOT-a41f9e22",
              artifact_version="v1", result="通過")
    add_event(b, event_id="Claude-2b8d0f13-y2", task_id="GAME-T002", type="artifact_submitted",
              session_id="Claude-2b8d0f13", artifact_version="v2")
    set_row(b, "GAME-T002", 狀態="完成", 成果版本="v1")

def stale_pass_after_return(b):
    # v1 先通過、後又被退回，看板仍標完成
    add_event(b, event_id="DOT-a41f9e22-y3", task_id="GAME-T002", type="reviewed", session_id="DOT-a41f9e22",
              artifact_version="v1", result="通過")
    add_event(b, event_id="DOT-a41f9e22-y4", task_id="GAME-T002", type="reviewed", session_id="DOT-a41f9e22",
              artifact_version="v1", result="退回")
    set_row(b, "GAME-T002", 狀態="完成", 成果版本="v1")

def holder_without_claim(b):
    os.remove(os.path.join(b, "claims", "GAME-T004"))

results = [
    case("合法審查通過並結案清鎖", False, legit_pass),
    case("自審被抓到", True, self_review, "自審"),
    case("審查版本不是最新送審版本", True, wrong_version, "最新送審版本"),
    case("沒有審查就標完成", True, done_without_review, "找不到審查通過"),
    case("完成後仍留有效鎖（只警告）", False, done_keeps_lock, "結案清鎖"),
    case("依賴未完成就領取", True, dependency_skipped, "依賴"),
    case("重複的 event_id", True, duplicate_event, "重複"),
    case("持有者在對外操作開放時領用有效批准", False, use_by_holder),
    case("非持有者搶到 .use 檔，判定沒有執行資格", True, use_by_non_holder, "沒有執行資格"),
    case("批准缺有效期限", True, use_missing_expiry, "缺少「有效期限」"),
    case("批准有效期限格式錯誤", True, use_bad_expiry, "格式錯誤"),
    case("領用版本和批准版本不同", True, use_wrong_version, "版本不同"),
    case("內容雜湊和批准不同", True, use_wrong_hash, "內容雜湊"),
    case("新版本送審後沿用舊的通過紀錄", True, stale_pass_after_resubmit, "找不到審查通過"),
    case("通過後又被退回，仍標完成", True, stale_pass_after_return, "找不到審查通過"),
    case("看板有持有者但鎖檔被刪", True, holder_without_claim, "不存在"),
]
r = None
d = tempfile.mkdtemp(); b = os.path.join(d, "board"); shutil.copytree(EXAMPLE, b); late_return_resets_lease(b)
code, out = run(b)
ok = code == 0 and "GAME-T002：租約已" not in out
print(("通過" if ok else "失敗") + "：待審超時後退回，審查者重設租約，持有者不會被過期擋住")
if not ok: print(out)
shutil.rmtree(d)
results.append(ok)
print(f"共 {len(results)} 個情境，{sum(results)} 個通過")
sys.exit(0 if all(results) else 1)
