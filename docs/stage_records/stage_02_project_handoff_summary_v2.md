# 当前进度交接总说明 V2

## 1. 文档定位

本文档用于在本轮长时间连续开发、审查、补全、验收与 debug 工作结束后，为后续开发团队提供一份更细、更贴近当前仓库真实状态的暂停点说明。

它承接但不替代：
- `docs/PRD.md`
- `docs/changelog.md`
- `docs/stage_records/stage_01_project_handoff_summary_v1.md`

三者分工如下：
- `docs/PRD.md`：产品目标与范围真值。
- `docs/changelog.md`：逐批次变更留痕真值。
- `stage_01_project_handoff_summary_v1.md`：第一阶段总体交接摘要。
- 本文档：本轮对话结束时的详细暂停点说明，重点补充本轮后续新增的实现、修复、验证结果、当前边界与建议接手方式。

本文件同时吸收并取代以下三份历史阶段文档中仍然有效的内容：
- `docs/architecture/backend_fidelity_enhancement_plan_v1.md`
- `docs/architecture/alembic_workflow_v1.md`
- `docs/architecture/execution_plan_v1.md`

从本次整理完成后，这三份文档不再作为现行事实源保留，相关仍有效内容已并入本文件。

---

## 2. 本轮工作边界与最终收口判断

### 2.1 本轮实际工作边界

本轮后半段已经明确收紧了工作边界，原则是：
- 只做当前系统“已声明完成能力”的实现补全、验收、debug、稳定性收口。
- 不主动扩新产品范围。
- 不为未来阶段预建设计大块新系统。
- 允许做少量工程化整理，但前提是它直接服务于当前实现是否成立、是否可验、是否可排障。

因此，本轮后续工作的核心不再是“做更多功能”，而是：
- 修真实 bug。
- 修实现与测试/文档的漂移。
- 补当前链路最必要的排障与验证能力。
- 让现有原型系统达到一个清晰、可暂停、可交接的状态。

### 2.2 当前是否达到暂停点

当前已达到可安全暂停的状态。

判断依据：
- 当前前后端主链已经联通且有真实结构化输出。
- 当前状态链、导出链、诊断链和数据库真值层已经形成可核验闭环。
- 当前阶段顺序、接口契约、交接文档、PRD 和前端展示的主要漂移已经基本收口。
- 当前工作区干净，无待提交修改。
- 当前剩余事项已经从“必须修的真实问题”缩小到“后续如继续可再做的零星审计或下一阶段深化”。

---

## 3. 当前系统定位

### 3.1 当前系统不是什么

当前系统仍不是成熟生产系统，不应误判为：
- 完整后台任务系统
- 完整运维平台
- 真实外部模型与抓取链全部上线的正式系统
- 已彻底完成的长期可维护版本

### 3.2 当前系统是什么

当前系统更准确的定位是：

> 一个已具备真实主链、真实数据库真值层、结构化结果导出、轻量诊断能力、基础迁移治理、阶段状态持久化与第一轮高价值回归封口的“一期原型系统”。

也就是说，它已经明显超出“演示假链路”，但仍处于“原型强化完成、准备暂停或进入下一阶段”的状态。

---

## 4. 仍有效的历史计划内容整合

本节用于吸收此前三份历史文档中仍然有价值、但不值得继续单独保留的内容。

### 4.1 文档治理原则

当前继续有效的治理原则如下：
- `docs/` 仍是唯一事实来源区域。
- 需求以 `docs/PRD.md` 为唯一产品真值。
- 架构与阶段状态以 `docs/architecture/` 下当前仍保留文档为准。
- 变更历史以 `docs/changelog.md` 为唯一留痕真值。
- 每次结构性修改必须同步更新文档与 changelog，并保持 Git 提交语义一致。

这部分内容原先分散在 `execution_plan_v1.md` 中，现已并入本文件，不再需要保留独立总执行计划壳。

