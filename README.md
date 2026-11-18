# 研究周报复盘

用于分析研究生围绕研究问题积累的周度观察、解释和待验证事项。项目读取本地合成周报，按学生与研究问题建立时间线，并汇总每周有据可查的观察及待验证覆盖。

## 数据约定

示例记录为本地合成数据。`id` 是记录标识；`week`、`student`、`question`、`claim`、`evidence` 和 `status` 描述周报信息。`status` 可记录 `observed`、`interpreted`、`to_verify`；观察的多个证据引用以分号分隔。当前分析可比较各周记录状态与证据覆盖，但尚未判断新证据对解释的支持/反驳关系，也未保存导师反馈及历史周报快照。

## 使用与测试

需要 Python 3.11 或更新版本，不依赖外部服务。运行 `PYTHONPATH=src python -m unittest discover -s tests -v` 执行测试。`examples/sample.json` 展示跨周合成周报；`research_review.facts` 校验记录，`research_review.evidence_analysis.summarize_evidence` 汇总周度证据覆盖，`research_review.analysis.summarize` 组织问题时间线，`research_review.reports.build_report` 生成带修订号的分析。

## 目录

- `src/research_review/facts.py`：检查研究周报身份和证据状态。
- `src/research_review/evidence_analysis.py`：按周汇总可追溯观察和证据覆盖。
- `src/research_review/analysis.py`：按问题建立证据进展时间线。
- `src/research_review/reports.py`：列出缺少证据链接的记录并绑定来源修订号。
- `examples/`：本地合成周报。
- `tests/`：输入、统计和报告行为测试。
