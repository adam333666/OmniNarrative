# M29 后端阶段 D：模型优先叙事生成切换

## 目标

把 `narrative_generator` 从纯规则式主路径升级为“模型网关优先、规则回退兜底”的双路径实现，同时保持现有 `result_builder` 与结果包契约稳定。

本阶段目标：
- 保留当前标题、摘要、脚本段落、镜头、备选项的输出接口不变。
- 在 `narrative_generator` 内部优先调用 `model_gateway` 生成叙事草案。
- 对模型输出进行最小解析与结构收敛。
- 当模型依赖缺失、模型输出为空或解析失败时，显式回退到现有规则实现。

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/multi-media/backend/app/services/model_gateway/service.py`
- `/home/admin2/smy/multi-media/backend/app/services/narrative_generator/service.py`
- `/home/admin2/smy/multi-media/backend/app/schemas/narrative_package.py`

## 适配原则

- 不修改 `result_builder` 对 `narrative_generator` 的返回签名。
- 模型输出在本阶段只承担“增强主路径”的责任，不承担完全自由生成整包结构的责任。
- 回退必须是显式、可验证、可测试的，不能在失败时产生半结构化脏数据。
- 若模型只成功生成部分内容，优先局部补洞并落回规则字段，而不是整次中断。

## 变更范围

### 后端服务
- 调整 `NarrativeGeneratorService`，引入模型网关请求与响应处理。
- 新增模型草案解析辅助逻辑。
- 保留原有规则生成逻辑作为 fallback 路径。

### 测试
- 新增 fake model gateway 成功路径测试。
- 新增 fallback 路径测试。
- 现有结果构建回归测试必须继续通过。

## 当前阶段明确不做

- 不在本阶段把模型输出直接扩展成完整 `NarrativePackage`。
- 不做复杂 prompt 模板资产化治理。
- 不引入真实外部模型依赖作为测试前提。

## 验证要求

- `python3 -m py_compile` 通过。
- 后端测试通过，至少覆盖 fake model gateway 成功路径、fallback 路径、现有结果构建回归。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口。
