# 研究周报复盘

用于整理研究生每周的研究进展、证据和后续验证计划。项目目前可读取带稳定标识的 UTF-8 JSON 记录，按指定字段生成描述性统计，并为汇总标记数据修订号。

## 数据约定

示例记录为本地合成数据。`id` 是记录标识；`week`、`student`、`question`、`claim`、`evidence` 和 `status` 描述研究周报中的基本信息。`status` 当前可记录 `observed`、`interpreted`、`to_verify`。缺失值代表尚未观察或尚未填写，不等于数值零。日期使用 ISO 8601 格式。

## 使用与测试

需要 Python 3.11 或更新版本，不依赖外部服务。运行 `python -m unittest discover -s tests -v` 执行测试。将 `src` 加入 `PYTHONPATH` 后可导入 `research_review`；`examples/sample.json` 展示一组跨周的合成周报记录。

## 目录

- `src/research_review/facts.py`：读取并检查记录标识。
- `src/research_review/analysis.py`：按字段汇总数值观察。
- `src/research_review/reports.py`：构建带来源修订号的汇总。
- `examples/`：本地合成周报。
- `tests/`：输入、统计和报告行为测试。