### 4.2 一期架构假设与工程边界

当前仍成立的工程边界如下：
- 前端负责输入、状态展示、结果展示和导出触发，不承载核心生成逻辑。
- 后端负责输入归一化、画像抽取、趋势策略、叙事生成、结果组装、导出派生与状态真值。
- 一期原型不引入 Celery、Temporal、Airflow、Redis 等重型任务基础设施。
- 一期继续使用轮询状态而不是流式传输。
- 一期系统允许“可选后台执行壳层”，但当前默认关闭自动执行，不把其表述为成熟任务系统。
- 一期固定技术栈仍为：Next.js、FastAPI、SQLAlchemy、Alembic、httpx、LiteLLM、Crawl4AI、Docker Compose。

这部分原本分散在 `execution_plan_v1.md` 与 `backend_fidelity_enhancement_plan_v1.md` 中，现统一以后端真实落地状态为准。

### 4.3 胶水原材料与接入原则

当前继续有效的原材料判断如下：
- LiteLLM 作为统一模型调用边界，业务层不直接散落 provider-specific 调用。
- Crawl4AI 作为趋势采集边界，而不是自写抓取底层。
- SQLAlchemy + Alembic 作为数据库真值层与 migration 治理基础。
- httpx 作为统一 HTTP 客户端。
- `full-stack-fastapi-template` 主要提供 session/migration/工程组织参考，不直接照搬业务结构。

当前继续有效的胶水原则如下：
- 尽量只写编排、适配、转换、落库、容错、验证。
- 不重写成熟底层能力。
- 不在业务 service 中泄漏第三方库的细碎细节。

### 4.4 Alembic 当前正式工作流

当前数据库 schema 治理方式已经明确为：

1. 优先 Alembic migration
2. 旧库兼容补表/补列
3. 仅在缺少 Alembic 运行包时，才回退到 `create_all`

当前 Alembic 相关核心文件：
- `alembic.ini`
- `backend/migrations/env.py`
- `backend/migrations/script.py.mako`
- `backend/migrations/versions/`

当前关键 revision：
- `20260325_091900_initialize_truth_tables.py`
- `20260327_103900_add_generation_job_status_columns.py`
- `20260327_111000_add_generation_job_events.py`

当前启动职责边界：
- Alembic 负责 schema 变更与 revision 留痕。
- `bootstrap_database()` 负责启动时调度 migration、执行有限兼容修复、再做 seed。
- seed 只负责当趋势模板表为空时导入模板，不负责 schema 变更。

当前最小命令规范：

```bash
# 查看当前 revision
DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_alembic_demo.db python3 -m alembic -c alembic.ini current

# 升级到最新 revision
DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_alembic_demo.db python3 -m alembic -c alembic.ini upgrade head

# 回滚到 base
DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_alembic_demo.db python3 -m alembic -c alembic.ini downgrade base
```

当前新增 revision 仍应遵守：
- 先改模型，再写/生成 revision
- 一个 revision 只处理一批强相关 schema 变化
- `upgrade()` 与 `downgrade()` 必须都可读、可执行
- 不在 revision 内塞业务 seed
- 旧库兼容优先文件化为 migration，而不是继续把临时分支堆进 bootstrap

### 4.5 后端忠实度补强阶段结论

此前 `backend_fidelity_enhancement_plan_v1.md` 的阶段计划，现在可以视为已基本落地到以下状态：
- M26：数据库真值层接入，已完成
- M27：趋势采集受控真实化，已完成第一轮
- M28：模型网关接入，已完成第一轮
- M29：模型优先叙事生成，已完成第一轮
- M30：生成状态持久化升级，已完成第一轮
- M31：验证与回归封口，已完成第一轮

因此该计划文档的主要价值已经从“指导实施”转为“历史路径说明”，当前已无必要继续单独保留。

---

## 5. 本轮已达成的全部关键工作

