# M5 主链路验证记录

## 目标

记录 M5 阶段的自动化验证与人工核对结果，确保 docs、代码与 git 提交保持一致。

## 自动化验证项

- Python 语法校验：已通过
  - 命令：`cd /home/admin2/smy/multi-media/backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/api/routes/config.py app/core/config.py app/schemas/trend_template.py app/services/trend_strategy/default_templates.py app/services/trend_strategy/repository.py app/services/trend_strategy/service.py tests/test_m5_trend_and_exports.py`
- pytest 最小测试集：已通过
  - 命令：`cd /home/admin2/smy/multi-media/backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m5_trend_and_exports.py`
  - 结果：`4 passed in 0.14s`
- CLI 趋势刷新脚本：已通过
  - 命令：`cd /home/admin2/smy/multi-media && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 scripts/trend_refresh.py`
  - 结果：成功刷新 5 个模板，并输出各平台摘要。

## 人工核对项

- 趋势模板读取接口与刷新接口返回结构符合 docs/api/m5_trend_validation_contract.md。
- trend_refresh.py 直接复用统一刷新服务，没有复制另一套模板逻辑。
- 结果页既有 M4 导出链路未被 M5 变更破坏。
- 趋势模板真值已从代码常量迁移到 backend/app/data/platform_trend_templates.json 文件仓储。

## 结果

- M5 最小闭环已完成：趋势模板可读取、可手动刷新、可通过内部 API 触发、可通过 CLI 触发。
- 自动化验证覆盖了输入校验、趋势模板读取与刷新、结果包结构、导出与 Video Payload。
- 当前阶段仍采用文件仓储作为一期简化方案，后续如进入 PostgreSQL 落地，可在不改变上层服务契约的前提下替换仓储实现。
