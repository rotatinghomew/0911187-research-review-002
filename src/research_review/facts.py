"""读取并校验研究问题的周度证据记录。"""

import json
import math
from pathlib import Path


def load_records(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("记录文件必须包含数组")
    records = []
    seen = set()
    for position, record in enumerate(payload):
        required = ("id", "week", "student", "question", "claim", "status")
        if not isinstance(record, dict) or any(not record.get(field) for field in required):
            raise ValueError(f"第 {position + 1} 条记录缺少研究周报必填字段")
        if record["id"] in seen:
            raise ValueError(f"重复记录标识：{record['id']}")
        seen.add(record["id"])
        if record["status"] not in {"observed", "interpreted", "to_verify"}:
            raise ValueError(f"记录 {record['id']} 的 status 无效")
        value = record.get("value")
        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
        ):
            raise ValueError(f"记录 {record['id']} 的 value 必须是有限数值或空值")
        records.append(dict(record))
    return records