以下内容以“当前仓库真实状态”为准。

### 4.1 结果真值与导出链一致性

已完成：
- 为同一个 `generation_id` 持久化结果快照。
- `result / export/json / export/md / video-payload` 统一复用同一份结果真值。
- 避免同一任务多次读取时重复重算与结果漂移。

当前意义：
- 同一任务的结果、JSON 导出、Markdown 导出、Video payload 之间已形成共享真值。
- 结果链不再是“每个接口各算一遍”的不稳定状态。

核心位置：
- `backend/app/db/repositories/generation_result_repository.py`
- `backend/app/services/generation_pipeline/result_builder.py`

---

### 4.2 模型网关第一轮真实化治理

已完成：
- 接入 `litellm` 适配边界与 `model_gateway`。
- 建立 provider 配置缺失、provider unavailable、timeout、provider error、malformed response 等错误分类。
- 建立 fallback 语义、重试、timeout 与诊断字段。
- `narrative_generator` 已通过统一 `model_gateway` 取草案，再回退规则生成。

当前意义：
- 模型调用不再散在业务层。
- 当前即使模型不可用，也不会污染主链结构输出。

核心位置：
- `backend/app/integrations/llm/litellm_adapter.py`
- `backend/app/services/model_gateway/service.py`
- `backend/app/services/narrative_generator/service.py`

---

### 4.3 趋势模板真值层与趋势刷新收口

已完成：
- 趋势模板切到数据库真值层主路径。
- 趋势刷新具备手动触发与数据库写回。
- fallback 不再覆盖已有数据库真值。
- 允许部分来源失败但保留可用结果，避免全局被脏数据拖垮。

当前意义：
- 趋势链不再是纯返回值演示。
- 当前至少已经具备受控真实化的数据库写回能力。

核心位置：
- `backend/app/services/trend_strategy/service.py`
- `backend/app/services/trend_collector/service.py`
- `backend/app/services/trend_strategy/repository.py`

---

### 4.4 Alembic 接入与数据库启动治理

已完成：
- Alembic 已接入。
- 初始 schema 与后续新增表/列已有 revision 管理。
- bootstrap 已优先走 migration，并保留 legacy 兼容兜底。
- 启动时数据库 bootstrap 支持重试。
- 已补 roundtrip 回归。

当前意义：
- 数据库 schema 治理已经从“只靠 create_all”推进到“有 migration 基础”的状态。
- 当前更适合继续演进，而不是回到无治理状态。

核心位置：
- `alembic.ini`
- `backend/migrations/`
- `backend/app/db/bootstrap.py`
- `backend/tests/test_m32_bootstrap_resilience.py`
- `backend/tests/test_m33_alembic_cli_roundtrip.py`

---

### 4.5 显式阶段状态持久化

已完成：
- `generation_jobs` 具备显式字段：
  - `current_status`
  - `current_stage`
  - `stage_message`
  - `completed_at`
  - `updated_at`
- 状态读取不再只靠时间即时推导。
- 失败、超时、完成都能写库。

当前意义：
- 当前状态链已经具备基本审计价值。
- 状态接口不再只是“模拟展示”，而是数据库真值层的反映。

核心位置：
- `backend/app/db/models/generation_job.py`
- `backend/app/db/repositories/generation_job_repository.py`
- `backend/app/services/generation_pipeline/store.py`

---

### 4.6 结果构建末端从入口层剥离

已完成：
- 将末端步骤执行抽到独立 `orchestrator`。
- 将结果物化与并发锁抽到 `coordinator`。
- 将可选后台触发抽到 `runner`。
- `result_builder` 收缩为快照命中判断 + 协调层调用入口。

当前意义：
- 当前结果链内部职责已经比最初清晰得多。
- 后续如果要继续深化执行链，不必再把逻辑堆回 `result_builder`。

