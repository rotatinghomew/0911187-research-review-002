"""沿研究问题整理每周观察、解释与待验证事项。"""

from collections import defaultdict


def summarize(records):
    groups = defaultdict(list)
    for record in records:
        key = (str(record["student"]), str(record["question"]))
        groups[key].append(record)
    result = {}
    for (student, question), entries in sorted(groups.items()):
        ordered = sorted(entries, key=lambda item: (item["week"], item["id"]))
        observations = [entry for entry in ordered if entry["status"] == "observed"]
        interpretations = [entry for entry in ordered if entry["status"] == "interpreted"]
        pending = [entry for entry in ordered if entry["status"] == "to_verify"]
        result[f"{student}:{question}"] = {
            "student": student,
            "question": question,
            "weeks": sorted({entry["week"] for entry in ordered}),
            "observations": [{"id": entry["id"], "claim": entry["claim"], "evidence": entry.get("evidence", "")} for entry in observations],
            "interpretations": [{"id": entry["id"], "claim": entry["claim"]} for entry in interpretations],
            "to_verify": [{"id": entry["id"], "claim": entry["claim"]} for entry in pending],
            "has_new_observation": bool(observations),
        }
    return result
