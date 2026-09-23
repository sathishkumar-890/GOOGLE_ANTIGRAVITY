import json

def main():
    transcript_path = r"C:\Users\User\.gemini\antigravity\brain\7f2dd70d-8dac-443f-87a4-db0069ebd5e1\.system_generated\logs\transcript.jsonl"
    with open(transcript_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "AKfycbwhOmBGplMtm5BIRP58sG6KOmazzrhmA5LypzMqoA17K_y6m96CteMRQ6sXnCidgaUZ" in line:
                try:
                    obj = json.loads(line)
                    source = obj.get("source")
                    step_type = obj.get("type")
                    content = str(obj.get("content", ""))[:200]
                    print(f"Line {idx} | Source: {source} | Type: {step_type}")
                    if "USER" in str(source):
                        print(f"  User said: {content}")
                    elif step_type == "USER_INPUT":
                        print(f"  User input: {content}")
                except Exception:
                    pass

if __name__ == "__main__":
    main()
