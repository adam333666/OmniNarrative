# M30 后端阶段 E：生成状态持久化升级

## 目标

把 `generation_pipeline_store` 从单进程内存字典升级为数据库真值层驱动的持久化实现，在保持现有 `generate / status / result / export` API 契约不变的前提下，让生成记录可恢复、可审计、可跨重启读取。

本阶段目标：
- 引入 `generation_jobs` 数据模型，持久化保存生成请求快照与基础状态字段。
- 将阶段状态从纯时间推导升级为“显式阶段字段 + 受控推进写库”。
- 将 `generation_pipeline_store` 的 `create / get_record / get_status` 主路径切换到数据库 repository。
- 用显式测试覆盖“创建后可恢复读取”和“状态查询跨实例一致”两条关键路径。

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/multi-media/backend/app/db/repositories/trend_template_repository.py`
- `/home/admin2/smy/multi-media/backend/app/db/models/trend_template.py`
- `/home/admin2/smy/upstream-materials/full-stack-fastapi-template/backend/app/core/db.py`
- `/home/admin2/smy/upstream-materials/sqlalchemy/lib/sqlalchemy/orm/session.py`

## 为什么使用这些材料

- 当前项目已经在趋势模板真值层上采用 `SQLAlchemy model + repository + bootstrap` 的胶水方式，这一模式已经被本项目验证可用，继续沿用能够避免状态存储层出现第二套风格。
- `full-stack-fastapi-template` 提供的不是业务逻辑，而是“session factory + 数据访问边界 + 启动期建表”的成熟工程化模式，适合我们在不引入额外中间件的前提下扩展持久化层。
- SQLAlchemy 已经是项目固定技术栈的一部分，当前阶段用它扩展 `generation_jobs` 真值层，比自己写文件态或自制 KV 存储更符合胶水编程原则。

## 适配原则

- 不修改对前端暴露的 API 响应结构。
- 不在本阶段引入任务队列、后台 worker、Redis 或复杂状态机。
- 可以引入轻量 orchestration 层，但它仍运行在当前同步请求链中，不冒充真实后台 worker。
- 不做“数据库失败时静默回退内存态”的伪稳健实现，避免运行时真值漂移。
- 继续保留当前单进程受控推进策略，但推进结果要显式写回数据库真值层。

## 数据模型设计

新增表：`generation_jobs`

字段：
- `generation_id`：外部可见业务 ID，唯一约束。
- `request_payload`：原始 `CreationRequest` 快照，JSON 存储。
- `created_at`：生成创建时间，作为阶段推进的基准。
- `current_status`：当前整体状态真值。
- `current_stage`：当前阶段真值。
- `stage_message`：当前阶段说明。
- `failed`：失败标记。
- `timed_out`：超时标记。
- `failure_reason`：失败原因，可空。
- `completed_at`：结果构建完成时间，可空。
- `updated_at`：最后一次阶段推进时间。

当前阶段明确不做：
- 不持久化完整结果包。
- 不持久化每一步中间产物。
- 不记录细粒度事件流。
- 不引入真实后台 worker 主动驱动每一步执行。
- 不把结果构建入口长期兼任完整执行编排器，后续应继续向独立 orchestration 层收口。

## 实现顺序

1. 新增 `GenerationJobModel` 与 repository。
2. 把 `bootstrap_database()` 扩展到包含 `generation_jobs` 表。
3. 重写 `generation_pipeline_store`，让其通过 repository 读写生成记录。
4. 将 `result_builder` 末端接入显式阶段推进，保证只有结果真正落库后才写 `DONE`。
5. 在保持同步请求链前提下，把步骤执行与失败收口从 `result_builder` 中拆到独立 orchestrator。
6. 新增阶段 E 测试，覆盖创建、读取、状态推进、legacy 补列、orchestrator 编排和 404 路径。
7. 回归现有后端测试，确认外部链路无漂移。

## 边界条件与注意事项

- `request_payload` 必须按 `CreationRequest.model_dump()` 写入，读取时再恢复为 `CreationRequest`，不能让 SQLAlchemy 模型直接泄漏到业务层。
- `generation_id` 继续沿用当前 `gen_` 前缀格式，避免前端或日志引用失配。
- 自然状态推进仍允许参考 `created_at`，但显式推进后的阶段不能再被后续读取回退覆盖。
- 若仍保留自然状态推进兜底，其阶段顺序必须与真实执行链一致，避免 `status`/diagnostics 显示“叙事已生成”却还未完成趋势适配的假信号。
- `DONE` 只能在结果真正构建并落库后写入，不能仅由时间推导提前出现。
- 若未来进入更真实的异步任务链，本阶段的数据模型可以继续向“job status history / result snapshot”扩展，但当前不提前设计。

## 验证要求

- `python3 -m py_compile` 通过。
- 后端回归测试通过，至少覆盖阶段 E 新增测试与既有阶段 A-D 测试。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口。
