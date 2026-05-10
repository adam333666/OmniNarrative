# M40 LangGraph 化 Generation Orchestrator PoC 方案

## 1. 文档定位

本文档用于锁定 `P2` 第一项具体实施内容：

> 用成熟仓库 `langchain-ai/langgraph` 替换当前 `generation_pipeline/orchestrator.py`
> 中手写的串行执行编排逻辑，
> 让“阶段流转、节点执行、结果汇总”优先由成熟图编排框架驱动，
> 当前仓库只保留状态落库、事件记录、结果持久化与 API 胶水。

本文档受以下事实源约束：
- `docs/PRD.md`
- `docs/stage_records/stage_01_project_handoff_summary_v1.md`
- `docs/stage_records/stage_02_project_handoff_summary_v2.md`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
- `docs/architecture/m38_instructor_profile_parser_poc.md`
- `docs/architecture/m39_instructor_narrative_bundle_poc.md`
- `docs/research/p0_strict_glue_repo_selection_v1.md`
- `docs/changelog.md`

---

## 2. 当前问题

当前 `generation_pipeline/orchestrator.py` 仍主要依赖仓内手写串行编排：
- 手工顺序调用 `profile_parser`
- 手工顺序调用 `trend_strategy`
- 手工顺序调用 `narrative_generator`
- 手工顺序调用 `package_assembler`

这导致：
- 执行编排仍是本仓自写
- 阶段流转逻辑与业务调用逻辑混在一起
- 后续若要扩展重试、分支、条件路由，会继续加重本地编排代码

---

## 3. 上游仓库与准入结论

### 3.1 本轮主仓库

- 仓库：`langchain-ai/langgraph`
- 本地路径：`/home/admin2/smy/upstream-materials/langgraph`
- 固定版本：`ae76f33c`
- 许可证：MIT

### 3.2 本轮未作为主落地点的候选

- `pydantic/pydantic-ai`
- 本地路径：`/home/admin2/smy/upstream-materials/pydantic-ai`

暂不选其作为本轮主落地点的原因：
- 它更适合后续带工具、带依赖注入、带 durable agent 的智能执行深化
- 当前这一步是一个阶段清晰、固定顺序的 stateful workflow
- `LangGraph` 对“显式节点 + 显式边 + 图式编排”的贴合度更高

---

## 4. 本轮目标

本轮目标是把 `GenerationExecutionOrchestrator` 从“手写顺序执行器”改为“LangGraph 主路径”：

1. 用 `StateGraph` 表达当前四个核心执行节点
2. 用图编排替换手写顺序调用
3. 保持对现有 `store / coordinator / runner / result_repository` 的兼容
4. 不在本轮引入新的复杂条件分支，只做最小可运行替换

---

## 5. 接入边界

### 5.1 本仓允许保留的内容

- `GenerationExecutionState` 这样的本地状态 schema
- 节点内部对现有 service 的调用
- `generation_pipeline_store` 的阶段记录与失败记录
- `coordinator / runner / result_builder` 与现有 API 的对接

### 5.2 本仓不允许继续扩大的内容

- 不继续把节点顺序和状态更新写成新的本地串行大函数
- 不继续新增“另一套自写状态机”

---

## 6. 技术方案

### 6.1 图结构

本轮最小图结构为：

- `START -> parse_profiles -> adapt_trend -> generate_narrative -> assemble_package -> END`

各节点分别负责：
- `parse_profiles`
- `adapt_trend`
- `generate_narrative`
- `assemble_package`

### 6.2 状态承载

图状态中保存：
- `generation_id`
- `record`
- `audience_profile`
- `style_profile`
- `trend_summary`
- `title`
- `one_sentence_summary`
- `script_segments`
- `key_shots`
- `title_alternatives`
- `hook_alternatives`
- `result`

### 6.3 与现有胶水边界的关系

本轮不改：
- `GenerationPipelineStore`
- `GenerationMaterializationCoordinator`
- `GenerationExecutionRunner`
- `GenerationResultBuilder`

原因是：
- 这些模块当前已经承担“状态真值、后台启动、结果持久化、路由对接”的胶水角色
- 当前最应该去自写化的是“执行编排”本身

---

## 7. 环境与依赖说明

本轮为了让本地上游 `LangGraph` 真正可运行，已在当前宿主环境安装：
- `langgraph`
- `langgraph-checkpoint`
- `langgraph-prebuilt`
- `langgraph-sdk`
- `ormsgpack`

已观察到的环境风险：
- 安装过程中 `langchain-core` 被升级到 `1.2.22`
- 当前宿主里已有的 `langchain / langchain-openai / langchain-community / langchain-text-splitters` 对 `langchain-core<1.0.0` 有兼容性警告

本轮处理原则：
- 先把 `multi-media` 自身的 PoC 跑通
- 将该环境漂移明确记入 `changelog`
- 后续若需要长期稳定，应考虑把本项目隔离到独立虚拟环境

---

## 8. 验证口径

本轮完成后至少需要满足：

1. `GenerationExecutionOrchestrator.execute()` 已通过 LangGraph 图执行
2. 现有 `test_m35_generation_orchestrator.py` 仍通过
3. `test_m36_generation_execution_runner.py` 不被编排替换破坏
4. 失败路径仍会正确落 `FAILED` 事件

建议验证命令：
- `python3 -m py_compile backend/app/services/generation_pipeline/orchestrator.py`
- `pytest -q backend/tests/test_m35_generation_orchestrator.py backend/tests/test_m36_generation_execution_runner.py`

---

## 9. 完成标准

本轮完成标准定义为：
- `generation_pipeline/orchestrator.py` 已改为 LangGraph 主路径
- 现有 runner/coordinator/store 仍保持兼容
- tests 通过
- `docs/changelog.md` 已追加记录
- 有独立 Git 提交与本批变更对应
