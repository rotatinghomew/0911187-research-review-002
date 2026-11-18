"""按 cohort 和周次汇总有证据支持的研究指标。"""

from collections import defaultdict
from statistics import mean, median


def summarize_cohort_metrics(records):
    grouped = defaultdict(list)
    for record in records:
        grouped[(str(record.get("cohort", "未分组")), str(record["question"]))].append(record)

    summaries = {}
    for (cohort, question), entries in sorted(grouped.items()):
        weeks = defaultdict(list)
        for entry in entries:
            weeks[str(entry["week"])].append(entry)

        series = []
        for week, rows in sorted(weeks.items()):
            student_values = defaultdict(list)
            eligible_students = {str(row["student"]) for row in rows}
            for row in rows:
                value = row.get("value")
                evidence = str(row.get("evidence", "")).strip()
                if row["status"] != "observed" or not evidence or isinstance(value, bool):
                    continue
                if not isinstance(value, (int, float)):
                    continue
                student_values[str(row["student"])].append(float(value))

            per_student = [mean(values) for values in student_values.values()]
            series.append({
                "week": week,
                "eligible_students": len(eligible_students),
                "measured_students": len(per_student),
                "coverage": len(per_student) / len(eligible_students) if eligible_students else None,
                "mean": mean(per_student) if per_student else None,
                "median": median(per_student) if per_student else None,
            })
        summaries[f"{cohort}:{question}"] = series
    return summaries