核心位置：
- `backend/app/services/generation_pipeline/orchestrator.py`
- `backend/app/services/generation_pipeline/coordinator.py`
- `backend/app/services/generation_pipeline/runner.py`
- `backend/app/services/generation_pipeline/result_builder.py`

---

### 4.7 轻量后台执行壳层

已完成：
- `generate` 创建任务后会尝试调用 `runner.submit(...)`。
- 但默认配置 `generation_auto_start_enabled = False`，不会误导为成熟后台系统。
- runner 已支持：
  - 惰性线程池创建
  - 生命周期 shutdown
  - inflight 去重
  - shutdown 清理 inflight

当前意义：
- 当前已经有“后台执行壳层”的基础形态。
- 但它仍是原型收口所需的最小实现，不应视为成熟 worker 系统。

核心位置：
- `backend/app/core/config.py`
- `backend/app/api/routes/creations.py`
- `backend/app/main.py`
- `backend/app/services/generation_pipeline/runner.py`

---

### 4.8 轻量任务事件轨迹与 diagnostics

已完成：
- 新增 `generation_job_events` 表。
- 记录创建、阶段推进、完成、失败、超时等事件。
- 新增受内网 key 保护的 diagnostics 接口：
  - `GET /api/v1/creations/{generation_id}/diagnostics`
- diagnostics 支持：
  - `event_type`
  - `limit`
  - `since`
  - `until`
  - `failed_only`

后来继续补强：
- 已补后台触发层事件：
  - `BACKGROUND_SUBMITTED`
  - `BACKGROUND_STARTED`
  - `BACKGROUND_DEDUPED`
  - `BACKGROUND_SKIPPED_DISABLED`
  - `BACKGROUND_SKIPPED_TERMINAL`

当前意义：
- 当前已具备不直连数据库也能排查主链问题的最小能力。
- 诊断链已经能区分“没启动、开始了、被去重、失败了”等不同情况。

核心位置：
- `backend/app/db/models/generation_job_event.py`
- `backend/app/db/repositories/generation_job_event_repository.py`
- `backend/app/api/routes/creations.py`
- `backend/tests/test_m34_generation_diagnostics.py`

---

### 4.9 状态诊断字段

已完成：
- `status` 响应已补入：
  - `created_at`
  - `updated_at`
  - `completed_at`
  - `total_elapsed_seconds`
  - `stage_elapsed_seconds`

当前意义：
- 当前状态页与排障链已经不仅知道“在哪一阶段”，还知道“总耗时”和“阶段耗时”。

核心位置：
- `backend/app/schemas/status.py`
- `frontend/lib/api-client/backend.ts`

---

### 4.10 主链顺序与展示顺序对齐

本轮后期收掉了多处真实漂移：
- 自然状态推进顺序与真实执行顺序不一致
- 前端生成状态页展示顺序仍是旧版
- PRD 中阶段顺序仍是旧版
- M2 契约和 M31 验证文档仍是旧版
- M3/M4 契约仍把 `DONE` 当成结果读取前置条件
- `generate` 响应的 `current_status` 使用硬编码而不是实际记录字段

当前结果：
- 后端真实执行顺序
- 状态接口语义
- 结果/导出契约
- 前端生成过渡页展示
- PRD 和交接文档

已经基本对齐到同一套阶段真值。

---

## 6. 本轮新增或强化的关键测试

### 已新增/强化的关键回归包括

- `backend/tests/test_m30_generation_store_persistence.py`
  - 显式阶段持久化
  - timeout/failed 状态
  - 事件轨迹
  - 自然推进止于 `PACKAGE_ASSEMBLING`
  - 自然推进顺序与真实执行顺序一致

- `backend/tests/test_m31_backend_regression_closure.py`
  - 趋势刷新写库
  - fallback 不覆写真值
  - `generate -> status -> result -> export -> video payload` 整链稳定性

