"""
Export Antigravity local chat conversations to clean, readable Markdown archives
so they can be tracked, organized, and synced to GitHub.
"""
import sqlite3
import os
import json
import re

OUTPUT_DIR = "04_CHAT_ARCHIVES"
DB_PATH = os.path.expanduser("~/.gemini/antigravity/conversation_summaries.db")
BRAIN_BASE = os.path.expanduser("~/.gemini/antigravity/brain")


def clean_name(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s).strip()
    return re.sub(r"[-\s]+", "_", s)


def export_all_chats():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT conversation_id, title, last_modified_time FROM conversation_summaries ORDER BY last_modified_time DESC"
    ).fetchall()
    conn.close()

    exported_count = 0
    for cid, title, last_mod in rows:
        t = title if title else "Untitled_Chat"
        safe_t = clean_name(t)
        out_path = os.path.join(OUTPUT_DIR, f"{safe_t}.md")
        log_file = os.path.join(BRAIN_BASE, cid, ".system_generated", "logs", "transcript.jsonl")

        if not os.path.exists(log_file):
            continue

        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        chat_entries = []
        for line in lines:
            try:
                d = json.loads(line)
            except Exception:
                continue
            msg_type = d.get("type")
            content = d.get("content", "")
            if msg_type == "USER_INPUT" and content:
                # Strip internal metadata wrappers
                content = re.sub(r"<USER_REQUEST>\s*", "", content)
                content = re.sub(r"\s*</USER_REQUEST>.*", "", content, flags=re.DOTALL)
                chat_entries.append(("USER", content.strip()))
            elif msg_type == "PLANNER_RESPONSE" and content:
                chat_entries.append(("ASSISTANT", content.strip()))

        with open(out_path, "w", encoding="utf-8") as out:
            out.write(f"# Chat Archive: {t}\n\n")
            out.write(f"- **Conversation ID**: `{cid}`\n")
            out.write(f"- **Last Modified**: {last_mod}\n")
            out.write(f"- **Total Messages**: {len(chat_entries)}\n\n---\n\n")
            for role, text in chat_entries:
                if role == "USER":
                    out.write(f"### 👤 User:\n{text}\n\n")
                else:
                    out.write(f"### 🤖 Antigravity Agent:\n{text}\n\n---\n\n")

        exported_count += 1
        print(f"Exported: {out_path} ({len(chat_entries)} messages)")

    print(f"\nDone! Exported {exported_count} chats to {OUTPUT_DIR}/")


if __name__ == "__main__":
    export_all_chats()
