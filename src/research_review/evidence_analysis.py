"""按研究问题和周次汇总可追溯观察证据。"""

from collections import defaultdict


def summarize_evidence(records):
    threads = defaultdict(list)
    for record in records:
        threads[(str(record["student"]), str(record["question"]))].append(record)
    result = {}
    for (student, question), entries in sorted(threads.items()):
        weeks = defaultdict(list)
        for entry in entries:
            weeks[str(entry["week"])].append(entry)
        series = []
        for week, rows in sorted(weeks.items()):
            observed = [row for row in rows if row["status"] == "observed"]
            evidence_refs = sorted({
                reference.strip()
                for row in observed
                for reference in str(row.get("evidence", "")).split(";")
                if reference.strip()
            })
            series.append({
                "week": week,
                "record_count": len(rows),
                "observations": len(observed),
                "interpretations": sum(row["status"] == "interpreted" for row in rows),
                "pending_verifications": sum(row["status"] == "to_verify" for row in rows),
                "evidence_references": evidence_refs,
            })
        result[f"{student}:{question}"] = {
            "weeks": series,
            "observed_weeks": sum(bool(row["evidence_references"]) for row in series),
            "weeks_without_linked_evidence": [row["week"] for row in series if not row["evidence_references"]],
        }
    return result