- `backend/tests/test_m32_bootstrap_resilience.py`
  - migration/bootstrap 重试
  - fallback bootstrap
  - legacy 补表/补列

- `backend/tests/test_m33_alembic_cli_roundtrip.py`
  - `upgrade -> downgrade -> upgrade` CLI 回归

- `backend/tests/test_m34_generation_diagnostics.py`
  - diagnostics 鉴权
  - 事件过滤
  - 时间窗口过滤
  - failed only
  - 默认后台跳过事件

- `backend/tests/test_m35_generation_orchestrator.py`
  - orchestrator 阶段推进
  - orchestrator 失败收口

- `backend/tests/test_m36_generation_execution_runner.py`
  - coordinator 直接物化
  - runner 提交
  - 后台事件留痕
  - shutdown 清 inflight

---

## 7. 近期明确通过的验证

本轮后期我拿到过明确结束摘要的验证包括：

- `pytest -q tests/test_m30_generation_store_persistence.py`
  - `8 passed in 3.51s`

- `pytest -q tests/test_m30_generation_store_persistence.py tests/test_m36_generation_execution_runner.py::test_runner_shutdown_clears_inflight_generation_ids`
  - `9 passed in 4.86s`

- `pytest -q tests/test_m36_generation_execution_runner.py::test_runner_records_submission_start_and_dedup_events tests/test_m36_generation_execution_runner.py::test_runner_records_disabled_skip_event tests/test_m36_generation_execution_runner.py::test_runner_shutdown_clears_inflight_generation_ids`
  - `3 passed in 1.64s`

- `pytest -q tests/test_m35_generation_orchestrator.py`
  - `2 passed in 2.55s`

- `npm run build`（frontend）
  - 已明确通过
  - `/generating/[id]` 与 `/result/[id]` 已进入构建输出

### 关于仍有工具回传噪音的测试

当前仍有一类已知现象：
- 某些 `TestClient` 相关 pytest 在当前工具环境中，偶尔会出现“pytest 进程已退出，但结束摘要未完整回传”的情况。

重要判断：
- 这不等于测试逻辑本身挂死。
- 我在多轮核验中确认过，对应 pytest 进程多数情况下已经正常退出。
- 另外我也确认过没有残留 `generation-exec` 线程。

这意味着：
- 当前剩余噪音更偏工具回传层，而不是明显的应用级死锁。

---

## 8. 当前仓库真实状态

截至本文件落盘时：
- Git 工作区干净。
- 最近一组关键提交包括：
  - `802352c docs: align PRD stage order`
  - `2cbf7b5 fix: align generation status page order`
  - `a7684e5 docs: update status and validation contracts`
  - `b11dd80 fix: source generate status from persisted record`
  - `78995ba docs: align result and export contracts`
  - `c39fee3 fix: clear inflight runner state on shutdown`
  - `85abc22 test: align diagnostics event expectations`
  - `8104036 fix: align natural stage progression order`
  - `4e0c763 test: stabilize integration client lifecycle`
  - `e067558 feat: add background execution trail events`
  - `790ac95 feat: add optional generation execution runner`
  - `d362e86 refactor: extract generation execution orchestrator`

当前说明：
- 本轮“补全实现情况、验收、debug、收口”工作已经进入明确暂停点。
- 若继续工作，更适合开启下一阶段目标，而不是继续在当前阶段里做大规模深挖。

---

## 9. 当前边界与不要误判的点

### 8.1 不要误判为已经完成的内容

以下内容仍不应被误判为“成熟完成”：
- 真实生产级后台任务系统
- 真实生产级模型供应商治理
- 真实生产级趋势抓取体系
- 完整运维后台
- 完整可观测平台

### 8.2 当前已达到但需正确理解的内容

- 有后台执行壳层，但默认关闭自动执行。
- 有 diagnostics，但仍是轻量内部接口，不是完整运维平台。
- 有事件轨迹，但仍是最小可审计形态。
- 有 Alembic，但还不是“团队长期治理完全收口”的终局状态。
- 有前后端演示闭环，但系统总体仍是一期强化原型。

---

## 10. 对历史文档进一步精简的判断

### 10.1 关于这三份历史文档

本次已经完成整合并移除的三份文档：
- `backend_fidelity_enhancement_plan_v1.md`
- `alembic_workflow_v1.md`
- `execution_plan_v1.md`

删除它们的理由不是“这些内容没价值”，而是：
- 其中有效内容已经被当前真实实现吸收。
- 当前继续保留独立壳子，反而更容易让后续团队在多份计划文档之间来回比对。
- `current_progress_handoff_v2.md` 现在已经承接了它们仍然有效的结论、边界和操作原则。

### 10.2 关于大量 `m*` 文档是否需要整合

当前判断是：

不建议现在把所有 `m*` 文档继续大规模合并成一份。

原因：
- `m*` 文档按阶段拆分，仍然保留了较高的“问题来源可追溯性”。
- 它们记录的是每个阶段为什么做、怎么做、验证点是什么，这和总交接文档的职责不同。
- 如果现在强行把所有 `m*` 文档完全揉成一个大文档，信息密度会过高，反而不利于后续团队按模块定位。

当前更合理的策略是：
- 保留 `m*` 文档作为阶段索引和历史实现说明。
- 保留 `current_progress_handoff_v2.md` 作为“当前状态总说明”。
- 后续若要进一步精简，优先做“归档分层”，而不是继续做“一锅端式整合”。

### 10.3 后续如果还要继续精简，建议怎么做

建议采用三层结构，而不是只剩一层：

1. `PRD.md`
作用：产品真值

2. `current_progress_handoff_v2.md`
作用：当前状态总说明

3. `m*` 文档
作用：按阶段与模块保留的实现历史和专题说明

如果未来还要进一步瘦身，优先方案应是：
- 把明显已失效、且内容完全被 V2 覆盖的少量 `m*` 文档移入 `docs/archive/`
- 而不是现在就把全部 `m*` 文档继续揉成一个超长单文档

---

## 11. 如果后续团队继续，应如何开始

### 9.1 如果继续做“本阶段尾部收口”

当前只剩很少量工作可继续做，而且大多已非必须：
- 再做一轮零星事实源漂移搜索
- 在当前工具条件下继续观察 `TestClient` 类集成回归摘要回传问题

若不是必须，不建议继续在本阶段投入大量时间。

### 9.2 如果进入下一阶段

更合理的下一阶段方向应是：
- 后台执行链进一步真实化
- 模型网关真实 provider 治理深化
- 趋势采集真实化深化
- 部署与联调收口

这已经属于下一轮明确目标，而不是当前阶段的补全与 debug。

---

## 12. 建议的接手顺序

后续团队接手时建议按以下顺序读文档：

1. `docs/PRD.md`
2. `docs/stage_records/stage_01_project_handoff_summary_v1.md`
3. 本文档
4. `docs/api/m2_input_status_contract.md`
5. `docs/api/m3_result_contract.md`
6. `docs/api/m4_export_contract.md`
7. `docs/architecture/m30_backend_phase_e_generation_persistence.md`
8. `docs/architecture/m31_backend_phase_f_validation_closure.md`
9. `docs/changelog.md`

---

## 13. 最终结论

本轮对话结束时，`/home/admin2/smy/multi-media` 已从“可运行原型”进一步推进到“主链语义、状态顺序、结果真值、导出真值、诊断能力、迁移治理、交接文档和关键回归基本对齐”的暂停点。

当前最重要的事实不是“功能又增加了多少”，而是：
- 现有能力之间的漂移已经被大幅收口。
- 当前系统的完成情况比之前更容易被后续团队正确理解。
- 当前暂停点已经足够清晰，后续团队可以较低成本接手，而不必再靠聊天记录拼事实。
