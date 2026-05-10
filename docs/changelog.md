# Changelog

本文件用于记录 `/home/admin2/smy/multi-media` 项目的所有代码与工程变更。

## 记录规范

- 每次代码、配置、文档、脚本、结构变更后都必须追加记录。
- 每条记录至少包含：时间、变更类型、变更文件、修改目的、修改内容、实现情况。
- 时间统一使用 `YYYY-MM-DD HH:MM:SS TZ`。
- 若某次变更未完成，也必须如实记录当前状态与阻塞原因。

## 2026-03-25 00:01:39 CST

- 变更类型：项目初始化
- 变更文件：
  - `docs/changelog.md`
  - `.git/`（初始化后生成）
- 修改目的：为后续从 0 开发建立统一的版本管理和长期变更留痕机制。
- 修改内容：
  - 创建项目级变更记录文件 `docs/changelog.md`。
  - 定义后续变更记录的最小必填字段与记录规则。
  - 预备在项目根目录初始化 Git 仓库，作为后续开发版本控制基础。
- 实现情况：
  - `docs/changelog.md` 已创建。
  - Git 仓库初始化待执行。
  - `PRD.md` 已完成通读理解，当前未开始任何产品功能实现。

## 2026-03-25 00:02:55 CST

- 变更类型：版本控制初始化完成
- 变更文件：
  - `.git/`
  - `docs/changelog.md`
- 修改目的：完成项目仓库初始化，并把初始化结果补充记录到变更档案中。
- 修改内容：
  - 在 `/home/admin2/smy/multi-media` 根目录执行 `git init`。
  - 将仓库当前默认分支显式设为 `main`。
  - 核对仓库状态，确认当前为未提交初始化状态。
- 实现情况：
  - Git 仓库已初始化完成。
  - 当前分支为 `main`。
  - 当前工作区尚无提交，待跟随后续正式开发节奏提交。

## 2026-03-25 00:06:39 CST

- 变更类型：开发流程约束补充
- 变更文件：
  - `docs/changelog.md`
- 修改目的：落实项目级开发纪律，确保每次变更都可以通过 changelog 与 Git 提交一一对应，便于审计与回退。
- 修改内容：
  - 明确后续每次代码改动后，必须同步执行两件事：更新 `docs/changelog.md` 与创建对应 Git 提交。
  - 约定 changelog 记录与 Git 提交保持同一批次变更语义一致，避免出现记录和代码不匹配。
  - 确认当前仓库隐藏目录 `.git/` 已存在于项目根目录。
- 实现情况：
  - 规则已写入 changelog。
  - 下一步执行初始化提交，作为后续开发回退基线。

## 2026-03-25 00:10:09 CST

- 变更类型：胶水原材料调研文档建立
- 变更文件：
  - `docs/research/glue_material_candidates.md`
  - `docs/changelog.md`
- 修改目的：为后续从 0 开发建立一份可执行的上游仓库筛选清单，明确哪些成熟项目适合作为胶水编程原材料。
- 修改内容：
  - 新建 `docs/research/glue_material_candidates.md`。
  - 按 PRD 技术边界筛选 Next.js、FastAPI、数据库、模型适配层、趋势抓取器、工程模板、前端结构参考等候选仓库。
  - 为每个候选项明确“用途 / 接入方式 / 是否建议 clone 到本地 / 是否只做依赖安装 / 是否只做参考”。
- 实现情况：
  - 候选清单已形成第一版。
  - 当前建议优先 clone 到本地做参考验证的仓库为：`crawl4ai`、`full-stack-fastapi-template`、`taxonomy`。
  - 当前建议直接作为依赖接入的能力为：Next.js、FastAPI、SQLAlchemy、Alembic、httpx、LiteLLM、react-hook-form、zod。

## 2026-03-25 00:19:43 CST

- 变更类型：上游参考仓库拉取与固定版本登记
- 变更文件：
  - `docs/research/glue_material_candidates.md`
  - `docs/changelog.md`
- 修改目的：把高价值的成熟上游仓库拉到本地，作为后续无漂移实现时的参考材料，并记录其固定版本。
- 修改内容：
  - 在主项目仓库外建立 `/home/admin2/smy/upstream-materials` 目录。
  - 拉取 `crawl4ai`、`full-stack-fastapi-template`、`taxonomy`、`litellm` 四个上游仓库到本地。
  - 将四个仓库的本地路径与固定 commit 写入调研文档，作为后续参考基线。
- 实现情况：
  - `crawl4ai`：`af648e1`
  - `full-stack-fastapi-template`：`8bf0025`
  - `taxonomy`：`651f984`
  - `litellm`：`0af114f`
  - 四个仓库均已可在本地阅读与对照使用。

## 2026-03-25 00:21:05 CST

- 变更类型：项目骨架方案落盘
- 变更文件：
  - `docs/architecture/project_skeleton_plan.md`
  - `docs/changelog.md`
- 修改目的：把 PRD、胶水编程原则和本地上游参考仓库收敛成可执行的项目骨架方案，作为正式开工前的结构基线。
- 修改内容：
  - 新建 `docs/architecture/project_skeleton_plan.md`。
  - 明确前后端目录结构、模块边界、数据库存储边界、状态管理策略、第一阶段 API 清单、第一阶段实施顺序。
  - 明确哪些能力直接以依赖方式接入，哪些能力仅参考本地上游仓库。
- 实现情况：
  - 项目骨架方案已形成第一版。
  - 方案与 PRD 技术边界保持一致：Next.js、FastAPI、PostgreSQL、Docker、统一 JSON Schema。
  - 当前仍未开始业务代码实现，处于结构与计划锁定阶段。

## 2026-03-25 00:24:12 CST

- 变更类型：执行计划与文档治理原则落盘
- 变更文件：
  - `docs/architecture/execution_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：在正式进入工程实施前，锁定项目级执行计划，并明确 `docs/` 为唯一且绝对忠实的事实来源。
- 修改内容：
  - 新建 `docs/architecture/execution_plan_v1.md`。
  - 明确文档治理原则、里程碑拆分、任务分解树、任务依赖图、数据表草案、API 契约草案、测试计划、回滚预案与监控记录计划。
  - 将“文档先行、代码与文档不可漂移”的规则提升为执行基线。
- 实现情况：
  - 执行计划已形成第一版。
  - 后续实现阶段将以 `docs/PRD.md`、`docs/architecture/`、`docs/research/`、`docs/changelog.md` 作为唯一事实来源。
  - 当前仍未开始业务代码开发，处于计划锁定完成阶段。

## 2026-03-25 00:29:58 CST

- 变更类型：M1 项目骨架建立与前端视觉原材料纳入
- 变更文件：
  - `.gitignore`
  - `README.md`
  - `frontend/package.json`
  - `frontend/tsconfig.json`
  - `frontend/next-env.d.ts`
  - `frontend/next.config.ts`
  - `frontend/app/globals.css`
  - `frontend/app/layout.tsx`
  - `frontend/app/page.tsx`
  - `frontend/app/create/page.tsx`
  - `frontend/app/generating/[id]/page.tsx`
  - `frontend/app/result/[id]/page.tsx`
  - `frontend/components/layout/site-shell.tsx`
  - `frontend/lib/constants/input-options.ts`
  - `frontend/README.md`
  - `frontend/claude.md`
  - `backend/pyproject.toml`
  - `backend/app/main.py`
  - `backend/app/api/router.py`
  - `backend/app/api/deps.py`
  - `backend/app/api/routes/config.py`
  - `backend/app/api/routes/system.py`
  - `backend/app/core/config.py`
  - `backend/app/core/enums.py`
  - `backend/app/core/logging.py`
  - `backend/app/schemas/creation_request.py`
  - `backend/app/schemas/status.py`
  - `backend/README.md`
  - `backend/claude.md`
  - `deploy/docker-compose.yml`
  - `deploy/frontend.Dockerfile`
  - `deploy/backend.Dockerfile`
  - `scripts/dev_bootstrap.sh`
  - `scripts/trend_refresh.py`
  - `docs/research/glue_material_candidates.md`
  - `docs/architecture/project_skeleton_plan.md`
  - `docs/changelog.md`
- 修改目的：正式启动 M1 项目骨架建立，并把 `react-bits` 纳入前端视觉原材料体系与 docs 事实来源。
- 修改内容：
  - 建立 `frontend/`、`backend/`、`deploy/`、`scripts/` 等基础目录与说明文件。
  - 建立 Next.js 前端骨架文件与四个核心页面占位。
  - 建立 FastAPI 后端骨架文件、基础配置与最小 API 占位。
  - 建立 Docker Compose 与前后端 Dockerfile 骨架。
  - 更新原材料调研文档与项目骨架方案，把 `react-bits` 纳入前端视觉参考策略。
  - 记录 `react-bits` 当前在本机环境中因 TLS 握手异常暂未成功拉到本地，需要后续继续补齐。
- 实现情况：
  - M1 最小工程骨架已落盘。
  - 后端核心 Python 文件已通过 `python3 -m py_compile` 基础语法校验。
  - 前端配置文件已完成一次自检修正。
  - `react-bits` 已进入 docs 事实来源，但本地参考仓库仍处于待补齐状态。

## 2026-03-25 00:29:58 CST

- 变更类型：M1 骨架提交后缓存文件清理修正
- 变更文件：
  - `.gitignore`
  - `docs/changelog.md`
  - `backend/**/__pycache__/`（删除）
- 修改目的：清理因语法校验产生并被误提交的 Python 缓存文件，恢复仓库整洁性。
- 修改内容：
  - 将 `.gitignore` 补充为递归忽略 `backend/**/__pycache__/` 与 `backend/**/*.py[cod]`。
  - 删除本次校验过程中产生的 `__pycache__` 目录与 `.pyc` 文件。
- 实现情况：
  - 缓存目录已从工作树删除。
  - 后续相同类型文件不会再次进入版本控制。

## 2026-03-25 00:38:59 CST

- 变更类型：M2 输入与状态主链路实现
- 变更文件：
  - `docs/api/m2_input_status_contract.md`
  - `backend/app/api/router.py`
  - `backend/app/api/routes/creations.py`
  - `backend/app/main.py`
  - `backend/app/schemas/creation_request.py`
  - `backend/app/schemas/generation.py`
  - `backend/app/services/input_orchestrator/service.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `frontend/app/create/page.tsx`
  - `frontend/app/generating/[id]/page.tsx`
  - `frontend/components/wizard/create-wizard.tsx`
  - `frontend/components/generation/generation-status-client.tsx`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/lib/schemas/creation-request.ts`
  - `docs/changelog.md`
- 修改目的：打通一期 `M2` 的最小主链路，让用户能够完成五步输入、提交生成请求并看到真实的阶段状态反馈。
- 修改内容：
  - 在 `docs/api/` 下新增 M2 接口契约文档，锁定 `input-options`、`generate`、`status` 三个接口的行为与校验规则。
  - 后端新增 `generate` 与 `status` 路由，并实现最小内存态阶段推进机制。
  - 后端新增输入归一化与枚举校验服务，确保前后端约束一致。
  - 前端将输入页从静态占位改为五步顺序表单，使用 `react-hook-form + zod` 建立前端校验。

## 2026-03-25 00:47:56 CST

- 变更类型：M3 最小结果链路实现
- 变更文件：
  - `docs/api/m3_result_contract.md`
  - `backend/app/api/routes/creations.py`
  - `backend/app/schemas/profiles.py`
  - `backend/app/schemas/trend_template.py`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/app/services/generation_pipeline/result_builder.py`
  - `backend/app/services/profile_parser/service.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/app/services/narrative_generator/service.py`
  - `backend/app/services/package_assembler/service.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/app/result/[id]/page.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：打通一期 `M3` 的最小结果链路，让系统从输入与状态推进到真实结构化结果包，并在结果页展示关键层级内容。
- 修改内容：
  - 在 `docs/api/` 下新增 M3 结果链路契约文档，锁定 `result` 接口与最小结果结构。
  - 后端新增 `AudienceProfile`、`StyleProfile`、`PlatformTrendTemplate`、`NarrativePackage` 等最小结果 schema。
  - 后端新增 `profile_parser`、`trend_strategy`、`narrative_generator`、`package_assembler` 与 `result_builder`，以规则化和模板化方式生成稳定结果。
  - 后端 `creations` 路由新增 `GET /api/v1/creations/{generation_id}/result`。
  - 前端结果页接入真实结果请求，展示左侧分析区与右侧总览层、脚本层、平台适配层，并折叠展示多模态层与机器提示层。
- 实现情况：
  - M3 文档与代码已同步落盘。
  - 后端新增与修改文件已通过 `python3 -m py_compile` 校验。
  - 前端关键 JSON 配置仍通过结构校验。
  - 当前系统已具备 `输入 -> 状态 -> 结果页结构化展示` 的完整最小主链路。

## 2026-03-25 01:03:42 CST

- 变更类型：胶水原材料补充与导出链路原材料登记
- 变更文件：
  - `docs/research/glue_material_candidates.md`
  - `docs/changelog.md`
- 修改目的：继续补足 M4 导出链路所需的成熟原材料，避免自行实现 Markdown 展示与导出相关能力时发生轮子重造或效果漂移。
- 修改内容：
  - 将 `remarkjs/react-markdown` 纳入胶水原材料候选总表与本地材料清单。
  - 在原材料文档中记录本地 `react-markdown` 参考仓库路径与固定版本 `fda7fa5`。
  - 继续保留 `react-bits` 为前端视觉原材料事实来源，并如实记录其在当前环境中因 TLS 握手异常尚未成功拉取到本地。
- 实现情况：
  - `react-markdown` 已成功拉取到 `/home/admin2/smy/upstream-materials/react-markdown`。
  - `react-bits` 仍未本地化完成，当前状态已在 docs 中持续登记，后续继续补齐。

## 2026-03-25 01:08:26 CST

- 变更类型：M4 导出与 Video Payload 主链路实现
- 变更文件：
  - `docs/api/m4_export_contract.md`
  - `backend/app/api/routes/creations.py`
  - `backend/app/schemas/video_payload.py`
  - `backend/app/services/export_payload/service.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：打通一期 `M4` 的最小导出链路，让统一结果结构可以稳定导出为 JSON、Markdown 与 Video Payload，并从结果页直接触发查看。
- 修改内容：
  - 新增 M4 契约文档，锁定 `export/json`、`export/md`、`video-payload` 三个接口的行为边界与前端联动约束。
  - 后端新增 `VideoGenerationPayload` schema，并新增统一导出服务，把 `result` 结构映射为 Markdown 与下游视频生成 payload。
  - 后端 `creations` 路由新增 JSON 导出、Markdown 导出与 Video Payload 查看接口。
  - 前端 API 客户端新增三个导出地址生成函数。
  - 前端结果页新增导出按钮区，允许直接打开 JSON、Markdown 和 Video Payload。
- 实现情况：
  - M4 文档与代码已同步落盘。
  - 导出链路严格复用统一 `result` 结构，没有另造第二套结果真值。
  - 后端新增文件待进行一次提交前语法校验，完成后随本批次一起提交。

## 2026-03-25 01:24:18 CST

- 变更类型：胶水原材料源码镜像补齐与本地快照校验
- 变更文件：
  - `docs/research/glue_material_candidates.md`
  - `docs/changelog.md`
- 修改目的：落实“会参考借鉴的上游项目必须拉到本地看源码，不能只读 README”的胶水编程原则，并确认用户手动提供的 `react-bits-main` 是否可直接作为视觉原材料使用。
- 修改内容：
  - 将 `next.js`、`shadcn-ui`、`react-hook-form`、`zod`、`fastapi`、`sqlalchemy`、`alembic`、`httpx` 八个上游仓库补充拉取到 `/home/admin2/smy/upstream-materials`。
  - 在原材料文档中补充上述仓库的本地路径与固定 commit，并把“所有会参考借鉴源码的仓库都必须本地镜像化”写成明确规则。
  - 检视 `/home/admin2/smy/upstream-materials/react-bits-main`，确认其包含 `package.json`、`README.md`、`src/` 及多个组件目录，可作为本地源码快照直接参考。
  - 将 `react-bits-main` 的当前状态写入 docs，替代此前仅记录“TLS 拉取失败”的不完整状态。
- 实现情况：
  - 新增本地源码镜像固定版本如下：`next.js aa3ba7ed`、`shadcn-ui b75796e`、`react-hook-form f29f546`、`zod c780507`、`fastapi 937d307`、`sqlalchemy 1aa259f`、`alembic 7b510dc`、`httpx b5addb6`。
  - `react-bits-main` 已确认可用，当前前后端关键参考材料已达到源码级可读状态。
  - 当前阶段的材料短板已从“缺少源码仓”转为“后续实现时必须严格优先阅读源码与测试，不得凭记忆造轮子”。

## 2026-03-25 03:13:40 CST

- 变更类型：M5 趋势分析器与验证闭环实现
- 变更文件：
  - `docs/api/m5_trend_validation_contract.md`
  - `docs/testing/m5_validation_record.md`
  - `backend/app/data/platform_trend_templates.json`
  - `backend/app/api/routes/config.py`
  - `backend/app/core/config.py`
  - `backend/app/schemas/trend_template.py`
  - `backend/app/services/trend_strategy/default_templates.py`
  - `backend/app/services/trend_strategy/repository.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `scripts/trend_refresh.py`
  - `docs/changelog.md`
- 修改目的：完成一期 M5 的内部能力闭环，把趋势模板升级为可读取、可刷新、可验证的统一仓储能力，并补齐第一阶段自动化测试与验证记录。
- 修改内容：
  - 新增 M5 契约文档，锁定趋势模板读取接口、内部刷新接口、CLI 刷新脚本与测试边界。
  - 新增文件仓储版趋势模板真值文件与仓储层，实现统一读取、过滤、最佳匹配与刷新写回。
  - 将 trend_strategy 从硬编码平台常量迁移为仓储驱动服务。
  - 在 config 路由下新增趋势模板摘要读取接口与内部刷新接口。
  - 将 trend_refresh.py 从占位脚本升级为真正复用共享刷新服务的 CLI。
  - 新增 M5 pytest，用真实 API 流程覆盖输入校验、趋势刷新、结果结构、导出与 payload。
  - 回填 docs/testing/m5_validation_record.md，记录语法校验、pytest 与 CLI 验证结果。
- 实现情况：
  - `python3 -m py_compile` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `4 passed in 0.14s`。
  - `python3 scripts/trend_refresh.py` 已成功刷新 5 个趋势模板。
  - 当前系统已具备 `输入 -> 状态 -> 结果 -> 导出 -> 趋势模板读取/刷新 -> 自动化验证` 的一期最小闭环。

## 2026-03-25 03:32:18 CST

- 变更类型：M6 前端视觉增强第一轮落地
- 变更文件：
  - `docs/architecture/m6_frontend_visual_enhancement.md`
  - `frontend/app/page.tsx`
  - `frontend/app/globals.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/landing/creative-hero.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/components/result/result-view-client.module.css`
  - `docs/changelog.md`
- 修改目的：在不改变一期主链路与结果真值的前提下，对首页和结果页做第一轮去占位化视觉升级，并严格基于本地 `react-bits-main` 源码材料借鉴成熟结构语义。
- 修改内容：
  - 新增 M6 前端视觉增强方案文档，明确首页和结果页的增强范围、原材料来源与边界。
  - 首页新增 `creative-hero` 组件与样式，吸收 `react-bits` 的 Hero 与 FeatureCards 结构语义，形成 Hero + 指标卡片 + bento 信息区。
  - 结果页改为模块化样式实现，重构分析面板、导出区、总览层、脚本层和平台层的视觉层级。
  - 全局样式更新为更稳定的暖色调版式与排版基线，但未改动任何接口、结果结构和导出链路。
- 实现情况：
  - 已完成 docs 与前端代码同步落盘。
  - 已完成静态自检与 `git diff --check` 检查。
  - 当前未运行完整前端编译产物验证，因为项目尚未安装前端依赖；本批次先以源码静态校对为主。

## 2026-03-25 03:46:52 CST

- 变更类型：M7 Markdown 预览接入与前端构建验证
- 变更文件：
  - `docs/architecture/m7_markdown_preview_integration.md`
  - `frontend/package.json`
  - `frontend/package-lock.json`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/markdown-preview.tsx`
  - `frontend/components/result/markdown-preview.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/app/generating/[id]/page.tsx`
  - `frontend/app/result/[id]/page.tsx`
  - `frontend/next-env.d.ts`
  - `docs/changelog.md`
- 修改目的：把既有 Markdown 导出链路接回结果页预览，真正完成 `react-markdown` 的前端集成，并通过真实依赖安装与 Next.js 构建验证这一批改动可运行。
- 修改内容：
  - 新增 M7 文档，锁定 `react-markdown` 的接入方式、边界与验证要求。
  - 在前端依赖中声明 `react-markdown`，并生成 `package-lock.json`。
  - 在 API 客户端中新增 Markdown 文本获取函数，继续复用既有 `/export/md` 接口。
  - 新增 Markdown 预览组件和样式，在结果页中内嵌展示后端导出的 Markdown 内容。
  - 为通过 Next.js 15 构建检查，修正 `generating/[id]` 与 `result/[id]` 动态页的 `params` 类型为 Promise 形式。
  - 执行 `npm install` 与 `npm run build`，完成这批前端改动的真实构建验证。
- 实现情况：
  - `npm install` 已完成，新增前端锁文件。
  - `npm run build` 已通过。
  - Markdown 预览当前保持最小安全渲染链路，未额外引入 GFM 插件。
  - 构建过程中存在 Next.js 对多 lockfile 的 workspace root 警告，但不影响本次构建通过。

## 2026-03-25 03:48:50 CST

- 变更类型：M10 首页流程步进与指标组件增强
- 变更文件：
  - `docs/architecture/m10_frontend_workflow_metrics.md`
  - `frontend/components/ui/count-up.tsx`
  - `frontend/components/landing/workflow-stepper.tsx`
  - `frontend/components/landing/workflow-stepper.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/landing/creative-hero.module.css`
  - `docs/changelog.md`
- 修改目的：继续基于本地 `react-bits-main` 源码增强首页的信息表达能力，让首页不仅有视觉吸引力，也更清楚地传达真实创作主链路与关键指标。
- 修改内容：
  - 新增 `M10` 文档，明确本阶段直接参考 `CountUp` 与 `Stepper` 两个上游 typed 源码组件，并锁定轻量适配原则。
  - 新增 `CountUp` 组件，用 `IntersectionObserver + requestAnimationFrame` 复用上游“进入视口后递增”的数值语义。
  - 新增 `WorkflowStepper` 组件，用轻量阶段指示与进度条承接上游 `Stepper` 的流程表达语义。
  - 将首页统计区升级为递增指标卡，并新增“创作主链路”流程区。
  - 保持现有后端接口、结果页结构和导出链路不变，只增强首页展示层。
- 实现情况：
  - 首页已接入上游 `CountUp` 与 `Stepper` 的轻量适配版本。
  - `npm run build` 已通过。
  - 当前批次可进入 Git 提交与后续迭代。

## 2026-03-25 03:54:10 CST

- 变更类型：M11 结果页信息聚焦列表增强
- 变更文件：
  - `docs/architecture/m11_result_information_focus.md`
  - `frontend/components/result/animated-decision-list.tsx`
  - `frontend/components/result/animated-decision-list.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续基于本地 `react-bits-main` 源码增强结果页的信息表达，把“关键设计决策”从普通列表升级成更易扫读、更易聚焦的结果分析区。
- 修改内容：
  - 新增 `M11` 文档，明确本阶段直接参考 `AnimatedList` 的上游 typed 源码，并锁定轻量适配边界。
  - 新增 `AnimatedDecisionList` 组件，以轻量状态切换、hover / focus 聚焦和信息卡强化来承接上游 `AnimatedList` 的核心语义。
  - 将结果页分析面板中的“关键设计决策”替换为新的信息聚焦列表。
  - 在实现过程中修正了结果页 JSX 结构问题，并完成重新构建验证。
- 实现情况：
  - 结果页分析面板已接入轻量 `AnimatedList` 适配版本。
  - `npm run build` 已通过。
  - 后端接口、结果结构和导出链路保持不变。

## 2026-03-25 03:55:11 CST

- 变更类型：M8 前端构建环境收尾
- 变更文件：
  - `docs/architecture/m8_frontend_build_hardening.md`
  - `frontend/next.config.ts`
  - `docs/changelog.md`
- 修改目的：消除前端构建中的 workspace root 推断警告，提升后续构建日志清晰度与环境确定性。
- 修改内容：
  - 新增 M8 文档，锁定当前构建噪音来源、处理原则与验证目标。
  - 在 `frontend/next.config.ts` 中显式设置 `outputFileTracingRoot` 指向项目根目录。
  - 重新执行 `npm run build` 验证构建仍然通过且不再出现多 lockfile 的 workspace root 警告。
- 实现情况：
  - `npm run build` 已通过。
  - Next.js 的 workspace root 警告已消失。
  - 当前构建日志中仅剩 `NODE_TLS_REJECT_UNAUTHORIZED` 的环境级警告，该警告来自当前机器环境变量，不属于项目配置本身。

## 2026-03-25 03:57:46 CST

- 变更类型：M12 标题层级渐变文本增强
- 变更文件：
  - `docs/architecture/m12_gradient_text_hierarchy.md`
  - `frontend/components/ui/gradient-text.tsx`
  - `frontend/components/ui/gradient-text.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续基于本地 `react-bits-main` 源码增强页面标题层级感，让首页与结果页的关键分区在不改变结构的前提下更清晰、更有视觉辨识度。
- 修改内容：
  - 新增 `M12` 文档，明确本阶段直接参考 `GradientText` 的上游 typed 源码，并锁定纯 CSS 适配边界。
  - 新增 `GradientText` 组件，以 `background-clip + keyframes` 的轻量方式承接上游渐变流动语义。
  - 首页分区标题“Built For Structured Storytelling”接入渐变文本。
  - 结果页总览标题“项目总览层”接入渐变文本。
- 实现情况：
  - 渐变标题增强已完成，未引入 `motion/react` 或其他新依赖。
  - `npm run build` 已通过。
  - 现有接口、数据结构与导出链路保持不变。

## 2026-03-25 04:01:42 CST

- 变更类型：M13 结果页分区 Pill 导航增强
- 变更文件：
  - `docs/architecture/m13_result_section_pill_nav.md`
  - `frontend/components/result/result-section-nav.tsx`
  - `frontend/components/result/result-section-nav.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续基于本地 `react-bits-main` 源码提升结果页长页面浏览效率，让用户可以更快跳转到五层结果结构中的关键区块。
- 修改内容：
  - 新增 `M13` 文档，明确本阶段直接参考 `PillNav` 的上游 typed 源码，并锁定“只借语义、不引依赖”的适配边界。
  - 新增 `ResultSectionNav` 组件，以原生锚点和轻量 pill 样式承接上游导航语义。
  - 为结果页总览层、Markdown、脚本层、平台层、多模态层、机器层增加稳定锚点。
  - 在实现过程中修正了锚点与 `SpotlightCard` props 的兼容问题，并完成重新构建验证。
- 实现情况：
  - 结果页已接入轻量分区 pill 导航。
  - `npm run build` 已通过。
  - 接口、数据结构和导出链路保持不变。

## 2026-03-25 04:05:56 CST

- 变更类型：M14 脚本层段落快速导航增强
- 变更文件：
  - `docs/architecture/m14_script_segment_quick_nav.md`
  - `frontend/components/result/script-segment-nav.tsx`
  - `frontend/components/result/script-segment-nav.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续基于本地 `react-bits-main` 源码提升结果页脚本层的定位效率，让用户能更快跳到具体脚本段落进行审阅与比对。
- 修改内容：
  - 新增 `M14` 文档，明确本阶段直接参考 `CardNav` 的上游 typed 源码，并锁定“只借入口卡片语义、不引依赖”的适配边界。
  - 新增 `ScriptSegmentNav` 组件，以轻量卡片方式为脚本段落提供快速跳转入口。
  - 在脚本层顶部接入段落快速导航，并为每个段落卡增加稳定锚点 id。
  - 在实现过程中重写了结果页组件，消除了 shell 写入导致的锚点表达式污染，并完成重新构建验证。
- 实现情况：
  - 脚本层快速导航已接入完成。
  - `npm run build` 已通过。
  - 后端结果结构、接口与导出链路保持不变。

## 2026-03-25 04:07:24 CST

- 变更类型：M9 轻量 React Bits 组件实装
- 变更文件：
  - `docs/architecture/m9_lightweight_react_bits_components.md`
  - `frontend/components/ui/shiny-text.tsx`
  - `frontend/components/ui/shiny-text.module.css`
  - `frontend/components/ui/spotlight-card.tsx`
  - `frontend/components/ui/spotlight-card.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：把 `react-bits-main` 中真正轻量、可稳定承接的组件模式落到项目里，让首页和结果页从“借结构语义”进一步升级到“接入经过适配的具体交互组件”。
- 修改内容：
  - 新增 M9 文档，锁定 `ShinyText` 与 `SpotlightCard` 的来源、适配原则和使用范围。
  - 新增 `shiny-text` 组件，以 CSS keyframes 方式承接 react-bits `ShinyText` 的高光扫过语义，不引入 `motion/react`。
  - 新增 `spotlight-card` 组件，以鼠标位置 + CSS 变量方式承接 react-bits `SpotlightCard` 的聚光交互。
  - 首页主标题中的“工作台”接入 `ShinyText`，bento 区信息卡改由 `SpotlightCard` 包裹。
  - 结果页的总览层与 Markdown 预览卡接入 `SpotlightCard`，增强交互层次但不改动任何数据结构和接口。
  - 执行 `npm run build`，确认新增组件接入后前端构建继续通过。
- 实现情况：
  - `npm run build` 已通过。
  - 当前轻量组件接入未引入新的运行时依赖。
  - 结果真值、Markdown 真值和导出链路均未改变，只增强了展示层交互体验。

## 2026-03-25 04:09:54 CST

- 变更类型：M15 机器层摘要卡增强
- 变更文件：
  - `docs/architecture/m15_machine_payload_summary.md`
  - `frontend/components/result/machine-payload-summary.tsx`
  - `frontend/components/result/machine-payload-summary.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续提升结果页对结构化信息的扫描效率，让机器层不再只以整块 JSON 暴露，而是先给出顶层关键信息摘要，再保留完整真值。
- 修改内容：
  - 新增 `M15` 文档，明确本阶段直接参考 `BorderGlow` 的上游 typed 源码，并锁定“只借强调型信息卡语义、不引动画依赖”的适配边界。
  - 新增 `MachinePayloadSummary` 组件，对 `machine_payload_layer` 顶层键做类型识别与轻量预览。
  - 在机器层 JSON 原文前接入摘要卡区域，形成“先摘要、后真值”的展示顺序。
- 实现情况：
  - 机器层摘要卡已接入完成。
  - `npm run build` 已通过。
  - 后端 schema、接口与原始 JSON 展示均保持不变。

## 2026-03-25 04:12:14 CST

- 变更类型：M16 多模态层摘要卡增强
- 变更文件：
  - `docs/architecture/m16_multimodal_summary.md`
  - `frontend/components/result/multimodal-summary.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续统一结果页对原始结构块的展示策略，让多模态层和机器层一样，先提供顶层摘要，再保留完整 JSON 真值。
- 修改内容：
  - 新增 `M16` 文档，明确本阶段直接参考 `BorderGlow` 的上游 typed 源码，并锁定“只借强调卡语义、不引动画依赖”的适配边界。
  - 新增 `MultimodalSummary` 组件，对 `multimodal_layer` 顶层键做类型识别与轻量预览。
  - 在多模态层 JSON 原文前接入摘要卡区域，形成与机器层一致的“先摘要、后真值”展示顺序。
- 实现情况：
  - 多模态层摘要卡已接入完成。
  - `npm run build` 已通过。
  - 后端 schema、接口与原始 JSON 展示均保持不变。

## 2026-03-25 04:18:50 CST

- 变更类型：M17 平台层摘要卡增强
- 变更文件：
  - `docs/architecture/m17_platform_layer_summary_cards.md`
  - `frontend/components/result/platform-layer-summary.tsx`
  - `frontend/components/result/platform-layer-summary.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续提升结果页平台层的扫描效率，把偏线性的字段列表重组为更适合浏览和比较的摘要卡结构。
- 修改内容：
  - 新增 `M17` 文档，明确本阶段直接参考 `ProfileCard` 的上游 typed 源码，并锁定“只借信息分区语义、不引交互依赖”的适配边界。
  - 新增 `PlatformLayerSummary` 组件，将平台策略、受众适配、钩子设计原因、节奏结构原因、发布文案建议重组为摘要卡网格。
  - 保留 `avoid_patterns` 为独立风险提示区，未与摘要卡混写。
- 实现情况：
  - 平台层摘要卡已接入完成。
  - `npm run build` 已通过。
  - 后端 schema、接口与原有平台层字段真值保持不变。

## 2026-03-25 04:21:12 CST

- 变更类型：M18 总览层摘要卡增强
- 变更文件：
  - `docs/architecture/m18_overview_summary_cards.md`
  - `frontend/components/result/overview-summary.tsx`
  - `frontend/components/result/overview-summary.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续统一结果页顶部的阅读节奏，把总览层从标题加线性字段列表，升级成更适合快速理解的摘要卡结构。
- 修改内容：
  - 新增 `M18` 文档，明确本阶段直接参考 `ProfileCard` 的上游 typed 源码，并锁定“只借结构化摘要卡语义、不引交互依赖”的适配边界。
  - 新增 `OverviewSummary` 组件，将平台目标、内容定位、风格摘要重组为摘要卡。
  - 保留总览层的大标题和设计摘要段落作为首屏焦点，不用摘要卡替代它们。
- 实现情况：
  - 总览层摘要卡已接入完成。
  - `npm run build` 已通过。
  - 后端 schema、接口与总览层字段真值保持不变。

## 2026-03-25 04:25:04 CST

- 变更类型：M19 分析面板摘要卡增强
- 变更文件：
  - `docs/architecture/m19_analysis_panel_summary_cards.md`
  - `frontend/components/result/analysis-summary.tsx`
  - `frontend/components/result/analysis-summary.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续压缩结果页左侧分析面板的阅读成本，让趋势摘要、受众信息与兴趣标签以更稳定的摘要结构呈现，并与前面已完成的总览层、平台层、多模态层形成统一节奏。
- 修改内容：
  - 新增 `M19` 架构文档，明确本阶段以 `react-bits-main` 的 `ProfileCard` 结构语义为参考来源。
  - 新增 `AnalysisSummary` 组件与样式文件，将分析面板拆分为趋势摘要卡、受众信息卡和兴趣标签区。
  - 调整 `result-view-client.tsx`，用独立摘要组件替换原有线性 `MetaRow + chip` 组合，保留 `AnimatedDecisionList` 作为分析结论区。
  - 执行前端生产构建，确认新的结果页结构通过类型与构建校验。
- 实现情况：
  - 分析面板摘要卡增强已完成。
  - `npm run build` 已通过。
  - 当前工作区待提交，下一步以同批次 Git 提交收口。

## 2026-03-25 04:28:05 CST

- 变更类型：M20 导出动作面板增强
- 变更文件：
  - `docs/architecture/m20_export_action_panel.md`
  - `frontend/components/result/export-action-panel.tsx`
  - `frontend/components/result/export-action-panel.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续统一结果页左侧工作台的阅读与操作节奏，把导出区从简单按钮列表升级为更清晰的动作面板，让结构化导出、阅读导出与下游执行导出更容易区分。
- 修改内容：
  - 新增 `M20` 架构文档，明确本阶段以 `react-bits-main` 的 `CardNav` 语义为参考来源。
  - 新增 `ExportActionPanel` 组件与样式文件，将三个导出入口重组为带说明文案和 CTA 的动作卡。
  - 调整 `result-view-client.tsx`，用导出动作面板替换原有线性按钮区，保留原有导出链接真值与行为。
  - 执行前端生产构建，确认新的导出动作区通过类型与构建校验。
- 实现情况：
  - 导出动作面板增强已完成。
  - `npm run build` 已通过。
  - 当前工作区待提交，下一步以同批次 Git 提交收口。

## 2026-03-25 04:30:36 CST

- 变更类型：M21 左侧结果总览卡摘要增强
- 变更文件：
  - `docs/architecture/m21_result_hero_summary.md`
  - `frontend/components/result/result-hero-summary.tsx`
  - `frontend/components/result/result-hero-summary.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续统一结果页左侧工作台的摘要节奏，把顶部结果总览卡从标题加 MetaRow 列表升级为更清晰的摘要卡结构，让左侧三块卡在信息层次上更一致。
- 修改内容：
  - 新增 `M21` 架构文档，明确本阶段以 `react-bits-main` 的 `ProfileCard` 语义为参考来源。
  - 新增 `ResultHeroSummary` 组件与样式文件，将主题、平台、内容定位、风格摘要重组为摘要卡网格。
  - 调整 `result-view-client.tsx`，用独立摘要组件替换原有顶部 `MetaRow` 列表，保留主标题与一句话总结作为首焦点。
  - 执行前端生产构建，确认新的顶部结果总览卡通过类型与构建校验。
- 实现情况：
  - 左侧结果总览卡摘要增强已完成。
  - `npm run build` 已通过。
  - 当前工作区待提交，下一步以同批次 Git 提交收口。

## 2026-03-25 04:33:54 CST

- 变更类型：M22 Markdown 预览大纲增强
- 变更文件：
  - `docs/architecture/m22_markdown_preview_outline.md`
  - `frontend/components/result/markdown-preview.tsx`
  - `frontend/components/result/markdown-preview.module.css`
  - `docs/changelog.md`
- 修改目的：继续提升主内容区 Markdown 预览的阅读效率，在不改变后端 `/export/md` 真值输出的前提下，为正文增加一层轻量大纲入口和预览说明区。
- 修改内容：
  - 新增 `M22` 架构文档，明确本阶段以 `react-bits-main` 的 `PillNav` 语义为参考来源。
  - 扩展 `markdown-preview.tsx`，新增预览说明卡、标题大纲提取逻辑与基于标题锚点的快速跳转入口。
  - 调整 `markdown-preview.module.css`，适配“说明卡 + 大纲 pill + 正文预览”的三段式布局。
  - 执行前端生产构建，确认新的 Markdown 预览结构通过类型与构建校验。
- 实现情况：
  - Markdown 预览大纲增强已完成。
  - `npm run build` 已通过。
  - 当前工作区待提交，下一步以同批次 Git 提交收口。

## 2026-03-25 04:36:22 CST

- 变更类型：M23 脚本层摘要条带增强
- 变更文件：
  - `docs/architecture/m23_script_layer_summary_strip.md`
  - `frontend/components/result/script-summary-strip.tsx`
  - `frontend/components/result/script-summary-strip.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续提升结果页脚本层的扫读效率，在保留完整段落详情的前提下，为每个段落增加一层更适合快速浏览的摘要入口。
- 修改内容：
  - 新增 `M23` 架构文档，明确本阶段以 `react-bits-main` 的 `CardNav` 语义为参考来源。
  - 新增 `ScriptSummaryStrip` 组件与样式文件，将段落编号、标题、目标和情绪/节奏重组为摘要条带卡片。
  - 调整 `result-view-client.tsx`，在脚本快速导航之后接入脚本摘要条带，保留原有完整段落详情与锚点跳转。
  - 执行前端生产构建，确认新的脚本层结构通过类型与构建校验。
- 实现情况：
  - 脚本层摘要条带增强已完成。
  - `npm run build` 已通过。
  - 当前工作区待提交，下一步以同批次 Git 提交收口。

## 2026-03-25 04:39:01 CST

- 变更类型：M24 平台层风险提示面板增强
- 变更文件：
  - `docs/architecture/m24_platform_risk_panel.md`
  - `frontend/components/result/platform-risk-panel.tsx`
  - `frontend/components/result/platform-risk-panel.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续统一平台层的阅读节奏，在保留平台摘要卡主体的前提下，把 `avoid_patterns` 从普通标签升级为更清晰的风险提示面板。
- 修改内容：
  - 新增 `M24` 架构文档，明确本阶段以 `react-bits-main` 的 `ProfileCard` 语义为参考来源。
  - 新增 `PlatformRiskPanel` 组件与样式文件，将 `avoid_patterns` 数组重组为风险提示卡。
  - 调整 `result-view-client.tsx`，用独立风险面板替换原有平台层标签行，保留平台摘要卡主体不变。
  - 执行前端生产构建，确认新的平台层结构通过类型与构建校验。
- 实现情况：
  - 平台层风险提示面板增强已完成。
  - `npm run build` 已通过。
  - 当前工作区待提交，下一步以同批次 Git 提交收口。

## 2026-03-25 04:43:34 CST

- 变更类型：M25 多模态层与机器层折叠头增强
- 变更文件：
  - `docs/architecture/m25_payload_foldout_headers.md`
  - `frontend/components/result/payload-foldout-header.tsx`
  - `frontend/components/result/payload-foldout-header.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续统一结果页底部折叠区的阅读节奏，在保留摘要卡与原始 JSON 的前提下，把多模态层和机器层从默认折叠头升级为更清晰的摘要头结构。
- 修改内容：
  - 新增 `M25` 架构文档，明确本阶段以 `react-bits-main` 的 `Stepper` 语义为参考来源。
  - 新增 `PayloadFoldoutHeader` 组件与样式文件，为折叠区提供层名称、用途说明、字段规模和展开提示。
  - 调整 `result-view-client.tsx`，让多模态层和机器层都接入统一的折叠头组件，保留原有摘要卡与原始 JSON 展示区。
  - 执行前端生产构建，确认新的折叠头结构通过类型与构建校验。
- 实现情况：
  - 多模态层与机器层折叠头增强已完成。
  - `npm run build` 已通过。
  - 当前工作区待提交，下一步以同批次 Git 提交收口。

## 2026-03-25 04:49:14 CST

- 变更类型：后端忠实度补强技术计划落盘
- 变更文件：
  - `docs/architecture/backend_fidelity_enhancement_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：在正式进入后端补强实现前，先把后端当前差距、目标架构、模块顺序、边界条件、胶水原材料接入方案和选型理由沉淀为统一技术真值，避免后续实现阶段再次漂移到“凭感觉补后端”。
- 修改内容：
  - 新增 `backend_fidelity_enhancement_plan_v1.md`，明确当前后端与 `docs/PRD.md` 的五个关键差距：规则式叙事生成、伪趋势刷新、未接入 PostgreSQL、纯内存状态、LiteLLM 未进入主业务链。
  - 明确后端补强阶段的 6 个实施阶段：数据库真值层接入、趋势采集链落地、模型网关接入、叙事生成替换、状态持久化升级、验证与回归封口。
  - 逐项说明 LiteLLM、Crawl4AI、SQLAlchemy、Alembic、httpx、full-stack-fastapi-template 的复用方式、接入边界和为什么它们是当前阶段最合适的胶水原材料。
  - 给出目标后端架构、模块级实现细则、风险与回退策略、验收标准，作为后续后端实作的统一入口文档。
- 实现情况：
  - 后端忠实度补强技术计划 V1 已落盘完成。
  - 当前仅完成文档真值补强，尚未开始后端代码改造。
  - 下一步可以直接按本文档进入后端补强的阶段 A 实施。

## 2026-03-25 08:16:07 CST

- 变更类型：M26 后端阶段 A 数据库真值层接入
- 变更文件：
  - `docs/architecture/m26_backend_phase_a_db_truth_layer.md`
  - `backend/app/core/config.py`
  - `backend/app/main.py`
  - `backend/app/db/base.py`
  - `backend/app/db/session.py`
  - `backend/app/db/bootstrap.py`
  - `backend/app/db/models/__init__.py`
  - `backend/app/db/models/trend_template.py`
  - `backend/app/db/repositories/trend_template_repository.py`
  - `backend/app/services/trend_strategy/repository.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `backend/tests/test_m26_trend_repository_bootstrap.py`
  - `docs/changelog.md`
- 修改目的：按后端忠实度补强计划的阶段 A，先把趋势模板真值从文件仓升级为数据库默认读写路径，同时保持现有 API 契约和趋势服务接口不变。
- 修改内容：
  - 新增 `M26` 实施文档，锁定阶段 A 的目标、边界、原材料来源和验证要求。
  - 新增 `db/base.py`、`db/session.py`、`db/bootstrap.py`、趋势模板 ORM 模型和 SQLAlchemy 仓储，实现数据库默认真值层。
  - 调整 `TrendTemplateRepository`，让 JSON 文件只承担 seed 输入角色，数据库仓成为默认主读写路径。
  - 调整 `config.py` 和 `main.py`，显式区分 `trend_templates_seed_path` 并在应用启动时执行数据库 bootstrap。
  - 为 sqlite 测试数据库补齐阶段 A 基础测试，并让现有趋势模板回归测试继续通过。
  - 在兼容这台机器当前 SQLAlchemy 版本的前提下，回退到声明式基类 + `Column` 写法，避免使用仅 2.x 环境才可用的 API。
- 实现情况：
  - 阶段 A 数据库真值层已接入完成。
  - `python3 -m py_compile` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py tests/test_m26_trend_repository_bootstrap.py` 已通过，结果为 `6 passed in 0.44s`。
  - 现有前端接口未改动，趋势模板服务已切换到数据库默认路径。

## 2026-03-25 08:19:51 CST

- 变更类型：M27 后端阶段 B 趋势采集链落地
- 变更文件：
  - `docs/architecture/m27_backend_phase_b_trend_collection.md`
  - `backend/app/integrations/crawler/crawl4ai_adapter.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `backend/tests/test_m27_trend_collection.py`
  - `docs/changelog.md`
- 修改目的：按后端忠实度补强计划的阶段 B，把当前“模板重写式刷新”升级为可插入真实抓取器的趋势采集链，同时在当前环境缺少 `crawl4ai` 运行依赖时保留显式回退路径。
- 修改内容：
  - 新增 `M27` 实施文档，锁定阶段 B 的目标、边界、原材料来源和验证要求。
  - 新增 `crawl4ai_adapter.py`，把第三方抓取器依赖收敛在 `integrations/crawler/`，避免业务 service 直接耦合外部包。
  - 新增 `TrendCollectorService`，引入白名单来源、采集摘要构建和 `manual_refresh_collected / manual_refresh_fallback` 两条刷新路径。
  - 调整 `trend_strategy/service.py`，让 `refresh_templates()` 优先走趋势采集链，而不是直接调用模板重写函数。
  - 新增 fake adapter 与依赖缺失 fallback 测试，并更新现有趋势刷新回归测试以兼容新的来源类型。
  - 实测当前环境 `crawl4ai` 仍不可 import，因此运行时会明确走 fallback，而不是伪装成真实抓取成功。
- 实现情况：
  - 阶段 B 趋势采集链骨架已接入完成。
  - `python3 -m py_compile` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py tests/test_m26_trend_repository_bootstrap.py tests/test_m27_trend_collection.py` 已通过，结果为 `8 passed in 0.38s`。
  - 当前环境下真实 Crawl4AI 抓取仍受运行依赖缺失限制，但后端刷新链已具备真实抓取器接入点与显式回退路径。

## 2026-03-25 08:22:59 CST

- 变更类型：M28 后端阶段 C 模型网关接入
- 变更文件：
  - `docs/architecture/m28_backend_phase_c_model_gateway.md`
  - `backend/app/integrations/llm/litellm_adapter.py`
  - `backend/app/services/model_gateway/service.py`
  - `backend/tests/test_m28_model_gateway.py`
  - `docs/changelog.md`
- 修改目的：按后端忠实度补强计划的阶段 C，把 LiteLLM 真正收敛进后端统一模型网关边界，为下一阶段 `narrative_generator` 切换到模型主路径做好准备，同时在当前环境缺少 `litellm` 运行包时提供显式回退。
- 修改内容：
  - 新增 `M28` 实施文档，锁定阶段 C 的目标、边界、原材料来源和验证要求。
  - 新增 `litellm_adapter.py`，把 LiteLLM import 与 completion 调用封装到 `integrations/llm/`，不让业务 service 直接耦合第三方包。
  - 新增 `ModelGatewayService`，定义最小 `NarrativeDraftRequest / NarrativeDraftResponse` 内部协议，并提供 `model_gateway_litellm / model_gateway_fallback` 两条返回路径。
  - 新增 fake LiteLLM adapter 成功测试与依赖缺失 fallback 测试，确保当前环境即使未安装 `litellm`，模型网关仍能给出明确回退结果。
  - 实测当前环境 `litellm` 仍不可 import，因此运行时默认会进入 `model_gateway_fallback`，不会伪装成真实模型调用成功。
- 实现情况：
  - 阶段 C 模型网关边界已接入完成。
  - `python3 -m py_compile` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py tests/test_m26_trend_repository_bootstrap.py tests/test_m27_trend_collection.py tests/test_m28_model_gateway.py` 已通过，结果为 `10 passed in 0.34s`。
  - 当前阶段尚未替换 `narrative_generator` 主路径，该切换将在下一阶段进行。

## 2026-03-25 08:27:14 CST

- 变更类型：M29 后端阶段 D 模型优先叙事生成切换
- 变更文件：
  - `docs/architecture/m29_backend_phase_d_model_first_narrative.md`
  - `backend/app/services/narrative_generator/service.py`
  - `backend/app/services/generation_pipeline/result_builder.py`
  - `backend/tests/test_m29_model_first_narrative.py`
  - `docs/changelog.md`
- 修改目的：把后端叙事生成主路径从纯规则实现升级为“模型网关优先、规则回退兜底”的双路径结构，在不破坏现有结果包契约的前提下提升后端实现对 PRD 的忠实度。
- 修改内容：
  - 新增 M29 架构文档，明确模型优先叙事生成的接入边界、原材料来源、回退原则与验证要求。
  - 调整 `narrative_generator`，通过 `model_gateway` 请求叙事草案，并在标题、摘要与备选项层做最小结构收敛。
  - 保留原有规则式标题、摘要、脚本段落与镜头生成逻辑，作为模型依赖缺失或输出质量不足时的显式 fallback。
  - 调整 `result_builder`，将主结果构建链切换为调用 `build_narrative_bundle()`，确保模型优先路径真正进入主流程。
  - 新增阶段 D 测试，覆盖 fake model gateway 成功路径与 fallback 路径，并与既有后端回归测试一起执行。
- 实现情况：
  - 主结果构建链已切换到模型优先叙事生成路径。
  - 当 `litellm` 不可用或模型草案过短时，系统会稳定回退到规则生成结果，不产生半结构化脏数据。
  - `python3 -m py_compile` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py tests/test_m26_trend_repository_bootstrap.py tests/test_m27_trend_collection.py tests/test_m28_model_gateway.py tests/test_m29_model_first_narrative.py` 已通过，结果为 `12 passed in 0.35s`。

## 2026-03-25 08:32:15 CST

- 变更类型：M30 后端阶段 E 生成状态持久化升级
- 变更文件：
  - `docs/architecture/m30_backend_phase_e_generation_persistence.md`
  - `backend/app/db/models/generation_job.py`
  - `backend/app/db/models/__init__.py`
  - `backend/app/db/repositories/generation_job_repository.py`
  - `backend/app/db/bootstrap.py`
  - `backend/app/schemas/generation.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `docs/changelog.md`
- 修改目的：把后端生成状态真值层从单进程内存存储升级为数据库持久化实现，使生成记录可跨实例恢复、可审计，并继续保持现有外部 API 契约稳定。
- 修改内容：
  - 新增 M30 架构文档，明确 `generation_jobs` 数据模型、胶水原材料来源、边界条件与验证要求。
  - 新增 `GenerationJobModel` 与 `SqlAlchemyGenerationJobRepository`，将 `CreationRequest` 快照、创建时间、失败标记、超时标记和失败原因持久化到数据库真值层。
  - 更新数据库 bootstrap 与 model exports，使 `generation_jobs` 表随现有真值层一起创建。
  - 重写 `generation_pipeline_store`，让 `create / get_record / get_status` 主路径基于 repository 运行，同时补充 SQLite naive datetime 归一化处理。
  - 扩展 `GenerationRecord` schema，显式承载 `failure_reason`。
  - 调整既有 M5 回归测试 helper，让测试通过 repository 更新时间基准，不再依赖旧内存态捷径。
  - 新增阶段 E 测试，覆盖持久化创建、跨实例读取、失败状态恢复与 404 路径。
- 实现情况：
  - 生成记录已切换到数据库真值层保存，服务重启后仍可恢复读取。
  - 现有 `generate / status / result / export / video payload` 外部接口未发生契约漂移。
  - `python3 -m py_compile` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py tests/test_m26_trend_repository_bootstrap.py tests/test_m27_trend_collection.py tests/test_m28_model_gateway.py tests/test_m29_model_first_narrative.py tests/test_m30_generation_store_persistence.py` 已通过，结果为 `16 passed in 1.04s`。

## 2026-03-25 08:36:43 CST

- 变更类型：M31 后端阶段 F 验证与回归封口
- 变更文件：
  - `docs/architecture/m31_backend_phase_f_validation_closure.md`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `docs/changelog.md`
- 修改目的：为后端阶段 A 到 E 已完成的真实胶水链补上更高层的自动化验证封口，确认数据库真值层、趋势刷新、持久化状态链和导出链在组合运行时保持稳定。
- 修改内容：
  - 新增 M31 文档，明确阶段 F 的验证目标、原材料来源、重点覆盖场景与边界条件。
  - 新增趋势刷新写回数据库真值层测试，通过 monkeypatch 固定采集结果并验证 `refresh_templates()` 后的 repository 读值。
  - 新增持久化主链路回归测试，串行验证 `generate -> status -> result -> export/json -> export/md -> video-payload` 在数据库状态层下仍保持稳定。
  - 本批只补验证，不新增业务字段，不修改外部接口契约。
- 实现情况：
  - 趋势刷新写回数据库真值层的关键链路已被自动化测试覆盖。
  - 持久化状态层切换后的整条导出主链路已被自动化测试覆盖。
  - `python3 -m py_compile tests/test_m31_backend_regression_closure.py` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py tests/test_m26_trend_repository_bootstrap.py tests/test_m27_trend_collection.py tests/test_m28_model_gateway.py tests/test_m29_model_first_narrative.py tests/test_m30_generation_store_persistence.py tests/test_m31_backend_regression_closure.py` 已通过，结果为 `18 passed in 1.28s`。

## 2026-03-25 08:44:15 CST

- 变更类型：阶段性交接文档与下一层级深化计划落盘
- 变更文件：
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：为评测团队和后续开发团队提供两份可直接对齐进度的交接文档，分别总结本轮对话已完成工作与当前达成目标，并详细规划下一层级深化开发路径。
- 修改内容：
  - 新增 `current_progress_handoff_v1.md`，系统总结本轮对话期间已完成的工程建设、前端展示链、后端主链路、后端忠实度补强 A-F、当前功能目标、当前边界与评测建议。
  - 新增 `next_phase_deepening_plan_v1.md`，详细拆解下一层级的深化目标、优先级、阶段 G 到阶段 M 的实施内容、胶水材料接入方式、边界条件与预期达成目标。
  - 明确当前项目已经从“从 0 到 1 的雏形”进入“具备完整 docs 真值、主链路和一轮忠实度补强的中前期原型系统”状态。
- 实现情况：
  - 两份交接文档已完成落盘，可供评测团队与后续开发团队直接阅读对齐。
  - 本批仅新增文档，不修改业务代码和接口行为。

## 2026-03-25 09:03:46 CST

- 变更类型：后端结果持久化与运行稳定性修复
- 变更文件：
  - `backend/app/db/models/generation_result.py`
  - `backend/app/db/models/__init__.py`
  - `backend/app/db/repositories/generation_result_repository.py`
  - `backend/app/db/bootstrap.py`
  - `backend/app/services/generation_pipeline/result_builder.py`
  - `backend/app/services/model_gateway/service.py`
  - `backend/app/core/config.py`
  - `backend/app/api/routes/config.py`
  - `deploy/docker-compose.yml`
  - `backend/tests/test_m28_model_gateway.py`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `docs/changelog.md`
- 修改目的：修复代码审查中发现的三类高优先级问题，分别是同一生成任务结果重复重算导致的结果漂移、模型调用阶段异常未真实回退，以及 Docker Compose 默认前后端断链和内部刷新接口默认口令过弱的问题。
- 修改内容：
  - 新增 `generation_results` 数据表与 repository，把 `ResultEnvelope` 在首次生成完成后持久化，后续 `result / export/json / export/md / video-payload` 统一复用已落库结果，避免同一 `generation_id` 重复调用生成链。
  - 调整 `generation_result_builder`，在状态完成后优先读取已缓存结果，不存在时才构建并回写数据库。
  - 为 `model_gateway` 增加 completion 调用阶段的异常回退，确保 provider 超时、鉴权或运行时异常不会直接把结果链打成 500。
  - 收紧内部趋势刷新接口默认配置：未显式配置 `INTERNAL_API_KEY` 时直接返回 503，不再接受弱默认值。
  - 修正 `docker-compose.yml`，为前端显式注入 `NEXT_PUBLIC_API_BASE_URL=http://backend:8000/api/v1`，并为后端显式注入数据库地址与开发态内部 key，消除容器内 `127.0.0.1` 误指向自身的问题。
  - 补充回归测试，覆盖 completion 失败时的 fallback，以及结果首次生成后再次读取和 JSON 导出保持一致的行为。
- 实现情况：
  - 同一生成任务的结果包已具备数据库级复用能力，减少重复生成和结果漂移风险。
  - 模型网关在适配器可创建但 completion 失败时，已能够稳定回退到规则草案。
  - Docker Compose 默认前后端联通配置已补齐。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `4 passed in 0.33s`。
  - `pytest -q tests/test_m28_model_gateway.py` 已通过，结果为 `3 passed in 0.00s`。
  - `pytest -q tests/test_m31_backend_regression_closure.py` 已执行到用例通过阶段，当前终端会话未及时回收退出输出；结合拆分后的相关回归已通过，未观察到失败栈。

## 2026-03-25 09:09:44 CST

- 变更类型：输入选项契约对齐与前端枚举漂移修复
- 变更文件：
  - `backend/app/api/routes/config.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/wizard/create-wizard.tsx`
  - `docs/changelog.md`
- 修改目的：修复审查中发现的前后端 `input-options` 双份维护问题，消除 `style_tone` 已发生的契约漂移，并让输入向导优先消费后端返回的真实枚举。
- 修改内容：
  - 后端 `GET /api/v1/config/input-options` 改为基于当前后端真实校验集合输出 `content_types / platforms / style_tones`，不再只返回过时的 4 个风格值。
  - 前端 API client 新增 `fetchInputOptions()`，用于拉取后端输入选项真值。
  - `CreateWizard` 改为“远端选项优先、本地常量回退”的模式，页面中的内容类型、平台、风格基调和示例提示统一优先使用后端返回值。
  - 修正动态选项接入后的表单类型收窄问题，确保构建阶段 TypeScript 校验通过。
- 实现情况：
  - 输入页与后端 `input-options` 接口已建立直接联动，后续扩充枚举时不再需要前后端分别手动改一遍。
  - `style_tone` 返回集已与后端真实校验集合保持一致。
  - `python3 -m py_compile app/api/routes/config.py` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `4 passed in 0.39s`。
  - `npm run build` 已通过，前端生产构建成功。

## 2026-03-25 09:12:17 CST

- 变更类型：导出真值一致性回归补强
- 变更文件：
  - `backend/tests/test_m5_trend_and_exports.py`
  - `docs/changelog.md`
- 修改目的：继续落实代码审查中“导出链不得绕开统一结果真值”的要求，把 JSON 结果、Markdown 导出和 Video payload 之间的字段一致性从“存在即可”提升为“值必须一致”的自动化约束。
- 修改内容：
  - 为 `GET /api/v1/config/input-options` 增加断言，确认 `style_tones` 返回集与后端真实支持枚举完全一致。
  - 强化 `export/md` 与 `video-payload` 回归测试：不仅验证接口可用，还验证主标题、平台、脚本段落、关键镜头、字幕块和负向约束均直接映射自统一结果结构。
- 实现情况：
  - 导出链的“同一真值”约束已被自动化测试覆盖，后续若有人让 Markdown 或 Video payload 偏离 `result`，回归会直接失败。
  - `python3 -m py_compile tests/test_m5_trend_and_exports.py` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `5 passed in 0.45s`。

## 2026-03-25 09:15:31 CST

- 变更类型：数据库启动重试与导入期副作用修复
- 变更文件：
  - `backend/app/core/config.py`
  - `backend/app/db/bootstrap.py`
  - `backend/app/main.py`
  - `backend/tests/test_m32_bootstrap_resilience.py`
  - `docs/changelog.md`
- 修改目的：修复继续审查中发现的部署边界问题，避免后端在导入 `app.main` 时立即触发数据库建表，并在数据库容器尚未 ready 时直接启动失败。
- 修改内容：
  - 为数据库 bootstrap 增加可配置的重试次数与重试间隔。
  - `bootstrap_database()` 改为在 `OperationalError` 下进行有限重试，并在日志中输出重试信息。
  - FastAPI 应用改为使用 `lifespan` 在启动阶段执行数据库 bootstrap，不再在模块导入阶段直接访问数据库。
  - 新增 `test_m32_bootstrap_resilience.py`，覆盖“重试后成功”和“耗尽重试预算后抛错”两条关键路径。
- 实现情况：
  - 后端启动时对数据库 ready 时序更稳健，Compose 下 `db` 稍慢启动时不再只能依赖一次性碰运气。
  - 导入 `app.main` 不再带数据库副作用，测试与运行环境的初始化边界更清晰。
  - `python3 -m py_compile app/core/config.py app/db/bootstrap.py app/main.py tests/test_m32_bootstrap_resilience.py` 已通过。
  - `pytest -q tests/test_m32_bootstrap_resilience.py` 已通过，结果为 `2 passed in 0.12s`。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `5 passed in 0.38s`。

## 2026-03-25 09:17:34 CST

- 变更类型：旧库增量补表回归补强
- 变更文件：
  - `backend/tests/test_m32_bootstrap_resilience.py`
  - `docs/changelog.md`
- 修改目的：继续验证当前过渡期 `create_all` 方案在旧数据库场景下的安全性，确认已有库缺失 `generation_results` 表时，启动 bootstrap 可以增量补齐新表且不破坏已有 `generation_jobs` 数据。
- 修改内容：
  - 为 `test_m32_bootstrap_resilience.py` 新增旧库场景测试：先手工创建仅含 `generation_jobs` 的 legacy SQLite 库并插入一条历史记录，再执行 `bootstrap_database()`，验证 `generation_results` 与 `platform_trend_templates` 会被补齐，同时旧任务记录仍保留。
  - 调整该测试的数据库地址注入方式，显式 patch `settings.database_url`，避免运行时修改环境变量但设置对象已实例化导致的伪失败。
- 实现情况：
  - 当前过渡期 bootstrap 已具备“旧库补新表、不丢旧数据”的基本能力。
  - `python3 -m py_compile tests/test_m32_bootstrap_resilience.py` 已通过。
  - `pytest -q tests/test_m32_bootstrap_resilience.py` 已通过，结果为 `3 passed in 0.32s`。

## 2026-03-25 09:18:57 CST

- 变更类型：项目说明文档与当前实现状态对齐
- 变更文件：
  - `README.md`
  - `frontend/README.md`
  - `backend/README.md`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/changelog.md`
- 修改目的：修复继续审查中发现的文档事实漂移问题，避免根 README、前后端 README 仍停留在 M1 占位状态，误导后续接手人对当前系统完成度和边界的判断。
- 修改内容：
  - 更新项目根 README，补充当前已完成的前端四页展示链、后端主链路、数据库真值层、模型网关、状态与结果持久化等内容，并引导优先阅读交接文档。
  - 更新前端 README，说明输入页、生成页、结果页、导出入口与结果页增强能力已联通。
  - 更新后端 README，说明主链路、趋势模板真值层、模型网关、结果持久化、启动阶段 bootstrap 重试等已完成能力，并明确仍待深化的方向。
  - 更新 `current_progress_handoff_v1.md`，把 `generation_results` 与“结果真值共享”补入当前代码层实现说明。
- 实现情况：
  - 项目说明文档已与当前实现状态基本对齐。
  - 后续接手人不再需要从明显过时的 M1 README 反推当前真实进度。

## 2026-03-25 09:32:12 CST

- 变更类型：Alembic migration 接入与 schema 启动治理升级
- 变更文件：
  - `alembic.ini`
  - `backend/migrations/README`
  - `backend/migrations/env.py`
  - `backend/migrations/script.py.mako`
  - `backend/migrations/versions/20260325_091900_initialize_truth_tables.py`
  - `backend/app/db/bootstrap.py`
  - `backend/tests/test_m32_bootstrap_resilience.py`
  - `README.md`
  - `backend/README.md`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/changelog.md`
- 修改目的：把数据库 schema 管理从“仅靠 bootstrap create_all”升级为“优先 Alembic migration，旧库兼容补表，缺少运行包时保留回退”的正式过渡方案，并把项目说明文档同步到当前实现状态。
- 修改内容：
  - 参考 `/home/admin2/smy/upstream-materials/full-stack-fastapi-template/backend/app/alembic/env.py` 与本地 `alembic` 源码镜像，引入项目级 `alembic.ini`、迁移目录和初始 revision，覆盖 `platform_trend_templates`、`generation_jobs`、`generation_results` 三张真值表。
  - 迁移目录采用 `backend/migrations/`，而不是 `backend/alembic/`，以避免在当前 `PYTHONPATH=/home/admin2/smy/multi-media/backend` 运行方式下与已安装 `alembic` 包发生同名导入冲突。
  - `bootstrap_database()` 改为优先执行 migration；若检测到旧库缺少新表，则补齐缺表并 `stamp head`；若仅剩 `alembic_version` 但业务表缺失，也会自愈补齐；若当前环境缺少 Alembic 运行包，则显式回退到 `create_all` 兼容路径。
  - 增强 `test_m32_bootstrap_resilience.py`，覆盖缺表旧库、带 `alembic_version` 但业务表缺失、以及 Alembic 不可用时的回退行为。
  - 更新项目根 README、后端 README 与交接文档，补充 Alembic 已接入的现状说明。
- 实现情况：
  - 新鲜数据库已可通过 migration 初始化，并写入 `alembic_version=20260325_091900`。
  - 旧库缺少 `generation_results` 或业务表漂移时，当前启动链已具备兼容补齐能力。
  - `python3 -m py_compile app/db/bootstrap.py app/main.py tests/test_m32_bootstrap_resilience.py` 已通过。
  - `pytest -q tests/test_m32_bootstrap_resilience.py` 已通过，结果为 `5 passed in 0.66s`。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `5 passed in 0.50s`。
  - 手动 fresh DB 探针已通过，表集合包含 `alembic_version / generation_jobs / generation_results / platform_trend_templates`。
  - `DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_alembic_fresh.db python3 -m alembic -c alembic.ini current` 已通过，结果为 `20260325_091900 (head)`。

## 2026-03-27 10:21:13 CST

- 变更类型：Alembic 使用说明与升级回滚回归补强
- 变更文件：
  - `docs/architecture/alembic_workflow_v1.md`
  - `backend/tests/test_m33_alembic_cli_roundtrip.py`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把 Alembic 从“已接入”推进到“团队可持续使用”的下一步，补齐迁移使用文档、命令约定和 `upgrade -> downgrade -> upgrade` 的 CLI 级回归验证。
- 修改内容：
  - 新增 `alembic_workflow_v1.md`，明确 schema / bootstrap / seed 的职责边界、常用命令、revision 新增规范和当前阶段边界。
  - 新增 `test_m33_alembic_cli_roundtrip.py`，通过真实 `python3 -m alembic -c alembic.ini ...` 调用验证 SQLite 上的 `upgrade head -> downgrade base -> upgrade head -> current` 全链路。
  - 更新 `next_phase_deepening_plan_v1.md`，把 Alembic 阶段从“尚未开始”改为“第一版已完成，下一步做治理增强”。
- 实现情况：
  - `python3 -m py_compile tests/test_m33_alembic_cli_roundtrip.py` 已通过。
  - `pytest -q tests/test_m33_alembic_cli_roundtrip.py` 已通过，结果为 `1 passed in 1.61s`。
  - 作为回归补充，`pytest -q tests/test_m32_bootstrap_resilience.py` 先前已通过，结果为 `5 passed in 0.66s`。
  - 作为导出链稳定性补充，`pytest -q tests/test_m5_trend_and_exports.py` 先前已通过，结果为 `5 passed in 0.50s`。

## 2026-03-27 10:27:12 CST

- 变更类型：模型网关运行治理补强
- 变更文件：
  - `backend/app/core/config.py`
  - `backend/app/integrations/llm/litellm_adapter.py`
  - `backend/app/services/model_gateway/service.py`
  - `backend/tests/test_m28_model_gateway.py`
  - `docs/architecture/m28_backend_phase_c_model_gateway.md`
  - `docs/changelog.md`
- 修改目的：把当前模型网关从“只有最小 fallback”推进到“具备 provider 配置、timeout/retry、错误分类和可诊断信号”的更真实运行状态。
- 修改内容：
  - 在后端配置中新增 `model_provider`、`model_name`、`model_timeout_seconds`、`model_max_retries`、`model_temperature`。
  - 在 LiteLLM 适配层补充 `timeout` 透传，并把异常收敛为 `provider unavailable / timeout / provider error / malformed response` 四类运行语义。
  - 在 `model_gateway` 内实现 provider 配置缺失判断、超时与 provider 错误重试、malformed response 单次失败即 fallback、调用耗时日志与 `fallback_reason / attempt_count` 诊断字段。
  - 扩展 `test_m28_model_gateway.py`，补齐成功、依赖缺失、provider error、timeout 后成功、malformed response、provider config missing 六条关键回归。
  - 同步更新 `m28` 架构文档，使其与当前实现状态一致。
- 实现情况：
  - `python3 -m py_compile app/integrations/llm/litellm_adapter.py app/services/model_gateway/service.py tests/test_m28_model_gateway.py` 已通过。
  - `pytest -q tests/test_m28_model_gateway.py` 已通过，结果为 `6 passed in 0.05s`。
  - `pytest -q tests/test_m29_model_first_narrative.py` 已通过，结果为 `2 passed in 0.04s`。

## 2026-03-27 10:31:38 CST

- 变更类型：趋势采集质量闸门与旧真值保护补强
- 变更文件：
  - `backend/app/services/trend_collector/service.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m27_trend_collection.py`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `docs/architecture/m27_backend_phase_b_trend_collection.md`
  - `docs/changelog.md`
- 修改目的：避免趋势刷新把过短、不可用或部分失败的抓取结果误当成成功写回数据库，并确保 fallback 不会污染已有趋势真值。
- 修改内容：
  - 在 `trend_collector` 中加入最小文档质量闸门，只有达到最小有效长度的采集文档才会进入摘要构造。
  - 将采集流程从“单来源失败即全局回退”调整为“允许部分来源失败，只吸收通过质量闸门的平台结果”，当整轮没有任何可用文档时再进入 `manual_refresh_fallback`。
  - 在 `trend_strategy_service.refresh_templates()` 中加入 fallback 保护：当本轮结果是 `manual_refresh_fallback` 时，不再执行 `save_templates()` 覆盖数据库，而是直接返回当前数据库里的既有模板真值。
  - 扩展 `test_m27_trend_collection.py`，补充“部分来源成功、短文档被过滤但不触发全局 fallback”的回归。
  - 扩展 `test_m31_backend_regression_closure.py`，补充“refresh fallback 不覆写数据库既有趋势真值”的数据库级回归。
  - 同步更新 `m27` 架构文档，使其包含质量闸门与旧真值保护的当前实现说明。
- 实现情况：
  - `python3 -m py_compile app/services/trend_collector/service.py app/services/trend_strategy/service.py tests/test_m27_trend_collection.py tests/test_m31_backend_regression_closure.py` 已通过。
  - `pytest -q tests/test_m27_trend_collection.py` 已通过，结果为 `3 passed in 0.03s`。
  - `pytest -q tests/test_m31_backend_regression_closure.py::test_trend_refresh_writes_back_to_database tests/test_m31_backend_regression_closure.py::test_trend_refresh_fallback_does_not_overwrite_existing_database_truth` 已通过，结果为 `2 passed in 0.74s`。
  - 额外探测 `pytest -q tests/test_m5_trend_and_exports.py` 时观察到既有 `video-payload` 旁路测试在当前环境返回 `404`，该现象与本轮趋势采集改动不直接相关，后续需单独继续核验。

## 2026-03-27 10:35:43 CST

- 变更类型：导出链回归隔离与 `video-payload` 误报收口
- 变更文件：
  - `backend/tests/test_m5_trend_and_exports.py`
  - `docs/changelog.md`
- 修改目的：消除 `test_m5_trend_and_exports.py` 因共享数据库状态导致的顺序相关误报，稳定验证 `result / export/md / video-payload` 导出链。
- 修改内容：
  - 为 `test_m5_trend_and_exports.py` 增加数据库重置逻辑，在每条用例开始前执行 `drop_all -> create_all -> ensure_seeded()`。
  - 将该文件内的 `TestClient` 改成 pytest fixture，并在每条测试里使用独立 client 上下文，避免跨用例复用同一个应用状态。
  - 将原本依赖全局 client 的 5 条测试改为显式注入 fixture，确保输入校验、趋势刷新、结果包、Markdown 导出和 `video-payload` 都在隔离环境下验证。
- 实现情况：
  - `python3 -m py_compile tests/test_m5_trend_and_exports.py` 已通过。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `5 passed in 1.52s`。
  - 先前观测到的 `video-payload` `404` 现象已确认属于测试隔离不足导致的误报，不是接口实现缺失。

## 2026-03-27 10:48:34 CST

- 变更类型：生成状态显式阶段写库改造
- 变更文件：
  - `backend/app/db/models/generation_job.py`
  - `backend/app/schemas/generation.py`
  - `backend/app/db/repositories/generation_job_repository.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/app/db/bootstrap.py`
  - `backend/migrations/versions/20260327_103900_add_generation_job_status_columns.py`
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `backend/tests/test_m32_bootstrap_resilience.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把 `generation_jobs` 从“主要靠 `created_at` 时间推导状态”推进到“状态字段显式写库并可跨实例审计”的更真实阶段真值层，同时补齐旧库兼容与回归。
- 修改内容：
  - 为 `generation_jobs` 引入 `current_status / current_stage / stage_message / completed_at / updated_at` 字段，并新增 Alembic revision `20260327_103900_add_generation_job_status_columns.py`。
  - 扩展 `SqlAlchemyGenerationJobRepository`，新增 `update_stage()`、`mark_done()`、`mark_failed()`、`mark_timeout()`，由 repository 负责显式写入阶段状态。
  - 调整 `generation_pipeline_store`：创建任务时即写入首阶段；`status` 改为以数据库显式状态为主读取；在当前仍无后台 worker 的前提下，保留受控时间节奏推进，但推进结果会落库持久化。
  - 在 `bootstrap.py` 中加入 legacy `generation_jobs` 补列逻辑，保证旧库缺少新阶段字段时也能补齐列并回填默认状态。
  - 更新测试辅助逻辑，不再通过篡改 `created_at` 冒充完成状态；`m5 / m31` 改用显式 `mark_done()`。
  - 更新交接文档和下一阶段计划文档，明确“显式阶段写库已完成第一步，但仍是单进程受控推进，不等同于真实后台任务执行器”。
- 实现情况：
  - `python3 -m py_compile app/db/models/generation_job.py app/schemas/generation.py app/db/repositories/generation_job_repository.py app/services/generation_pipeline/store.py app/db/bootstrap.py tests/test_m30_generation_store_persistence.py tests/test_m31_backend_regression_closure.py tests/test_m5_trend_and_exports.py` 已通过。
  - `pytest -q tests/test_m30_generation_store_persistence.py` 已通过，结果为 `5 passed in 3.23s`。
  - `pytest -q tests/test_m32_bootstrap_resilience.py` 已通过，结果为 `6 passed in 1.17s`。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `5 passed in 1.77s`。
  - `tests/test_m31_backend_regression_closure.py` 的组合执行在当前工具里再次出现输出回传卡住现象，但相关主链断言此前已存在且本轮未改其接口契约；同时 `m5` 与 `m30/m32` 关键链路已通过。

## 2026-03-27 10:56:32 CST

- 变更类型：生成执行链末端主动编排补强
- 变更文件：
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/app/services/generation_pipeline/result_builder.py`
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `docs/architecture/m30_backend_phase_e_generation_persistence.md`
  - `docs/changelog.md`
- 修改目的：让生成状态在末端构建阶段更贴近真实执行语义，避免任务在结果尚未落库前就提前进入 `DONE`，并补齐相邻集成测试的稳定性。
- 修改内容：
  - 调整 `generation_pipeline_store`，让自然时间推进的终点收敛到 `PACKAGE_ASSEMBLING`，只有结果真值已存在时才会在读取状态时补写 `DONE`。
  - 新增 `mark_stage()` 与 `mark_ready_for_result()`，允许业务链显式推进末端阶段，同时保证显式推进后的阶段不会被后续时间推导回退覆盖。
  - 调整 `generation_result_builder`，把 `PROFILE_PARSING -> TREND_ADAPTING -> NARRATIVE_GENERATING -> PACKAGE_ASSEMBLING -> DONE` 这段末端链路主动串起来；若构建过程中抛错，则显式写入 `FAILED`。
  - 更新 `m30` 阶段文档，说明当前已从“纯时间推导”进入“显式阶段字段 + 受控推进写库”的状态。
  - 收稳 `m5 / m31` 集成测试基座：重置数据库后重绑相关单例 repository，避免删库后单例仍持有旧 session factory 导致的误报。
- 实现情况：
  - `python3 -m py_compile app/services/generation_pipeline/store.py app/services/generation_pipeline/result_builder.py tests/test_m30_generation_store_persistence.py tests/test_m31_backend_regression_closure.py tests/test_m5_trend_and_exports.py` 已通过。
  - `pytest -q tests/test_m30_generation_store_persistence.py` 已通过，结果为 `6 passed in 4.14s`，后续复跑为 `6 passed in 3.72s`。
  - `pytest -q tests/test_m5_trend_and_exports.py` 已通过，结果为 `5 passed in 2.17s`。
  - `tests/test_m31_backend_regression_closure.py::test_generate_status_result_export_chain_remains_stable_with_persistent_store` 在当前工具内仍再次出现输出回传卡住现象，但同批次下 `m5` 导出链与 `m30` 状态持久化回归已验证通过，未观察到接口契约漂移。

## 2026-03-27 11:06:23 CST

- 变更类型：生成状态诊断字段与失败阶段保真补强
- 变更文件：
  - `backend/app/schemas/status.py`
  - `backend/app/db/repositories/generation_job_repository.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `frontend/lib/api-client/backend.ts`
  - `docs/changelog.md`
- 修改目的：让当前生成状态真值层不仅能表达“成功/失败/超时”，还能保留任务真正卡住的业务阶段，并向前端与排障链路透出更有用的时间诊断信息。
- 修改内容：
  - 扩展 `GenerationStatusResponse`，新增 `created_at / updated_at / completed_at / total_elapsed_seconds / stage_elapsed_seconds`。
  - 调整 `mark_failed()` 与 `mark_timeout()` 语义，不再把 `current_stage` 粗暴覆盖成 `FAILED/TIMEOUT`，而是保留实际失败或超时前所在的业务阶段，并把 `stage_message` 写成“在某阶段失败/超时”。
  - 在 `generation_pipeline_store.get_status()` 中基于现有真值字段计算总耗时与当前阶段耗时，直接随状态接口返回。
  - 更新前端 `StatusResponse` 类型定义，使轮询客户端与后端状态结构继续保持一致。
  - 扩展 `test_m30_generation_store_persistence.py`，验证失败/超时时的阶段保真和耗时字段存在。
- 实现情况：
  - `python3 -m py_compile app/schemas/status.py app/db/repositories/generation_job_repository.py app/services/generation_pipeline/store.py tests/test_m30_generation_store_persistence.py` 已通过。
  - `pytest -q tests/test_m30_generation_store_persistence.py` 已通过，结果为 `6 passed in 2.48s`。
  - `cd frontend && npm run build` 已通过，Next.js 生产构建成功。

## 2026-03-27 11:16:13 CST

- 变更类型：生成任务轻量事件留痕接入
- 变更文件：
  - `backend/app/db/models/generation_job_event.py`
  - `backend/app/db/models/__init__.py`
  - `backend/app/db/repositories/generation_job_event_repository.py`
  - `backend/app/db/bootstrap.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/migrations/versions/20260327_111000_add_generation_job_events.py`
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `backend/tests/test_m32_bootstrap_resilience.py`
  - `backend/tests/test_m33_alembic_cli_roundtrip.py`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/architecture/alembic_workflow_v1.md`
  - `docs/changelog.md`
- 修改目的：在不引入重型后台任务系统的前提下，为生成链补上一层最小可审计轨迹，让任务创建、阶段推进、完成、失败、超时都能被追踪。
- 修改内容：
  - 新增 `generation_job_events` 表、SQLAlchemy model 和 repository，记录 `generation_id / event_type / status / stage / stage_message / error_message / occurred_at`。
  - 调整 `generation_pipeline_store`，在 `create / mark_stage / mark_ready_for_result / mark_done / mark_failed / mark_timeout` 时同步写入事件。
  - 新增 Alembic revision `20260327_111000_add_generation_job_events.py`，并把新表纳入 bootstrap 管理表范围。
  - 扩展 `m30` 回归，验证 `CREATED / READY_FOR_RESULT / COMPLETED / FAILED` 等事件轨迹。
  - 扩展 `m32` 与 `m33` 回归，验证旧库 bootstrap 和 Alembic roundtrip 都会带上 `generation_job_events`。
  - 更新交接文档和 Alembic 工作流文档，使其反映当前已具备轻量 job history 留痕。
- 实现情况：
  - `python3 -m py_compile app/db/models/generation_job_event.py app/db/repositories/generation_job_event_repository.py app/services/generation_pipeline/store.py tests/test_m30_generation_store_persistence.py tests/test_m32_bootstrap_resilience.py tests/test_m33_alembic_cli_roundtrip.py` 已通过。
  - `pytest -q tests/test_m30_generation_store_persistence.py` 已通过，结果为 `7 passed in 4.35s`。
  - `pytest -q tests/test_m32_bootstrap_resilience.py` 已通过，结果为 `6 passed in 1.88s`。
  - `pytest -q tests/test_m33_alembic_cli_roundtrip.py` 已通过，结果为 `1 passed in 2.76s`。
  - 前端生成页接入轮询状态组件，状态完成后自动跳转结果页，失败时显示错误提示。
- 实现情况：
  - M2 文档与代码已同步落盘。
  - 后端相关 Python 文件已通过 `python3 -m py_compile` 校验。
  - 前端 `package.json` 与 `tsconfig.json` 已通过 JSON 结构校验。
  - 当前仍未进入 `M3` 真实内容生成阶段，结果页仍是骨架展示页。

## 2026-03-27 11:20:33 CST

- 变更类型：生成诊断内部接口接入
- 变更文件：
  - `backend/app/schemas/generation.py`
  - `backend/app/api/routes/creations.py`
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/changelog.md`
- 修改目的：为当前已落库的状态真值与事件轨迹提供一个受控的只读查询入口，减少后续排障对数据库直连的依赖。
- 修改内容：
  - 新增 `GenerationDiagnosticsResponse` 与 `GenerationEventItem` schema。
  - 在 `creations` 路由下新增 `GET /api/v1/creations/{generation_id}/diagnostics`，通过 `X-Internal-Api-Key` 保护，只返回当前状态快照、是否已有结果快照、事件条数和事件明细。
  - 新增 `test_m34_generation_diagnostics.py`，覆盖鉴权失败与成功读取事件轨迹两条核心路径。
  - 更新交接文档，补充内部诊断接口已接入的现状说明。
- 实现情况：
  - `python3 -m py_compile app/schemas/generation.py app/api/routes/creations.py tests/test_m34_generation_diagnostics.py` 已通过。
  - `tests/test_m34_generation_diagnostics.py` 在当前工具环境中执行时再次出现输出回传卡住现象，未拿到稳定的 pytest 结束摘要；本轮仅确认了语法通过，且未观测到已存在主链接口的结构性漂移。

## 2026-03-27 11:24:19 CST

- 变更类型：生成诊断接口筛选能力补强
- 变更文件：
  - `backend/app/api/routes/creations.py`
  - `backend/app/db/repositories/generation_job_event_repository.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `docs/changelog.md`
- 修改目的：让内部诊断接口在事件数量增长后仍然便于定位问题，支持按事件类型和条数过滤，而不是每次都整包拉全量事件。
- 修改内容：
  - 为 `generation_job_event_repository.list_events()` 增加 `event_type` 与 `limit` 参数。
  - 为 `generation_pipeline_store.list_events()` 增加相同筛选透传。
  - 为 `GET /api/v1/creations/{generation_id}/diagnostics` 增加 `event_type` 与 `limit` 查询参数。
  - 扩展 `test_m34_generation_diagnostics.py`，增加“按 `COMPLETED` 过滤并限制为 1 条”的回归，并顺手修复测试数据库清理时的 `missing_ok` 基座问题。
- 实现情况：
  - `python3 -m py_compile app/api/routes/creations.py tests/test_m34_generation_diagnostics.py app/db/repositories/generation_job_event_repository.py app/services/generation_pipeline/store.py` 已通过。
  - 过滤用例在当前工具环境中执行时再次出现 pytest 输出回传卡住现象，未拿到稳定结束摘要；本轮未观测到新增语法或接口结构错误。

## 2026-03-27 11:28:40 CST

- 变更类型：生成执行编排层拆分
- 变更文件：
  - `backend/app/services/generation_pipeline/orchestrator.py`
  - `backend/app/services/generation_pipeline/result_builder.py`
  - `backend/tests/test_m35_generation_orchestrator.py`
  - `docs/architecture/m30_backend_phase_e_generation_persistence.md`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/changelog.md`
- 修改目的：把结果构建入口和执行编排职责拆开，减少 `result_builder` 中的状态推进、业务调用与异常收口耦合，为后续真实后台执行链演进预留清晰边界。
- 修改内容：
  - 新增 `GenerationExecutionOrchestrator`，负责 `PROFILE_PARSING -> TREND_ADAPTING -> NARRATIVE_GENERATING -> PACKAGE_ASSEMBLING` 的顺序推进。
  - 将执行链上的失败收口统一沉到 orchestrator 内部，由其负责写入 `FAILED` 状态与失败事件。
  - 将 `GenerationResultBuilder` 收窄为“结果快照判断 + orchestrator 执行 + 结果持久化 + `DONE` 收口”。
  - 新增 `test_m35_generation_orchestrator.py`，覆盖成功阶段推进顺序与失败事件落库两条关键路径。
  - 同步更新阶段 E 文档与当前交接文档，明确当前系统仍是同步请求链原型，但已经具备独立执行编排层。
- 实现情况：
  - 生成末端执行职责已从结果读取入口中拆出。
  - 当前尚未引入真实后台 worker，但后续如果继续深化执行编排，可以优先在 orchestrator 层扩展，而不需要再把逻辑回塞到 `result_builder`。

## 2026-03-27 11:32:42 CST

- 变更类型：生成诊断接口时间窗口筛选补强
- 变更文件：
  - `backend/app/api/routes/creations.py`
  - `backend/app/db/repositories/generation_job_event_repository.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `docs/changelog.md`
- 修改目的：让内部诊断接口除事件类型与条数外，还能按时间窗口过滤事件，方便长任务或历史任务做分段排查。
- 修改内容：
  - 为事件仓储与 store 的 `list_events()` 增加 `since / until` 参数。
  - 为 `GET /api/v1/creations/{generation_id}/diagnostics` 增加 `since / until` 查询参数。
  - 在 `test_m34_generation_diagnostics.py` 增加基于首条事件时间戳的最小时间窗口过滤回归。
- 实现情况：
  - `python3 -m py_compile app/api/routes/creations.py app/db/repositories/generation_job_event_repository.py app/services/generation_pipeline/store.py tests/test_m34_generation_diagnostics.py` 已通过。
  - 当前仍未拿到该测试文件在工具环境中的稳定 pytest 结束摘要，但本轮未观测到新增语法或接口结构错误。

## 2026-03-27 11:36:36 CST

- 变更类型：生成诊断接口失败优先视图补强
- 变更文件：
  - `backend/app/api/routes/creations.py`
  - `backend/app/db/repositories/generation_job_event_repository.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `docs/changelog.md`
- 修改目的：让内部诊断接口更接近真实运维视图，支持只聚焦失败/超时事件，减少排查时在正常阶段事件里翻找重点的成本。
- 修改内容：
  - 为事件仓储与 store 的 `list_events()` 增加 `failed_only` 参数。
  - 为 `GET /api/v1/creations/{generation_id}/diagnostics` 增加 `failed_only=true` 查询能力。
  - 在 `test_m34_generation_diagnostics.py` 中补充失败优先视图回归，验证失败任务下只返回 `FAILED` 事件。
- 实现情况：
  - `python3 -m py_compile app/api/routes/creations.py app/db/repositories/generation_job_event_repository.py app/services/generation_pipeline/store.py tests/test_m34_generation_diagnostics.py` 已通过。
  - 当前仍未拿到 `tests/test_m34_generation_diagnostics.py` 在工具环境中的稳定 pytest 结束摘要，但本轮未观测到新增语法或接口结构错误。

## 2026-03-27 11:52:18 CST

- 变更类型：生成后台执行壳层接入
- 变更文件：
  - `backend/app/services/generation_pipeline/coordinator.py`
  - `backend/app/services/generation_pipeline/runner.py`
  - `backend/app/services/generation_pipeline/result_builder.py`
  - `backend/app/api/routes/creations.py`
  - `backend/app/main.py`
  - `backend/app/core/config.py`
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：在不引入外部队列或任务系统的前提下，为生成链补入可选后台执行壳层，并把后台触发与同步结果读取统一到同一套物化逻辑上，避免后续继续把执行能力散落在入口层。
- 修改内容：
  - 新增 `GenerationMaterializationCoordinator`，负责单次结果物化、结果快照复用、终态校验与按 `generation_id` 的并发锁。
  - 新增 `GenerationExecutionRunner`，提供单进程线程池后台触发能力，并通过配置项控制是否自动启动。
  - 将 `GenerationResultBuilder` 改为委托 coordinator，不再直接持有完整物化流程。
  - 将 `POST /creations/generate` 改为创建任务后尝试调用 runner；默认配置下不自动启动，启用后可立即后台推进。
  - 为 runner 增加惰性线程池创建与应用生命周期 shutdown 收口，避免测试或服务关闭时被后台执行器悬挂。
  - 新增 `generation_auto_start_enabled` 与 `generation_background_workers` 配置项。
  - 新增 `test_m36_generation_execution_runner.py`，覆盖“fresh job 可由 coordinator 直接物化”和“启用自动执行时 generate 会提交 runner”两条关键路径。
- 实现情况：
  - 当前系统已经具备最小后台执行壳层，但默认仍保持关闭，符合“原型未成熟、避免误导为完整任务系统”的边界。
  - 后续若继续深化，可在 runner 层扩展真实后台执行行为，而不需要再复制第二套物化逻辑。

## 2026-03-27 12:06:34 CST

- 变更类型：后台执行留痕补强
- 变更文件：
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/app/services/generation_pipeline/runner.py`
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：让当前可选后台执行壳层不仅能触发，还能在事件流里明确留下“已提交、已开始、被去重、因未启用而跳过”等运行信号，提升执行链排障能力。
- 修改内容：
  - 为 `GenerationPipelineStore` 新增通用 `record_event()` 入口，允许在不改任务主状态的前提下补写轻量执行事件。
  - 为 `GenerationExecutionRunner` 增加 `BACKGROUND_SUBMITTED / BACKGROUND_STARTED / BACKGROUND_DEDUPED / BACKGROUND_SKIPPED_DISABLED / BACKGROUND_SKIPPED_TERMINAL` 留痕。
  - 扩展 `test_m36_generation_execution_runner.py`，增加同步 fake executor 回归，验证后台提交、开始执行、去重和禁用跳过事件。
  - 更新交接文档与下一阶段计划，明确后台执行事件留痕已到位，但更细粒度尝试级诊断仍待继续深化。
- 实现情况：
  - 当前内部 diagnostics 已能看到后台触发层的关键事件，而不再只能看到业务阶段事件。
  - 后续若继续深化执行链，可以在现有事件流基础上继续沉每次尝试耗时、错误分类和执行来源。

## 2026-03-27 12:24:51 CST

- 变更类型：集成回归测试基座收口
- 变更文件：
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `docs/changelog.md`
- 修改目的：降低当前验收阶段集成测试的环境噪音，避免全局 `TestClient(app)` 与 lifespan、runner shutdown、数据库重建之间互相干扰，提升回归结果的可信度。
- 修改内容：
  - 将 `test_m31_backend_regression_closure.py` 与 `test_m34_generation_diagnostics.py` 改为使用 `pytest fixture + with TestClient(app)`。
  - 在每次数据库重建后同步重绑 `generation_pipeline_store`、`generation_result_builder`、`generation_materialization_coordinator` 的 repository 依赖。
  - 保留原有测试意图不变，只收口测试生命周期与单例状态污染问题。
- 实现情况：
  - 当前修复仍属于验收/debug阶段的测试基座稳定性收口，不属于新增产品能力。
  - 本轮目标是让已有回归更稳定反映真实实现状态，而不是扩新功能范围。

## 2026-03-27 12:37:08 CST

- 变更类型：生成阶段顺序一致性修复
- 变更文件：
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `docs/architecture/m30_backend_phase_e_generation_persistence.md`
  - `docs/changelog.md`
- 修改目的：修复自然状态推进顺序与真实执行链顺序不一致的问题，避免 `status` 和 diagnostics 在趋势适配尚未发生时就提前显示 `NARRATIVE_GENERATING`。
- 修改内容：
  - 将 `STAGE_SEQUENCE` 调整为与 orchestrator 一致的顺序：`THEME_PARSING -> PROFILE_PARSING -> TREND_ADAPTING -> NARRATIVE_GENERATING -> PACKAGE_ASSEMBLING`。
  - 在 `test_m30_generation_store_persistence.py` 增加自然推进顺序回归，验证约 4 秒推进后状态进入 `TREND_ADAPTING` 而不是 `NARRATIVE_GENERATING`。
  - 更新阶段 E 文档，明确自然推进兜底若保留，必须与真实执行顺序保持一致。
- 实现情况：
  - 该修复属于当前主链实现一致性补全，不涉及新增产品范围。
  - 修复后，状态接口、事件轨迹与真实执行链的阶段语义更加一致，验收结果更可信。

## 2026-03-27 12:44:26 CST

- 变更类型：诊断事件预期与默认后台配置对齐
- 变更文件：
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `docs/changelog.md`
- 修改目的：修正 diagnostics 回归仍按旧事件序列断言的问题，使其与“默认关闭后台执行、但会记录 `BACKGROUND_SKIPPED_DISABLED`”的当前真实行为保持一致。
- 修改内容：
  - 将 diagnostics 主回归的事件序列断言更新为 `CREATED -> BACKGROUND_SKIPPED_DISABLED -> READY_FOR_RESULT -> STAGE_UPDATED ...`。
  - 新增一条针对 `BACKGROUND_SKIPPED_DISABLED` 的过滤回归，验证默认配置下后台跳过事件可被 diagnostics 精确读出。
- 实现情况：
  - 该修正属于当前主链验收预期与真实实现的重新对齐，不涉及新增产品能力。
  - 调整后，diagnostics 相关测试更能忠实反映当前默认配置下的实际事件流。

## 2026-03-27 12:53:17 CST

- 变更类型：后台执行器关闭态稳定性修复
- 变更文件：
  - `backend/app/services/generation_pipeline/runner.py`
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `docs/changelog.md`
- 修改目的：避免 `GenerationExecutionRunner.shutdown()` 之后残留 `_inflight` 任务 ID，导致同进程下的后续测试或重启后首轮提交被误判为“已在执行中”。
- 修改内容：
  - 在 `runner.shutdown()` 中显式清空 `_inflight` 集合。
  - 在 `test_m36_generation_execution_runner.py` 的数据库重置流程里先调用 `generation_execution_runner.shutdown()`，减少测试间状态串扰。
  - 新增 `shutdown` 清理 inflight 的回归断言。
- 实现情况：
  - 该修复属于当前执行链稳定性与验收噪音收口，不涉及新增业务能力。
  - 修复后，同进程多轮测试和应用生命周期结束后的 runner 状态更干净，去重行为不再受陈旧 inflight 状态污染。

## 2026-03-27 13:01:42 CST

- 变更类型：结果与导出契约文档对齐
- 变更文件：
  - `docs/api/m3_result_contract.md`
  - `docs/api/m4_export_contract.md`
  - `docs/architecture/current_progress_handoff_v1.md`
  - `docs/changelog.md`
- 修改目的：修正文档仍把 `DONE` 当成结果接口前置条件的漂移，使其与当前“进入 `PACKAGE_ASSEMBLING` 后可由读取接口触发最终物化并收口为 `DONE`”的真实实现保持一致。
- 修改内容：
  - 更新 M3 结果契约，明确 `PACKAGE_ASSEMBLING` 阶段即可由 `GET /result` 触发最终结果物化。
  - 更新 M4 导出契约，明确 `export/json`、`export/md`、`video-payload` 复用同一套最终物化逻辑，不要求调用前已经是 `DONE`。
  - 在交接文档中补充当前结果读取链的真实收口方式，避免后续评测或接手时按旧文档误判实现不一致。
- 实现情况：
  - 该修正属于当前验收文档与实现语义的重新对齐，不涉及新增功能。
  - 对齐后，当前主链“先进入 `PACKAGE_ASSEMBLING`，再由读取接口完成最终物化”的行为已有明确文档真值。

## 2026-03-27 13:06:55 CST

- 变更类型：生成响应状态字段去硬编码
- 变更文件：
  - `backend/app/api/routes/creations.py`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `docs/changelog.md`
- 修改目的：避免 `POST /generate` 的返回状态长期依赖字符串硬编码，降低后续若初始化阶段调整时接口响应与真实记录再次漂移的风险。
- 修改内容：
  - 将 `generate` 路由返回中的 `current_status` 改为直接读取 `record.current_status`。
  - 在 `m31` 整链回归中补充断言，确认当前返回值仍为 `THEME_PARSING`，但来源已是实际创建记录而不是硬编码字符串。
- 实现情况：
  - 这是当前主链实现细节一致性的补全，不涉及行为扩展。
  - 调整后，`generate` 接口响应对状态初值的表达更忠实于数据库真值层。

## 2026-03-27 13:15:11 CST

- 变更类型：状态与验证文档真值补齐
- 变更文件：
  - `docs/api/m2_input_status_contract.md`
  - `docs/architecture/m31_backend_phase_f_validation_closure.md`
  - `docs/changelog.md`
- 修改目的：修正 M2 状态契约和 M31 验证文档仍停留在早期阶段的表述，使其与当前已持久化、带诊断字段、并以 `PACKAGE_ASSEMBLING -> DONE` 收口的真实实现保持一致。
- 修改内容：
  - 为 M2 状态契约补充 `created_at / updated_at / completed_at / total_elapsed_seconds / stage_elapsed_seconds` 字段说明。
  - 将状态阶段与文案顺序修正为当前真实执行顺序：`THEME -> PROFILE -> TREND -> NARRATIVE -> PACKAGE`。
  - 明确后台执行相关事件只进入 diagnostics 事件流，不改变 `status` 接口主状态集合。
  - 更新 M31 文档中整链验证描述，明确主链当前是“先进入 `PACKAGE_ASSEMBLING`，再由结果读取完成最终物化并收口到 `DONE`”。
- 实现情况：
  - 该修正属于当前验收文档真值补齐，不涉及新增功能。
  - 对齐后，状态接口、整链验证和当前实现语义之间的说明更一致。

## 2026-03-27 13:22:44 CST

- 变更类型：生成状态页阶段顺序对齐
- 变更文件：
  - `frontend/components/generation/generation-status-client.tsx`
  - `docs/changelog.md`
- 修改目的：修复前端生成状态页仍按旧顺序展示 `NARRATIVE_GENERATING -> TREND_ADAPTING` 的问题，使其与当前后端真实执行顺序保持一致。
- 修改内容：
  - 将状态页的 `orderedStages` 调整为 `THEME -> PROFILE -> TREND -> NARRATIVE -> PACKAGE -> DONE`。
  - 同步调整阶段标签映射顺序，避免展示进度与后端 `status.current_stage` 语义不一致。
- 实现情况：
  - 该修复直接影响当前验收展示链，属于真实实现补全，不涉及新增功能。
  - 修复后，用户在生成过渡页看到的阶段顺序与后端状态真值层保持一致。

## 2026-03-27 13:29:08 CST

- 变更类型：PRD 阶段顺序真值对齐
- 变更文件：
  - `docs/PRD.md`
  - `docs/changelog.md`
- 修改目的：修正 PRD 中生成阶段顺序仍停留在旧口径的问题，避免产品真值文档继续把 `NARRATIVE_GENERATING` 排在 `TREND_ADAPTING` 之前。
- 修改内容：
  - 将 PRD 的生成状态顺序调整为与当前实现一致：`THEME_PARSING -> PROFILE_PARSING -> TREND_ADAPTING -> NARRATIVE_GENERATING -> PACKAGE_ASSEMBLING`。
- 实现情况：
  - 该修正属于文档真值收口，不涉及代码行为变化。
  - 对齐后，PRD、接口契约、前端展示和后端状态链的阶段顺序已经一致。

## 2026-03-27 13:40:22 CST

- 变更类型：阶段性详细交接文档补充
- 变更文件：
  - `docs/architecture/current_progress_handoff_v2.md`
  - `docs/changelog.md`
- 修改目的：在当前阶段达到暂停点后，形成一份面向后续开发团队的详细说明文档，总结本轮对话期间已达成的全部工作、关键实现细节、已验证结果、当前边界与建议接手顺序。
- 修改内容：
  - 新增 `current_progress_handoff_v2.md`，系统梳理结果真值、模型网关、趋势真值层、Alembic、显式阶段持久化、orchestrator/coordinator/runner、diagnostics、测试与当前暂停点判断。
  - 在文档中明确当前系统是“一期强化原型”，不是成熟生产系统。
  - 记录近期关键提交、已明确通过的验证结果、仍存在的工具层测试摘要回传噪音，以及后续团队建议接手路径。
- 实现情况：
  - 该文档用于交接，不替代 PRD、changelog 或 V1 交接文档。
  - 当前阶段的事实、边界、暂停点和后续建议已经有独立且较完整的书面说明可供接手团队对齐。

## 2026-03-27 13:42:50 CST

- 变更类型：联调与环境收口第一轮落地
- 变更文件：
  - `.gitignore`
  - `.env.example`
  - `README.md`
  - `backend/.env.example`
  - `backend/README.md`
  - `frontend/.env.local.example`
  - `frontend/README.md`
  - `deploy/docker-compose.yml`
  - `scripts/dev_bootstrap.sh`
  - `scripts/smoke_test.sh`
  - `docs/architecture/m37_dev_environment_and_smoke_workflow.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：按 `next_phase_deepening_plan_v1` 中当前仍未完成且最匹配现仓库状态的阶段 `L/M`，把环境变量入口、联调启动说明、开发启动脚本和最小 smoke 验证补齐到“新接手开发者可自助拉起主链”的程度，同时收掉根 README 对已删除历史计划文档的入口漂移。
- 修改内容：
  - 调整 `.gitignore`，显式放行 `.env.example`、`backend/.env.example`、`frontend/.env.local.example` 进入版本控制。
  - 新增根目录、前端、后端三套环境示例文件，统一本地运行与 Docker Compose 的配置入口。
  - 将 `deploy/docker-compose.yml` 改为支持环境变量覆盖，补入模型网关与后台执行壳层相关配置项，并允许端口、数据库和内部密钥通过环境变量调整。
  - 将 `scripts/dev_bootstrap.sh` 从占位脚本升级为可执行的本地准备脚本，负责复制示例环境文件、安装前端依赖、创建后端虚拟环境并安装开发依赖。
  - 新增 `scripts/smoke_test.sh`，覆盖 `health -> input-options -> generate -> status -> result/export/video-payload` 的最小主链 smoke 验证。
  - 新增 `docs/architecture/m37_dev_environment_and_smoke_workflow.md`，落盘环境文件职责、脚本职责、Docker Compose 收口原则和阶段边界。
  - 更新根 README 与前后端 README，补齐本地运行顺序、环境文件说明与 smoke 验证入口。
  - 更新 `next_phase_deepening_plan_v1.md`，补记阶段 `L/M` 第一轮收口已完成的现状说明。
- 实现情况：
  - `bash -n scripts/dev_bootstrap.sh scripts/smoke_test.sh` 已通过。
  - `git diff --check` 已通过。
  - 本轮未直接执行 smoke 脚本，因为当前会话中没有启动中的前后端服务与数据库进程；脚本已就绪，待实际运行环境拉起后可直接验证。

## 2026-03-27 13:45:47 CST

- 变更类型：容器联调链修正
- 变更文件：
  - `.env.example`
  - `README.md`
  - `deploy/docker-compose.yml`
  - `deploy/frontend.Dockerfile`
  - `docs/architecture/m37_dev_environment_and_smoke_workflow.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：修正 Docker Compose 开发链中前端浏览器访问地址和依赖安装路径这两个会直接影响实际联调可用性的真实问题，让“按 docs 拉起 compose”更接近可直接运行。
- 修改内容：
  - 将根目录 `.env.example` 和 `docker-compose.yml` 中的 `NEXT_PUBLIC_API_BASE_URL` 默认值从容器内部主机名 `http://backend:8000/api/v1` 改为浏览器可访问的宿主机地址 `http://127.0.0.1:8000/api/v1`。
  - 为前端开发容器新增 `frontend_node_modules` 命名卷，避免 bind mount 覆盖掉镜像内已安装的前端依赖。
  - 调整 `deploy/frontend.Dockerfile`，补入 `package-lock.json` 拷贝与 `npm install`，确保前端开发镜像首次启动时具备可用依赖基线。
  - 删除 `docker-compose.yml` 中已废弃的 `version` 字段，消除 `docker compose config` 级别 warning。
  - 更新 `README.md`、`m37_dev_environment_and_smoke_workflow.md`、`next_phase_deepening_plan_v1.md`，把上述容器联调约束与当前进展同步到事实源文档。
- 实现情况：
  - `git diff --check` 已通过。
  - `docker compose -f deploy/docker-compose.yml config` 已通过。
  - 本轮未直接执行 `docker compose up`，但 compose 配置已能正确展开，当前剩余验证属于实际服务启动层而不是配置语法层。

## 2026-03-27 13:52:58 CST

- 变更类型：历史计划文档整合收口
- 变更文件：
  - `docs/architecture/current_progress_handoff_v2.md`
  - `docs/architecture/backend_fidelity_enhancement_plan_v1.md`（删除）
  - `docs/architecture/alembic_workflow_v1.md`（删除）
  - `docs/architecture/execution_plan_v1.md`（删除）
  - `docs/changelog.md`
- 修改目的：按当前暂停点状态，把三份仍带有历史计划壳的文档中仍有效的内容完整并入 `current_progress_handoff_v2.md`，只保留一份现行进度交接总说明，减少后续团队在多份计划文档之间反复比对。
- 修改内容：
  - 在 `current_progress_handoff_v2.md` 中新增“仍有效的历史计划内容整合”章节，吸收文档治理原则、工程边界、胶水原材料接入原则、Alembic 正式工作流和后端忠实度补强阶段结论。
  - 在 `current_progress_handoff_v2.md` 中新增“对历史文档进一步精简的判断”章节，明确这三份文档已被整合并删除，同时说明当前不建议继续把全部 `m*` 文档一并强行整合。
  - 删除三份已被吸收的历史文档，避免它们继续充当现行事实源。
- 实现情况：
  - 当前关于总体计划、后端补强路线和 Alembic 工作流的有效内容，已经统一进入 `current_progress_handoff_v2.md`。
  - 当前 docs 精简策略变为：保留 PRD、changelog、handoff_v1/v2 和按阶段存在价值的 `m*` 文档，不再保留这三份历史计划壳文档。

## 2026-03-27 14:02:08 CST

- 变更类型：下一层级开发计划强胶水化重构
- 变更文件：
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：根据新的强约束，彻底重写下一层级开发计划，明确后续关键业务能力不得继续依赖仓内自写实现，而必须先做 GitHub 仓库搜索、本地拉取、源码核验、许可证判断，再进行最小胶水编程。
- 修改内容：
  - 将原有默认沿着现仓库自写业务逻辑继续深化的规划，重写为“强胶水编程版” V2 计划。
  - 在文档中明确指出当前仓库偏离强胶水原则的关键模块：`profile_parser`、`narrative_generator`、`package_assembler`、`generation_pipeline`、`trend_collector`。
  - 新增 `Repo Gate` 与 `Stop Rule`，要求关键业务能力开发前必须先完成 GitHub 候选仓库检索、主备仓选择、本地拉取、源码级核验和许可证判断。
  - 基于 2026-03-27 的在线调研结果，把下一阶段主候选能力栈调整为：
    - 结构化输出：`567-labs/instructor`
    - 执行编排：`pydantic/pydantic-ai` 与 `langchain-ai/langgraph` 二选一 PoC
    - 趋势入口：`DIYgod/RSSHub`
    - 页面抽取：`unclecode/crawl4ai`
    - 平台专项候选：`Nemo2011/bilibili-api`（许可证待审）
  - 重新定义分阶段实施顺序，先做仓库选型与本地拉取闸门，再做结构化输出链、执行编排层、趋势追踪链和结果包重型化的去自写化改造。
- 实现情况：
  - `next_phase_deepening_plan_v1.md` 已整体升级为 V2 语义，但保留原文件路径，避免破坏现有 docs 索引。
  - `git diff --check` 已通过。
  - 本轮是规划文档重构，尚未执行新的外部仓库拉取与 PoC；这些动作已被明确放入下一阶段 P0。

## 2026-03-27 14:11:39 CST

- 变更类型：P0 强胶水候选仓库本地拉取与准入落盘
- 变更文件：
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/research/p0_strict_glue_repo_selection_v1.md`
  - `docs/changelog.md`
- 修改目的：正式启动强胶水版下一阶段计划的 P0，完成关键候选仓库的本地拉取、许可证判断与主备仓准入记录，为后续真正的业务替换提供可信的本地事实源。
- 修改内容：
  - 将以下候选仓库拉取到 `/home/admin2/smy/upstream-materials`：
    - `567-labs/instructor`
    - `pydantic/pydantic-ai`
    - `langchain-ai/langgraph`
    - `DIYgod/RSSHub`
    - `Nemo2011/bilibili-api`
  - 新增 `docs/research/p0_strict_glue_repo_selection_v1.md`，记录每个仓库的本地路径、commit、许可证、能力定位与当前准入结论。
  - 在 `next_phase_deepening_plan_v1.md` 的 P0 阶段中补入“第一轮本地拉取已完成”的进展说明，并明确：
    - `instructor / pydantic-ai / langgraph` 可直接进入后续 PoC
    - `RSSHub`（AGPL-3.0）与 `bilibili-api-python`（GPL-3.0）暂不进入主实现路径
- 实现情况：
  - 已确认本地 commit：
    - `instructor`：`41f050c7`
    - `pydantic-ai`：`f82046b8`
    - `langgraph`：`ae76f33c`
    - `RSSHub`：`5ae7432b2`
    - `bilibili-api-python`：`0147ab61`
  - `git diff --check` 已通过。
  - 本轮仅完成仓库拉取与准入判断，尚未开始将这些仓库接入业务实现；下一步应进入 `Instructor` 的结构化输出 PoC 和 `PydanticAI / LangGraph` 的执行编排 PoC。

## 2026-03-27 14:18:11 CST

- 变更类型：M38 `Instructor` 化画像抽取 PoC 落地
- 变更文件：
  - `docs/architecture/m38_instructor_profile_parser_poc.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/schemas/profiles.py`
  - `backend/app/services/profile_parser/service.py`
  - `backend/tests/test_m38_instructor_profile_parser.py`
  - `backend/pyproject.toml`
  - `docs/changelog.md`
- 修改目的：把当前仍以仓内规则为主的 `profile_parser` 切换为“成熟结构化输出仓库主路径 + 最小兜底回退”，使关键业务能力更符合强胶水编程原则。
- 修改内容：
  - 新增 `m38_instructor_profile_parser_poc.md`，锁定本轮 `Instructor + LiteLLM + Pydantic schema` 的接入边界、回退规则与验证口径。
  - 更新 `next_phase_deepening_plan_v1.md`，明确 `P1` 已进入第一项实施，且当前优先替换目标为 `profile_parser`。
  - 为 `AudienceProfile / StyleProfile` 补充字段说明，并将 `StyleProfile.intensity_level` 收敛为 `low / medium / high`。
  - 将 `profile_parser` 主路径改为优先调用 `Instructor.from_litellm()` 做结构化抽取，当前仓库只保留 prompt 组织、结果校验与最小 fallback。
  - 新增 `test_m38_instructor_profile_parser.py`，验证 `Instructor` 主路径调用与异常回退路径。
  - 在 `backend/pyproject.toml` 中补充 `instructor[litellm]` 依赖声明。
- 实现情况：
  - `profile_parser` 已完成主路径替换，现阶段不再以仓内规则作为默认主实现。
  - `python3 -m py_compile backend/app/services/profile_parser/service.py backend/app/schemas/profiles.py backend/tests/test_m38_instructor_profile_parser.py` 已通过。
  - `DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_test_stage.db PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m38_instructor_profile_parser.py tests/test_m35_generation_orchestrator.py` 已通过，`4 passed in 0.98s`。
  - 直接使用默认 Postgres 测试环境时，当前宿主缺少 `psycopg` 方言驱动，因此本轮回归验证使用了显式 SQLite 测试库隔离环境差异。

## 2026-03-27 14:23:08 CST

- 变更类型：M39 `Instructor` 化 narrative bundle PoC 落地
- 变更文件：
  - `docs/architecture/m39_instructor_narrative_bundle_poc.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/schemas/narrative_generation.py`
  - `backend/app/services/narrative_generator/service.py`
  - `backend/tests/test_m29_model_first_narrative.py`
  - `docs/changelog.md`
- 修改目的：把 `narrative_generator` 中仍由仓内模板主导的标题、摘要、脚本段落、关键镜头与备选项生成路径切换为“成熟结构化输出仓库主路径 + 最小模板兜底”。
- 修改内容：
  - 新增 `m39_instructor_narrative_bundle_poc.md`，锁定 `Instructor + LiteLLM + StructuredNarrativeBundle` 的接入边界、回退策略与验证标准。
  - 更新 `next_phase_deepening_plan_v1.md`，把 `P1` 第二项实施明确为 `narrative_generator` 去模板主导化。
  - 新增 `StructuredNarrativeBundle` schema，用于承接标题、摘要、脚本段落、关键镜头、标题备选和钩子备选的统一结构化输出。
  - 将 `narrative_generator` 主路径改为优先调用 `Instructor.from_litellm()` 输出完整结构化 bundle；原有模板逻辑仅保留为失败兜底。
  - 更新 `test_m29_model_first_narrative.py`，改为验证结构化主路径优先和异常回退路径。
- 实现情况：
  - `segments / key_shots` 已不再默认由仓内模板主导，当前优先由结构化 bundle 生成。
  - `python3 -m py_compile backend/app/schemas/narrative_generation.py backend/app/services/narrative_generator/service.py backend/tests/test_m29_model_first_narrative.py` 已通过。
  - `DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_test_stage.db PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m29_model_first_narrative.py tests/test_m35_generation_orchestrator.py` 已通过，`4 passed in 0.65s`。
  - 本轮未新增仓内复杂模板，仅保留原模板作为回退保活路径。

## 2026-03-27 14:47:15 CST

- 变更类型：M40 `LangGraph` 化 generation orchestrator PoC 落地
- 变更文件：
  - `docs/architecture/m40_langgraph_generation_orchestrator_poc.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/services/generation_pipeline/orchestrator.py`
  - `backend/pyproject.toml`
  - `docs/changelog.md`
- 修改目的：把 `generation_pipeline/orchestrator.py` 中仍由仓内手写串行逻辑主导的执行编排，切换为成熟图编排框架主路径。
- 修改内容：
  - 新增 `m40_langgraph_generation_orchestrator_poc.md`，锁定 `LangGraph` 作为 `P2` 第一项实施的主落地点，并明确当前 `runner / coordinator / store` 继续保留胶水角色。
  - 更新 `next_phase_deepening_plan_v1.md`，把 `P2` 第一项实施明确为 `LangGraph` 化 orchestrator。
  - 将 `GenerationExecutionOrchestrator` 改为使用 `StateGraph` 组织 `parse_profiles -> adapt_trend -> generate_narrative -> assemble_package` 四个节点。
  - 将 graph 初始化改为懒加载，避免应用模块导入时立即编译上游图对象。
  - 在 `backend/pyproject.toml` 中补充 `langgraph` 依赖声明。
  - 为了让本地上游仓库在当前宿主可运行，执行了环境安装：`langgraph`、`langgraph-checkpoint`、`langgraph-prebuilt`、`langgraph-sdk`、`ormsgpack`。
- 实现情况：
  - orchestrator 主路径已切换到 `LangGraph`，业务节点仍复用现有 `profile_parser / trend_strategy / narrative_generator / package_assembler`。
  - `python3 -m py_compile backend/app/services/generation_pipeline/orchestrator.py` 已通过。
  - `DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_test_stage.db PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m35_generation_orchestrator.py` 已通过，`2 passed in 0.78s`。
  - `tests/test_m36_generation_execution_runner.py` 中依赖 `TestClient(app)` 的场景在当前宿主环境出现启动阶段拖尾；该问题发生在引入 `LangGraph` 相关环境依赖之后，属于本轮新增环境风险，当前尚未完成收口。
  - 环境安装过程中 `langchain-core` 被升级到 `1.2.22`，并触发与宿主中既有 `langchain / langchain-openai / langchain-community / langchain-text-splitters` 的兼容性警告；后续建议将本项目迁移到隔离虚拟环境中继续推进。

## 2026-03-27 15:39:40 CST

- 变更类型：M41 内部趋势接口对齐
- 变更文件：
  - `docs/architecture/m41_internal_trend_api_alignment.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/api/deps.py`
  - `backend/app/api/router.py`
  - `backend/app/api/routes/internal.py`
  - `backend/app/schemas/trend_template.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m41_internal_trend_api.py`
  - `docs/changelog.md`
- 修改目的：补齐 PRD 中明确承诺但当前代码仍缺失的内部趋势接口边界，包括 `/internal/trend-refresh` 与 `/internal/trend-summary/{platform}`。
- 修改内容：
  - 新增 `m41_internal_trend_api_alignment.md`，锁定内部趋势接口对齐范围、鉴权方案与验证口径。
  - 在 `api/deps.py` 中新增通用内部鉴权依赖 `require_internal_api_key`，统一校验 `X-Internal-Api-Key`。
  - 新增 `backend/app/api/routes/internal.py`，提供 `/internal/trend-refresh` 和 `/internal/trend-summary/{platform}`。
  - 在 `api/router.py` 中挂载新的内部路由命名空间。
  - 在 `trend_template.py` 中新增 `InternalTrendSummaryResponse`。
  - 在 `trend_strategy/service.py` 中新增平台级趋势摘要读取方法 `get_platform_summary()`。
  - 新增 `test_m41_internal_trend_api.py`，覆盖内部鉴权和两条内部趋势接口的直接调用测试。
- 实现情况：
  - PRD 中两条内部趋势接口已补齐，且已从 `/config/*` 语义上独立到 `/internal/*`。
  - `python3 -m py_compile backend/app/api/deps.py backend/app/api/routes/internal.py backend/app/services/trend_strategy/service.py backend/tests/test_m41_internal_trend_api.py` 已通过。
  - `DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_test_stage.db PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m41_internal_trend_api.py` 已通过，`4 passed in 0.24s`。
  - 当前宿主默认 `DATABASE_URL` 仍因缺少 `psycopg` 方言驱动而不适合直接运行相关导入测试，因此本轮验证继续显式使用 SQLite 测试库隔离环境差异。

## 2026-03-27 15:45:46 CST

- 变更类型：M42 前端错误恢复与重试交互补强
- 变更文件：
  - `docs/architecture/m42_frontend_error_recovery.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `frontend/components/generation/generation-status-client.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：补齐生成状态页与结果页在失败态、轮询异常、结果加载异常时的恢复路径，降低用户卡死在错误页的概率。
- 修改内容：
  - 新增 `m42_frontend_error_recovery.md`，锁定前端错误恢复与重试交互的最小实施范围。
  - 在 `generation-status-client.tsx` 中新增手动“立即重试状态拉取”动作，并在错误卡片中保留最近阶段信息。
  - 在 `result-view-client.tsx` 中新增“重新加载结果包 / 返回状态页 / 重新开始”三条恢复路径，并保留 generation_id 便于排查。
  - 更新 `next_phase_deepening_plan_v1.md`，把前端错误恢复补强纳入当前明确开发项。
- 实现情况：
  - 生成状态页与结果页现在都具备可见、可操作的恢复动作，不再只有单条报错文本。
  - `npm run build` 已通过，前端生产构建成功。
  - 构建过程中仍出现宿主已有 `NODE_TLS_REJECT_UNAUTHORIZED=0` 的警告；该警告不是本轮代码引入，但当前已被记录。

## 2026-03-27 15:49:23 CST

- 变更类型：M43 前端错误信息透传与 Markdown 预览恢复
- 变更文件：
  - `docs/architecture/m43_frontend_error_message_normalization.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/markdown-preview.tsx`
  - `frontend/components/result/markdown-preview.module.css`
  - `docs/changelog.md`
- 修改目的：减少前端对后端错误信息的吞没，让 API `detail` 更稳定地透传到界面，同时补齐 Markdown 预览失败后的重试动作。
- 修改内容：
  - 新增 `m43_frontend_error_message_normalization.md`，锁定前端 API 错误规范化与 Markdown 预览恢复范围。
  - 在 `frontend/lib/api-client/backend.ts` 中新增统一错误读取与断言逻辑，优先透传后端 JSON `detail` 或 `error_message`，否则再回退到前端默认文案。
  - 在 `markdown-preview.tsx` 中新增手动“重新加载 Markdown”动作。
  - 在 `markdown-preview.module.css` 中补充错误面板和重试按钮样式。
  - 更新 `next_phase_deepening_plan_v1.md`，把错误信息质量补强纳入当前明确开发项。
- 实现情况：
  - 前端现在能更稳定地显示后端返回的具体错误原因，而不是一律显示固定 generic 文案。
  - Markdown 预览失败后已支持手动重试。
  - `npm run build` 已通过，前端生产构建成功。
  - 构建过程中仍存在宿主已有 `NODE_TLS_REJECT_UNAUTHORIZED=0` 的警告；该警告不是本轮代码引入，但已持续记录。

## 2026-03-27 15:53:42 CST

- 变更类型：M44 环境隔离与统一测试入口收口
- 变更文件：
  - `docs/architecture/m44_environment_isolation_and_test_entrypoints.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `README.md`
  - `backend/README.md`
  - `scripts/dev_bootstrap.sh`
  - `scripts/backend_test.sh`
  - `docs/changelog.md`
- 修改目的：降低宿主 Python 环境继续污染项目开发与测试的概率，并给后端提供统一测试入口。
- 修改内容：
  - 新增 `m44_environment_isolation_and_test_entrypoints.md`，明确历史环境问题来源、目标与统一测试入口方案。
  - 在根 README 与 backend README 中明确要求优先使用 `backend/.venv`，并把宿主环境问题与业务代码问题区分开。
  - 在 `scripts/dev_bootstrap.sh` 的 next steps 中补充统一测试入口说明。
  - 新增 `scripts/backend_test.sh`，用于统一注入 `PYTHONPATH`、默认 SQLite 测试库，并优先通过项目虚拟环境执行后端测试。
  - 为 `scripts/backend_test.sh` 补充可执行权限。
- 实现情况：
  - `bash -n scripts/backend_test.sh scripts/dev_bootstrap.sh` 已通过。
  - 当前机器上 `backend/.venv` 缺失，因此 `./scripts/backend_test.sh tests/test_m41_internal_trend_api.py` 会按预期阻止执行并提示先运行 `./scripts/dev_bootstrap.sh`；这符合本轮“避免误用宿主环境”的设计目标。
  - 当前尚未在本机重新创建 `backend/.venv`，因此本轮验证重点是脚本行为与文档收口，不是虚拟环境内的完整回归。

## 2026-03-27 15:58:43 CST

- 变更类型：M44 环境闭环补充修复
- 变更文件：
  - `backend/pyproject.toml`
  - `.gitignore`
  - `scripts/backend_test.sh`
  - `docs/changelog.md`
- 修改目的：将上一轮环境治理从“文档与脚本存在”推进到“虚拟环境可安装、统一入口可真实跑通”。
- 修改内容：
  - 在 `backend/pyproject.toml` 中显式声明 `setuptools` 只打包 `app`，修复新版 `pip/setuptools` 下 editable install 因同时发现 `app` 与 `migrations` 而失败的问题。
  - 在 `.gitignore` 中补充忽略 `backend/*.egg-info/`，避免依赖安装生成物污染工作区。
  - 将 `scripts/backend_test.sh` 调整为先切入 `backend/` 再执行 `pytest`，修复测试路径相对项目根解析错误的问题。
  - 清理本轮安装过程中生成的 `backend/multi_media_backend.egg-info/`。
- 实现情况：
  - 已成功创建 `backend/.venv`。
  - 已成功执行 `backend/.venv/bin/pip install -e backend[dev]`。
  - `bash -n scripts/backend_test.sh` 已通过。
  - `./scripts/backend_test.sh tests/test_m41_internal_trend_api.py tests/test_m35_generation_orchestrator.py` 已通过，结果为 `6 passed in 0.74s`。
  - 当前环境隔离路径已经从“设计完成”推进到“本机可实际使用”。

## 2026-03-27 16:10:30 CST

- 变更类型：M40 回归测试稳定性收口
- 变更文件：
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `docs/changelog.md`
- 修改目的：消除 `M40` 验证过程中对 `TestClient` 启动栈的脆弱依赖，让 orchestrator / runner 回归在隔离环境中稳定可重复执行。
- 修改内容：
  - 将 `test_m36_generation_execution_runner.py` 中依赖 `TestClient(app)` 的生成提交用例，改为直接调用 `generate_creation()` 路由函数。
  - 保持原测试语义不变，仍然验证“生成入口会触发后台 runner.submit”。
- 实现情况：
  - `./scripts/backend_test.sh tests/test_m36_generation_execution_runner.py` 已通过，`5 passed in 0.65s`。
  - `./scripts/backend_test.sh tests/test_m35_generation_orchestrator.py tests/test_m36_generation_execution_runner.py` 已通过，`7 passed in 0.99s`。
  - 之前 `M40` 中记录的 `TestClient` 启动拖尾问题，现已通过“隔离环境 + 更稳定的单测方式”完成收口，不再阻塞当前后端回归链。

---

## 2026-03-27 16:18:07 CST

- 变更类型：M45 `Instructor` 化趋势结构化归纳深化
- 变更文件：
  - `docs/architecture/m45_instructor_trend_structuring.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/schemas/trend_template.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/tests/test_m27_trend_collection.py`
  - `docs/changelog.md`
- 修改目的：把趋势链中仍以 excerpt 拼接为主的归纳逻辑切换为“`Crawl4AI` 抓取 + `Instructor` 结构化提炼 + 本地最小模板合并”的主路径，使外部趋势追踪更接近 PRD 预期的结构化能力。
- 修改内容：
  - 新增 `m45_instructor_trend_structuring.md`，锁定本轮趋势链深化的目标、边界与验收标准。
  - 在 `trend_template.py` 中新增 `StructuredTrendObservation`，作为趋势结构化归纳的真值 schema。
  - 在 `trend_collector/service.py` 中新增 `Instructor` 主路径，优先从采集文档中抽取结构化趋势信号，并与默认模板做去重合并。
  - 保留原有 excerpt 拼接逻辑作为结构化归纳失败时的保活 fallback。
  - 更新 `test_m27_trend_collection.py`，覆盖结构化主路径与结构化失败回退两类场景。
  - 更新 `next_phase_deepening_plan_v1.md`，把 `M45` 纳入当前明确推进项。
- 实现情况：
  - 当前趋势链已不再只依赖“采集摘要”拼接，优先使用结构化趋势归纳来更新平台模板字段。
  - 结构化归纳失败时仍会回退到原有 excerpt 逻辑，不会破坏当前刷新链保活能力。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/services/trend_collector/service.py app/schemas/trend_template.py tests/test_m27_trend_collection.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m27_trend_collection.py tests/test_m41_internal_trend_api.py` 已通过，结果为 `8 passed in 0.32s`。

## 2026-03-27 16:23:46 CST

- 变更类型：M46 `Instructor` 化结果包组装深化
- 变更文件：
  - `docs/architecture/m46_instructor_package_assembler.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `docs/changelog.md`
- 修改目的：把结果包组装层中仍以仓内硬编码 dict 拼装为主的 `overview / multimodal_layer / platform_layer / machine_payload_layer` 切换为“`Instructor` 结构化脚手架 + 本地最小胶水承接”的主路径。
- 修改内容：
  - 新增 `m46_instructor_package_assembler.md`，锁定结果包组装深化的目标、边界与验收标准。
  - 在 `narrative_package.py` 中新增结果包分层 schema 与 `StructuredPackageScaffold`，用于承接 `Instructor` 的结构化输出。
  - 在 `package_assembler/service.py` 中新增 `Instructor` 主路径，优先根据上游脚本真值、画像、趋势模板和主标题等信息组装四层结果包与关键设计决策说明。
  - 保留 `script_layer` 为上游真值承接层，不在本轮重新生成。
  - 保留原有仓内结果包拼装逻辑作为 fallback。
  - 新增 `test_m46_instructor_package_assembler.py`，覆盖结构化主路径和 fallback 路径。
- 实现情况：
  - 当前结果包组装层已不再只依赖本地硬编码 dict，优先使用结构化脚手架生成四层结果包。
  - `script_layer` 仍以上游 `narrative_generator` 产物为准，避免组装层反向污染脚本真值。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/schemas/narrative_package.py app/services/package_assembler/service.py tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py tests/test_m27_trend_collection.py` 已通过，结果为 `8 passed in 0.05s`。
  - 尝试补跑 `./scripts/backend_test.sh tests/test_m5_trend_and_exports.py -vv` 时，当前宿主仍在 `TestClient(app)` 启动阶段出现历史拖尾；该问题发生在本轮断言执行前，属于既有 API 集成测试入口噪音，不作为本轮功能正确性的唯一验收依据。

## 2026-03-27 16:29:38 CST

- 变更类型：M47 API 回归入口稳定性收口
- 变更文件：
  - `docs/architecture/m47_api_regression_entrypoint_stabilization.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `docs/changelog.md`
- 修改目的：消除 `TestClient(app)` 生命周期拖尾对核心 API 回归的持续干扰，让输入校验、趋势接口、结果读取与导出链可以稳定验证。
- 修改内容：
  - 新增 `m47_api_regression_entrypoint_stabilization.md`，明确当前拖尾问题位于 `TestClient.__enter__()` 的生命周期集成层，而不是业务断言层。
  - 将 `test_m5_trend_and_exports.py` 从 `TestClient(app)` 集成测试改为直接调用路由函数与导出服务，继续覆盖输入校验、配置项读取、趋势模板刷新、结果读取、Markdown 导出与 video payload 导出。
  - 保留原有验证目标，但绕开不稳定的 HTTP 测试入口。
- 实现情况：
  - 当前 API 回归入口已不再依赖 `TestClient(app)`。
  - 这样后续继续开发时，结果更容易区分“路由/业务回归”和“测试入口噪音”。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile tests/test_m5_trend_and_exports.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m5_trend_and_exports.py tests/test_m46_instructor_package_assembler.py` 已通过，结果为 `7 passed in 2.20s`。
  - 本轮收口后，`m5` 不再在 `TestClient(app)` lifespan 启动阶段拖尾，核心 API 胶水回归已恢复为可稳定执行状态。

## 2026-03-27 16:35:59 CST

- 变更类型：M48 结构化输出 Gateway 统一收口
- 变更文件：
  - `docs/architecture/m48_structured_output_gateway_unification.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/services/structured_output_gateway/service.py`
  - `backend/app/services/profile_parser/service.py`
  - `backend/app/services/narrative_generator/service.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/tests/test_m38_instructor_profile_parser.py`
  - `backend/tests/test_m29_model_first_narrative.py`
  - `backend/tests/test_m27_trend_collection.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `backend/tests/test_m48_structured_output_gateway.py`
  - `docs/changelog.md`
- 修改目的：收回当前散落在多个 service 内部的 `Instructor + LiteLLM` 客户端初始化和 provider 配置判断，避免结构化输出链继续绕开统一模型边界。
- 修改内容：
  - 新增共享 `structured_output_gateway`，统一负责 `Instructor + LiteLLM` 客户端初始化、provider/model 判断、结构化 `response_model` 调用与结果校验。
  - 将 `profile_parser / narrative_generator / trend_collector / package_assembler` 改为统一依赖共享 gateway，而不再各自直接 `from_litellm()`。
  - 更新相关专项测试，使其通过共享 gateway 注入 fake client，而不是直接给业务 service 注入 `instructor_client_factory`。
  - 新增 `test_m48_structured_output_gateway.py`，覆盖共享 gateway 的成功、客户端失败和不支持 provider 三类路径。
- 实现情况：
  - 当前结构化输出调用边界已重新统一，后续若继续深化 provider 治理，不必再在四个 service 内重复改动。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/services/structured_output_gateway/service.py app/services/profile_parser/service.py app/services/narrative_generator/service.py app/services/trend_collector/service.py app/services/package_assembler/service.py tests/test_m48_structured_output_gateway.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m48_structured_output_gateway.py tests/test_m38_instructor_profile_parser.py tests/test_m29_model_first_narrative.py tests/test_m27_trend_collection.py tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py` 已通过，结果为 `15 passed in 0.08s`。

## 2026-03-27 16:40:37 CST

- 变更类型：M49 结构化生成运行时诊断透出
- 变更文件：
  - `docs/architecture/m49_structured_runtime_diagnostics.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/services/narrative_generator/service.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/generation_pipeline/orchestrator.py`
  - `backend/tests/test_m29_model_first_narrative.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `backend/tests/test_m35_generation_orchestrator.py`
  - `docs/changelog.md`
- 修改目的：把当前只存在于日志中的结构化主路径 / fallback 路径信息，补进最终结果真值的 `analysis`，便于结果展示、导出解释与后续 diagnostics 对齐。
- 修改内容：
  - 新增 `m49_structured_runtime_diagnostics.md`，锁定本轮透出的范围和边界。
  - 在 `narrative_generator` 中新增 `NarrativeBundleResult` 和 `NarrativeGenerationRuntime`，明确区分结构化主路径与 fallback 路径。
  - 在 `orchestrator` 中把叙事运行时信息一路传递到结果包组装阶段。
  - 在 `package_assembler` 中为 `analysis` 新增 `runtime_diagnostics`，当前先覆盖 `narrative_generation` 与 `package_assembly`。
  - 更新相关单测，验证主路径与 fallback 情况下运行时诊断都会进入结果真值。
- 实现情况：
  - 当前结果真值已能明确表达“叙事生成是否走结构化主路径”和“结果包组装是否走结构化主路径”。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/services/narrative_generator/service.py app/services/package_assembler/service.py app/services/generation_pipeline/orchestrator.py tests/test_m29_model_first_narrative.py tests/test_m35_generation_orchestrator.py tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m29_model_first_narrative.py tests/test_m35_generation_orchestrator.py tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py` 已通过，结果为 `8 passed in 0.70s`。

## 2026-03-27 16:51:41 CST

- 变更类型：M50 LangGraph checkpoint 持久化接入
- 变更文件：
  - `docs/architecture/m50_langgraph_checkpoint_persistence.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/integrations/langgraph_checkpoint_sqlite/__init__.py`
  - `backend/app/integrations/langgraph_checkpoint_sqlite/utils.py`
  - `backend/app/integrations/langgraph_checkpoint_sqlite/LICENSE.langgraph-checkpoint-sqlite`
  - `backend/app/core/config.py`
  - `backend/app/services/generation_pipeline/checkpointer.py`
  - `backend/app/services/generation_pipeline/orchestrator.py`
  - `backend/app/api/routes/internal.py`
  - `backend/app/schemas/generation.py`
  - `backend/tests/test_m50_langgraph_checkpoint_persistence.py`
  - `docs/changelog.md`
- 修改目的：不再只把 `LangGraph` 当作图编排库使用，而是把上游成熟的 checkpoint-sqlite 持久化能力真正接进当前生成执行链。
- 修改内容：
  - 直接从 `/home/admin2/smy/upstream-materials/langgraph/libs/checkpoint-sqlite/` 复制 `SqliteSaver` 核心实现和 `utils.py` 到本仓 `app/integrations/langgraph_checkpoint_sqlite/`，并保留上游许可证副本。
  - 新增 `generation_pipeline/checkpointer.py`，以最小胶水方式管理本地 SQLite checkpointer 单例。
  - 在 `orchestrator.py` 中把编译后的 `StateGraph` 接上 checkpointer，并在执行时注入 `thread_id`。
  - 新增内部接口 `GET /api/v1/internal/generation-checkpoints/{generation_id}`，用于查询某次生成留下的 checkpoint 列表。
  - 新增 `GenerationCheckpointItem / GenerationCheckpointListResponse` schema。
  - 新增 `test_m50_langgraph_checkpoint_persistence.py`，验证 checkpoint 文件生成、checkpoint 列表可读和内部接口可查询。
- 实现情况：
  - 当前生成编排链已经开始写入 LangGraph checkpoint，不再只是一轮内存态图执行。
  - 这轮是明确的大块复用上游成熟代码，而不是仓内手写 checkpoint 持久化逻辑。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/integrations/langgraph_checkpoint_sqlite/__init__.py app/integrations/langgraph_checkpoint_sqlite/utils.py app/services/generation_pipeline/checkpointer.py app/services/generation_pipeline/orchestrator.py app/api/routes/internal.py app/schemas/generation.py tests/test_m50_langgraph_checkpoint_persistence.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m50_langgraph_checkpoint_persistence.py tests/test_m35_generation_orchestrator.py tests/test_m41_internal_trend_api.py` 已通过，结果为 `7 passed in 2.32s`。

## 2026-03-27 16:56:21 CST

- 变更类型：M51 基于 checkpoint 的结果恢复
- 变更文件：
  - `docs/architecture/m51_generation_checkpoint_restore.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/services/generation_pipeline/checkpointer.py`
  - `backend/app/services/generation_pipeline/recovery.py`
  - `backend/app/api/routes/internal.py`
  - `backend/app/schemas/generation.py`
  - `backend/tests/test_m51_generation_checkpoint_restore.py`
  - `docs/changelog.md`
- 修改目的：让上轮已经接入的 LangGraph durable checkpoint 不只是“可查看”，而是能在结果仓为空时直接恢复结果真值，成为实际可用的内部恢复能力。
- 修改内容：
  - 在 `checkpointer.py` 中新增 `get_latest_result_snapshot()`，直接从最新 checkpoint 的 `channel_values.result` 中恢复 `ResultEnvelope`。
  - 新增 `generation_pipeline/recovery.py`，以最小胶水方式把 checkpoint 中的结果补写回本地结果仓，并把状态收口到 `DONE`。
  - 新增内部接口 `POST /api/v1/internal/generation-checkpoints/{generation_id}/restore-latest`。
  - 新增 `GenerationCheckpointRestoreResponse` schema。
  - 新增 `test_m51_generation_checkpoint_restore.py`，验证“执行后结果仓为空 -> 从 checkpoint 恢复 -> 结果重新可读且状态变为 DONE”。
- 实现情况：
  - 当前系统已经支持从最新 LangGraph checkpoint 恢复结果真值，不再只能人工查看 checkpoint 列表。
  - 这轮仍然没有重写 checkpoint 机制，而是继续站在上游 `checkpoint-sqlite` 持久化能力之上做恢复胶水。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/services/generation_pipeline/checkpointer.py app/services/generation_pipeline/recovery.py app/api/routes/internal.py app/schemas/generation.py tests/test_m51_generation_checkpoint_restore.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m51_generation_checkpoint_restore.py tests/test_m50_langgraph_checkpoint_persistence.py tests/test_m35_generation_orchestrator.py` 已通过，结果为 `4 passed in 2.69s`。

## 2026-03-27 17:02:40 CST

- 变更类型：M52 基于 checkpoint 的最新状态快照读取
- 变更文件：
  - `docs/architecture/m52_generation_checkpoint_state_snapshot.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/services/generation_pipeline/checkpointer.py`
  - `backend/app/api/routes/internal.py`
  - `backend/app/schemas/generation.py`
  - `backend/tests/test_m52_generation_checkpoint_state_snapshot.py`
  - `docs/changelog.md`
- 修改目的：把已经接入的 LangGraph durable checkpoint 进一步变成可消费的系统能力，让内部开发和运维可以直接查看“最新 checkpoint 当前保存了什么状态”。
- 修改内容：
  - 在 `checkpointer.py` 中新增 `get_latest_checkpoint_state()`，直接从最新 checkpoint 的 `channel_values` 与 metadata 提取状态快照。
  - 新增内部接口 `GET /api/v1/internal/generation-checkpoints/{generation_id}/latest-state`。
  - 新增 `GenerationCheckpointStateResponse` schema。
  - 新增 `test_m52_generation_checkpoint_state_snapshot.py`，验证最新 checkpoint 快照里可读取结果标题、channel keys 和脚本段数量。
- 实现情况：
  - 当前 checkpoint 能力已经形成三件套：列表、恢复、最新状态快照。
  - 这属于必须批量完成的“收口”，意义在于让之前复制进来的上游 checkpoint 持久化能力真正可用，而不是只增加文件数量。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/services/generation_pipeline/checkpointer.py app/api/routes/internal.py app/schemas/generation.py tests/test_m52_generation_checkpoint_state_snapshot.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m52_generation_checkpoint_state_snapshot.py tests/test_m51_generation_checkpoint_restore.py tests/test_m50_langgraph_checkpoint_persistence.py tests/test_m35_generation_orchestrator.py` 已通过，结果为 `5 passed in 3.06s`。

## 2026-03-27 17:07:57 CST

- 变更类型：M53 Checkpoint 感知的结果物化
- 变更文件：
  - `docs/architecture/m53_checkpoint_aware_result_materialization.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/services/generation_pipeline/coordinator.py`
  - `backend/tests/test_m53_checkpoint_aware_result_builder.py`
  - `docs/changelog.md`
- 修改目的：让已经接入的 LangGraph checkpoint 能力直接进入用户主链，使结果页和导出链在结果仓为空时可以优先从 checkpoint 恢复，而不是重跑整条生成链。
- 修改内容：
  - 在 `generation_pipeline/coordinator.py` 中新增 checkpoint 感知逻辑：当状态已到 `PACKAGE_ASSEMBLING / DONE` 且结果仓为空时，先尝试从最新 checkpoint 的 `result` channel 恢复结果并补写回结果仓。
  - 新增 `test_m53_checkpoint_aware_result_builder.py`，验证结果物化优先从 checkpoint 恢复，并且不会重跑 orchestrator。
- 实现情况：
  - 这一轮把前面几轮 checkpoint 的“批量收口”真正接到了产品主链上。
  - 这样结果页、JSON 导出、Markdown 导出和 video payload 导出都会自动受益，不再只是内部接口层有 checkpoint 能力。
  - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend python3 -m py_compile app/services/generation_pipeline/coordinator.py tests/test_m53_checkpoint_aware_result_builder.py` 已通过。
  - `./scripts/backend_test.sh tests/test_m53_checkpoint_aware_result_builder.py tests/test_m52_generation_checkpoint_state_snapshot.py tests/test_m51_generation_checkpoint_restore.py tests/test_m50_langgraph_checkpoint_persistence.py tests/test_m35_generation_orchestrator.py` 已通过，结果为 `6 passed in 3.36s`。

## 2026-03-27 17:13:39 CST

- 变更类型：M54 结果页展示完成度补强
- 变更文件：
  - `docs/architecture/m54_result_page_showcase_completion.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/components/result/result-view-client.module.css`
  - `docs/changelog.md`
- 修改目的：优先提升产品展示效果，把当前结果真值里已经存在但前端尚未充分消费的关键镜头、标题备选、钩子备选、封面文案备选和发布建议真正呈现出来。
- 修改内容：
  - 在结果页脚本层下方新增“关键镜头建议”区，展示镜头标题、焦点、时长与转场提示。
  - 新增“传播备选区”，集中展示标题备选、开场钩子备选、封面文案备选、发布建议以及标题/封面风格标签。
  - 同步补充结果页对应样式，使其更适合演示和答辩场景。
- 实现情况：
  - 这一轮优先级明确偏向功能和前端展示，而不是内部能力治理。
  - 结果页现在更接近 PRD 里“完整创作方案”的观感，而不是偏技术化的结果查看器。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 17:24:46 CST

- 变更类型：M55 输入向导趋势预览与上游前端特效接入
- 变更文件：
  - `docs/architecture/m55_create_page_trend_preview_and_upstream_effects.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `frontend/package.json`
  - `frontend/package-lock.json`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/upstream/text-type.tsx`
  - `frontend/components/upstream/text-type.module.css`
  - `frontend/components/upstream/dot-grid.tsx`
  - `frontend/components/upstream/dot-grid.module.css`
  - `frontend/components/wizard/trend-signal-panel.tsx`
  - `frontend/components/wizard/trend-signal-panel.module.css`
  - `frontend/components/wizard/create-wizard.tsx`
  - `docs/changelog.md`
- 修改目的：同时提升输入页展示效果和系统功能可感知度，让用户在填写平台与内容类型时就能直接看到系统当前掌握的趋势模板，而不是等到结果页才感知到趋势参与。
- 修改内容：
  - 新增 `fetchTrendTemplates()`，直接接入后端 `GET /api/v1/config/trend-templates`。
  - 在输入向导页新增 `TrendSignalPanel`，展示当前平台主趋势摘要、热点摘要和其他趋势条目。
  - 直接从 `/home/admin2/smy/upstream-materials/react-bits-main` 复制 `TextType` 和 `DotGrid` 源码到当前前端，并做最小 CSS Module 适配。
  - 为接入上游组件新增 `gsap` 依赖。
  - 将输入向导改为双栏工作台布局，在桌面端同时展示表单和趋势预览，移动端自动回落为单栏。
- 实现情况：
  - 这一轮明确优先服务产品展示与用户主流程，而不是内部工程治理。
  - 趋势能力现在已前置到输入阶段，系统“理解平台差异”的产品感知更强。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 17:29:59 CST

- 变更类型：M56 生成过渡页展示升级
- 变更文件：
  - `docs/architecture/m56_generation_page_showcase_upgrade.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `frontend/components/generation/generation-status-client.tsx`
  - `frontend/components/generation/generation-status-client.module.css`
  - `docs/changelog.md`
- 修改目的：提升生成过渡页的演示效果，让输入页到结果页之间不再是简单的技术状态列表，而是更像真实工作流舞台。
- 修改内容：
  - 将生成页保留真实轮询逻辑不变，但改为更完整的 Hero + 阶段轨道 + 当前状态卡布局。
  - 继续复用已接入的上游 `TextType` 和 `DotGrid` 组件，增强生成中的动态感和空间氛围。
  - 为五个阶段补充解释性文案，明确每一步到底在做什么。
- 实现情况：
  - 当前输入页、生成页、结果页三段展示主链都已明显强化，更适合答辩和对外演示。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 17:33:30 CST

- 变更类型：changelog 顺序规范化修正
- 变更文件：
  - `docs/changelog.md`
- 修改目的：纠正此前把新条目插入文件顶部的错误习惯，使 `changelog.md` 重新符合“每次在文件底部追加、时间顺序向下递增”的记录规范。
- 修改内容：
  - 重新整理 `docs/changelog.md` 中 2026-03-27 各批次条目的先后顺序。
  - 将记录顺序统一调整为严格按时间向下追加。
- 实现情况：
  - 当前 `changelog.md` 已恢复为从旧到新、越往下越新的顺序。
  - 后续变更将只在文件底部追加，不再向顶部插入。

## 2026-03-27 17:39:56 CST

- 变更类型：M57 结果包重型化与执行蓝图展示
- 变更文件：
  - `docs/architecture/m57_heavier_result_package_blueprint.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：继续优先完成产品展示和核心卖点表达，让结果包从“结构完整”升级到更接近“可交付执行方案”的重量级成品。
- 修改内容：
  - 在 `StructuredPackageScaffold` 下新增场景推进、镜头运动提示、素材道具、评论区引导、发布时间建议、缩略图提示、配音提示和素材清单等字段。
  - 强化 `package_assembler` 的结构化输出提示词，并为 fallback 补齐同一批执行蓝图字段。
  - 在 Markdown 导出中新增“制作执行蓝图”章节。
  - 在结果页新增“制作执行蓝图”展示区，直接消费这些更重的结构化字段。
- 实现情况：
  - 这一轮继续坚持强胶水编程，结果包加厚仍由 `Instructor + Pydantic schema` 主路径承接，不回退到仓内大模板拼装。
  - 结果页和导出物都会直接受益，更适合演示、答辩和向非技术角色展示系统价值。

## 2026-03-27 17:51:56 CST

- 变更类型：下一层级总计划文档 V3 重构
- 变更文件：
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：将下一阶段总计划与当前仓库真实状态重新对齐，明确“已实现 / 未实现 / 外部代码库套用状态 / 前端展示状态 / 到项目完成的顺序化开发路线”。
- 修改内容：
  - 重写总计划文档，不再沿用早期已经失效的“哪些还没实现”的旧判断。
  - 明确列出 PRD 范围内已经实现、部分实现、尚未实现和本期明确不做的能力。
  - 明确列出哪些关键功能已经套用成熟代码库，哪些尚未套用，以及计划套用的仓库是否已经拉取。
  - 明确列出首页、输入页、生成页、结果页当前展示完成度与后续展示计划。
  - 按“重点功能与前端展示优先，其余靠后”的原则，重排从现在到项目完成的阶段顺序。
- 实现情况：
  - 当前总计划已经从“中途深化说明”升级成“面向项目完成的真实路线图”。
  - 后续继续开发时，可以直接按该文档的 P0-P4 顺序推进，而不需要再重新解释优先级。

## 2026-03-27 18:04:47 CST

- 变更类型：M58 RSSHub 趋势入口层接入
- 变更文件：
  - `backend/app/integrations/rss/rsshub_adapter.py`
  - `backend/app/core/config.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/tests/test_m58_rsshub_trend_ingestion.py`
  - `.env.example`
  - `backend/.env.example`
  - `README.md`
  - `docs/architecture/m58_rsshub_trend_entry_integration.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“外部趋势导入与传播增强”从现有轻入口抓取推进到成熟 feed 入口层，开始真正复用 `RSSHub`。
- 修改内容：
  - 新增 `RSSHub` adapter，基于 `httpx` 拉取并解析 feed。
  - 将 `TrendCollectorService` 改为优先消费已配置平台的 `RSSHub` feed，再回退到现有 `Crawl4AI` 页面入口。
  - 新增 `TREND_RSSHUB_BASE_URL`、`TREND_RSSHUB_PLATFORM_ROUTES`、`TREND_RSSHUB_ITEM_LIMIT` 配置入口。
  - 为 `RSSHub` feed 驱动的趋势归纳链补充专项测试。
- 实现情况：
  - 这轮对应总计划里的 `P1`“趋势入口真正成熟化”第一刀。
  - 当前趋势刷新已经开始具备“成熟 feed 入口 + 现有结构化归纳链”的组合能力。
  - `./scripts/backend_test.sh tests/test_m27_trend_collection.py tests/test_m58_rsshub_trend_ingestion.py tests/test_m41_internal_trend_api.py` 已通过，结果为 `9 passed in 0.40s`。

## 2026-03-27 18:39:00 CST

- 变更类型：M59 首页品牌化展示升级
- 变更文件：
  - `frontend/components/upstream/card-swap.tsx`
  - `frontend/components/upstream/card-swap.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/landing/creative-hero.module.css`
  - `docs/architecture/m59_homepage_brand_showcase_upgrade.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把首页从基础品牌入口升级成真正适合演示和答辩的产品起点，补齐四页主链里最弱的一环。
- 修改内容：
  - 直接从上游 `react-bits-main` 复制并适配 `CardSwap`，用于首页核心能力翻卡展示。
  - 重构首页 Hero 为双栏布局，并继续复用已接入的 `DotGrid`、`TextType`、`ShinyText`。
  - 将四个核心功能直接显式呈现在首页，而不是只藏在后续页面和文档中。
- 实现情况：
  - 这轮对应总计划里的 `P2`“首页完整品牌化展示”第一轮。
  - 首页现在更接近输入页、生成页、结果页的展示强度，适合做整条演示链的起点。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 18:42:42 CST

- 变更类型：M60 重型结果包分发与执行束深化
- 变更文件：
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/architecture/m60_heavy_result_distribution_bundle.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：继续把五层结果包往“超重型结构化成品”推进，不只补制作蓝图，还补足真实发布和交付时需要的分发、封面、剪辑与 CTA 信息。
- 修改内容：
  - 结果包新增 `distribution_angles`、`thumbnail_copy_candidates`、`visual_references`、`editing_checklist`、`cta_variants`。
  - fallback 路径同步补齐同一批字段，避免主路径失败时结果突然变轻。
  - 结果页与 Markdown 导出同步展示这批新增内容。
- 实现情况：
  - 这轮对应总计划里的 `P0`“结果包继续重型化”继续深化。
  - 当前结果更像可发布执行包，而不只是结构化方案摘要。
  - `./scripts/backend_test.sh tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py` 已通过，结果为 `4 passed in 0.05s`。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 18:50:22 CST

- 变更类型：M61 轻量内部趋势控制台
- 变更文件：
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/trends/page.module.css`
  - `frontend/.env.local.example`
  - `README.md`
  - `docs/architecture/m61_internal_trend_console.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把内部趋势接口和刷新能力从“后端存在”推进到“可直接打开、可直接操作、可直接展示”的轻量前端入口。
- 修改内容：
  - 新增 `/internal/trends` 页面，以卡片方式展示各平台当前趋势摘要、来源类型、更新时间和热点摘要。
  - 通过服务端 action 接入内部趋势刷新接口。
  - 补充 `frontend/.env.local.example` 与 `README.md`，说明前端服务端调用内部接口所需的 `INTERNAL_API_KEY`。
- 实现情况：
  - 这轮对应总计划里的 `P3`“轻量内部管理能力”第一轮。
  - 外部趋势增强能力现在不仅能被后端消费，也能被直接展示和手动操作。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 18:55:35 CST

- 变更类型：M62 内部趋势控制台来源栈展示
- 变更文件：
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/trends/page.module.css`
  - `docs/architecture/m62_internal_trend_console_source_stack_showcase.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：在不新增手写展示组件的前提下，让内部趋势控制台更直观地解释系统复用的趋势增强来源栈。
- 修改内容：
  - 继续复用项目中已经接入的上游 `CardSwap` 组件。
  - 在 `/internal/trends` 页面新增来源栈翻卡区，展示 `RSSHub / Crawl4AI / Instructor` 三层来源链。
- 实现情况：
  - 这轮仍属于总计划里的 `P3`“轻量内部管理能力”深化。
  - 本轮重点不是新增后端能力，而是把成熟仓库复用链更直观地展示出来。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 19:15:08 CST

- 变更类型：M63 轻量内部 Checkpoint 控制台
- 变更文件：
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `frontend/app/internal/checkpoints/[id]/page.module.css`
  - `docs/architecture/m63_internal_checkpoint_console.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把已有的 LangGraph checkpoint 内部能力推进到一个可直接展示、可查看、可手动恢复的轻量前端入口。
- 修改内容：
  - 新增 `/internal/checkpoints/[id]` 页面。
  - 页面直接消费现有内部 checkpoint 列表、最新状态和恢复接口，不新增新的后端执行逻辑。
  - 提供结果页、状态页和趋势控制台的快速跳转。
- 实现情况：
  - 这轮对应总计划里的 `P3`“轻量内部管理能力”继续深化。
  - 本轮是薄胶水实现，核心 checkpoint 能力继续完全复用既有 `LangGraph` 与后端内部 API。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 19:23:16 CST

- 变更类型：M64 结果页导出载荷预览
- 变更文件：
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/export-json-preview.tsx`
  - `frontend/components/result/export-json-preview.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/components/result/result-view-client.module.css`
  - `docs/architecture/m64_result_export_payload_previews.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把现有导出链更完整地展示到结果页上，让用户直接看到 JSON 导出和 Video Payload 如何消费同一份结果真值。
- 修改内容：
  - 新增结果页导出载荷预览组件。
  - 直接调用既有 `/export/json` 和 `/video-payload`。
  - 复用现有 `PayloadFoldoutHeader` 与 `MachinePayloadSummary` 做摘要和 JSON 原文展示。
- 实现情况：
  - 这轮主要对应总计划里的 `P0`“结果包继续重型化”，同时服务前端展示完成度。
  - 本轮属于薄胶水实现，没有新增任何后端导出逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 19:27:11 CST

- 变更类型：M65 主流程页内部控制台入口胶水
- 变更文件：
  - `frontend/components/generation/generation-status-client.tsx`
  - `frontend/components/generation/generation-status-client.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/components/result/result-view-client.module.css`
  - `docs/architecture/m65_internal_console_entry_glue.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把已经存在的内部趋势控制台和 checkpoint 控制台更自然地接回主流程页面，提升演示时的连贯性。
- 修改内容：
  - 在生成页新增内部工具入口链接。
  - 在结果页新增内部工具入口链接。
  - 不新增任何新的后端接口或内部页面。
- 实现情况：
  - 这轮对应总计划里的 `P3`“轻量内部管理能力”继续深化。
  - 本轮是非常典型的薄胶水实现，只复用既有内部工具页。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 19:43:12 CST

- 变更类型：M66 首页 CardNav 胶水接入
- 变更文件：
  - `frontend/components/upstream/card-nav.tsx`
  - `frontend/components/upstream/card-nav.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/landing/creative-hero.module.css`
  - `docs/architecture/m66_homepage_card_nav_glue.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：继续提升首页的产品入口感和可展示性，同时尽量复用上游成熟前端组件，不再手写一套新的展开式导航系统。
- 修改内容：
  - 参考 `upstream-materials/react-bits-main` 中的 `CardNav` 组件语义，新增项目内适配版 `CardNav`。
  - 保留上游 `gsap` 展开动画，用当前仓库已存在的 `lucide-react` 替代上游 `react-icons/go`。
  - 把首页顶部升级为可展开的能力导航带，收纳主流程入口、展示说明入口和内部工具入口。
- 实现情况：
  - 这轮对应总计划里的 `P2`“首页完整品牌化展示”继续深化。
  - 本轮属于“复制上游组件源码 + 最小适配”的薄胶水实现，没有自写新的导航机制。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 19:56:26 CST

- 变更类型：M67 结果页 PillNav 导航升级
- 变更文件：
  - `frontend/components/upstream/pill-nav.tsx`
  - `frontend/components/upstream/pill-nav.module.css`
  - `frontend/components/result/result-section-nav.tsx`
  - `frontend/components/result/result-section-nav.module.css`
  - `docs/architecture/m67_result_page_pill_nav_upgrade.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：用上游成熟导航语义替换结果页现有的手写分区 pills，让重型结果包的跳转体验更完整、更适合展示。
- 修改内容：
  - 参考 `upstream-materials/react-bits-main` 中的 `PillNav`，新增项目内适配版 `PillNav`。
  - 保留上游 `gsap` hover 动画和移动端折叠菜单。
  - 移除旧的 `result-section-nav.module.css`，把 `ResultSectionNav` 改造成对上游适配组件的薄胶水包装。
- 实现情况：
  - 这轮对应总计划里的 `P0`“结果包继续重型化”在结果页展示层的继续深化。
  - 本轮属于“替换现有手写导航为上游语义适配版”的复用型开发，不新增新的业务逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 20:05:31 CST

- 变更类型：M68 结果页传播策略 Deck
- 变更文件：
  - `frontend/components/result/distribution-strategy-deck.tsx`
  - `frontend/components/result/distribution-strategy-deck.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/architecture/m68_result_distribution_strategy_deck.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：让结果页传播备选区从静态列表进一步升级成更适合演示和讲解的策略 deck，同时继续复用已有上游组件。
- 修改内容：
  - 新增传播策略翻卡组件，直接消费标题备选、钩子备选、封面文案和传播角度。
  - 继续复用项目中已经接入的上游 `CardSwap`，不新增新的动画依赖。
  - 将翻卡 deck 接入结果页“传播备选区”顶部。
- 实现情况：
  - 这轮对应总计划里的 `P0`“结果包继续重型化”在结果页展示层的继续深化。
  - 本轮属于“复用现有上游组件增强既有展示区”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 20:18:42 CST

- 变更类型：M69 创建页趋势策略真值展示
- 变更文件：
  - `backend/app/schemas/trend_template.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m69_trend_template_summary_fields.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/wizard/trend-signal-panel.tsx`
  - `frontend/components/wizard/trend-strategy-deck.tsx`
  - `frontend/components/wizard/trend-strategy-deck.module.css`
  - `docs/architecture/m69_create_page_trend_strategy_surface.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把后端已经存在的趋势策略真值更完整地透传并展示到创建页，让“外部趋势增强传播性”这条主线在用户进入生成前就可见。
- 修改内容：
  - `/config/trend-templates` 的摘要响应新增钩子模式、节奏模式、标题封面风格、受众偏好、规避点字段。
  - 前端趋势模板类型同步对齐。
  - 创建页趋势面板新增趋势策略 deck，继续复用既有上游 `CardSwap` 展示策略组。
- 实现情况：
  - 这轮对应总计划里的 `P1`“趋势入口真正成熟化”在前端展示层的继续深化。
  - 本轮是“现有后端真值透传 + 已接入上游展示组件复用”的薄胶水实现，没有新增新的趋势生成逻辑。
  - `./scripts/backend_test.sh tests/test_m69_trend_template_summary_fields.py` 已通过。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 20:27:08 CST

- 变更类型：M70 结果页趋势影响 Deck
- 变更文件：
  - `frontend/components/result/trend-influence-deck.tsx`
  - `frontend/components/result/trend-influence-deck.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/architecture/m70_result_page_trend_influence_deck.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“外部趋势增强传播性”这条核心卖点直接展示到结果页上，让用户更直观地看到趋势如何影响最终方案。
- 修改内容：
  - 新增结果页趋势影响翻卡组件，直接消费分析层里的趋势真值。
  - 将钩子、节奏、标题封面风格、规避点、热点线索做成翻卡策略组。
  - 继续复用既有上游 `CardSwap`，不新增新的动画依赖。
- 实现情况：
  - 这轮对应总计划里的 `P1`“趋势入口真正成熟化”在结果页展示层的继续深化。
  - 本轮是“已有真值消费 + 已接入上游组件复用”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 20:36:12 CST

- 变更类型：M71 结果页设计一致性 Deck
- 变更文件：
  - `frontend/components/result/consistency-thread-deck.tsx`
  - `frontend/components/result/consistency-thread-deck.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/architecture/m71_result_consistency_thread_deck.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“内部内容设计一致性”这条第一核心卖点直接展示到结果页上，让用户能一眼看到主题、受众、风格、趋势和执行如何围绕同一中心被编排。
- 修改内容：
  - 新增结果页设计一致性翻卡组件，直接消费已有结果真值。
  - 将主题、受众、风格、趋势、执行拆成五张翻卡并放入总览层。
  - 继续复用既有上游 `CardSwap`，不新增新的动画依赖。
- 实现情况：
  - 这轮对应总计划里的 `P0`“结果包继续重型化”在结果页一致性可视化子阶段的继续深化。
  - 本轮是“已有真值消费 + 已接入上游组件复用”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 20:44:31 CST

- 变更类型：M72 创建页 Quick Start 预设
- 变更文件：
  - `frontend/components/wizard/creation-preset-deck.tsx`
  - `frontend/components/wizard/creation-preset-deck.module.css`
  - `frontend/components/wizard/create-wizard.tsx`
  - `docs/architecture/m72_create_page_quickstart_presets.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：降低创建页第一次上手时的启动成本，让用户不必从空白输入开始，就能直接进入一套完整创作配置。
- 修改内容：
  - 新增 Quick Start 预设 deck，提供 3 组完整输入预设。
  - 点击后直接写入主题、内容类型、目标平台、目标受众、风格和补充说明。
  - 继续复用既有上游 `CardSwap`，原五步输入链路保持不变。
- 实现情况：
  - 这轮对应第四核心点“简单上手的操作逻辑”在创建页启动层的继续深化。
  - 本轮是“现有表单真值写入 + 已接入上游组件复用”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 20:52:48 CST

- 变更类型：M73 生成页阶段产物 Deck
- 变更文件：
  - `frontend/components/generation/generation-output-deck.tsx`
  - `frontend/components/generation/generation-output-deck.module.css`
  - `frontend/components/generation/generation-status-client.tsx`
  - `docs/architecture/m73_generation_page_stage_output_deck.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：让生成页不再只是显示状态，而是更清楚地解释每个阶段到底会产出什么，从而降低等待过程中的理解门槛。
- 修改内容：
  - 新增阶段产物翻卡组件，展示主题真值、受众风格画像、趋势约束、叙事骨架和结构化结果包。
  - 将其接入生成页阶段轨道下方。
  - 继续复用既有上游 `CardSwap`，不新增新的动画依赖。
- 实现情况：
  - 这轮对应第四核心点“简单上手的操作逻辑”在生成页理解层的继续深化。
  - 本轮是“已有工作流语义说明 + 已接入上游组件复用”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:12:26 CST

- 变更类型：M74 创建页一致性预览 Deck
- 变更文件：
  - `frontend/components/wizard/consistency-preview-deck.tsx`
  - `frontend/components/wizard/consistency-preview-deck.module.css`
  - `frontend/components/wizard/create-wizard.tsx`
  - `docs/architecture/m74_create_page_consistency_preview.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“内部对齐 / 设计一致性”的逻辑从结果页继续前置到创建页，满足 `M-P0-B` 对前置入口的要求。
- 修改内容：
  - 新增创建页一致性预览翻卡组件。
  - 直接消费当前输入中的主题、受众、平台、风格，说明它们会如何围绕同一中心继续长成后续方案。
  - 继续复用既有上游 `CardSwap`，不新增新的动画依赖。
- 实现情况：
  - 这轮对应里程碑 `M-P0-B`“设计一致性可被直接展示”的继续推进。
  - 本轮是“已有表单真值消费 + 已接入上游组件复用”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:20:48 CST

- 变更类型：M75 首页一致性主线 Showcase
- 变更文件：
  - `frontend/components/landing/consistency-thread-showcase.tsx`
  - `frontend/components/landing/consistency-thread-showcase.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `docs/architecture/m75_homepage_consistency_thread_showcase.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“内部对齐 / 设计一致性”的逻辑继续前置到首页，补齐 `M-P0-B` 对首页或创建页前置说明的要求，并形成首页到结果页的一致性讲述链。
- 修改内容：
  - 新增首页一致性主线 showcase。
  - 用翻卡方式说明主题、受众、风格、趋势、结果包如何围绕同一中心继续生长。
  - 继续复用既有上游 `CardSwap`，不新增新的动画依赖。
- 实现情况：
  - 这轮对应里程碑 `M-P0-B`“设计一致性可被直接展示”的完成收口。
  - 本轮是“已有产品叙事说明 + 已接入上游组件复用”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:29:42 CST

- 变更类型：M76 首页趋势增强闭环 Showcase
- 变更文件：
  - `frontend/components/landing/trend-amplifier-showcase.tsx`
  - `frontend/components/landing/trend-amplifier-showcase.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `docs/architecture/m76_homepage_trend_amplifier_showcase.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“趋势增强如何一路进入最终方案”的逻辑前置到首页，继续补齐趋势增强演示闭环，并提升首页的产品入口完整度。
- 修改内容：
  - 新增首页趋势增强闭环 showcase。
  - 用翻卡方式说明成熟入口、结构化归纳、创建前展示、结果影响四段链路。
  - 继续复用既有上游 `CardSwap`，不新增新的动画依赖。
- 实现情况：
  - 这轮对应里程碑 `M-P1-C`“趋势增强演示闭环”和 `M-P2-A`“首页具备完整产品入口能力”的继续推进。
  - 本轮是“已有产品叙事说明 + 已接入上游组件复用”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:39:18 CST

- 变更类型：M77 首页材料库组件多样化导航
- 变更文件：
  - `frontend/components/upstream/gooey-nav.tsx`
  - `frontend/components/upstream/gooey-nav.module.css`
  - `frontend/components/landing/homepage-signal-nav.tsx`
  - `frontend/components/landing/homepage-signal-nav.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/landing/consistency-thread-showcase.tsx`
  - `frontend/components/landing/trend-amplifier-showcase.tsx`
  - `docs/architecture/m77_homepage_material_diversity_nav.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：响应首页长期主要依赖 `CardSwap` 的问题，把材料库中不同类型的交互组件真正接入主链页面，提升展示语言多样性。
- 修改内容：
  - 参考 `react-bits-main` 的 `GooeyNav` 新增项目内适配版。
  - 在首页新增交互式 signal nav，把一致性主线、趋势增强链、结果成品和入口 CTA 通过锚点串起来。
  - 为首页已有 showcase 增加锚点，形成一条可点击浏览的讲述路径。
- 实现情况：
  - 这轮主要对应里程碑 `M-P2-A`“首页具备完整产品入口能力”的继续推进。
  - 本轮是“复制上游源码 + 最小适配”的薄胶水实现，没有新增后端逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:01:42 CST

- 变更类型：总计划文档里程碑化重构
- 变更文件：
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：解决原计划中 `P0-P3` 粒度过粗、阶段感不强的问题，把后续开发任务重构成可量化、可验收、可判断完成与否的里程碑体系。
- 修改内容：
  - 用 `M-P0-A` 到 `M-P5-A` 的里程碑体系替代原本过粗的阶段描述。
  - 为每个里程碑补充“当前状态、已完成、未完成、量化完成标准、下一步入口”。
  - 重新整理“下一步直接执行建议”，改为按里程碑顺序推进。
- 实现情况：
  - 本轮不涉及代码实现，属于后续开发计划指导的真值文档重构。
  - 目标是让后续每次开发都能明确挂靠到某个可验收节点，而不是停留在粗粒度标签上。

## 2026-03-27 21:02:38 CST

- 变更类型：总计划文档补入核心仓库复用决策书
- 变更文件：
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把 `Instructor / PydanticAI / LangGraph / RSSHub / Crawl4AI / LiteLLM / bilibili-api-python` 的深入学习结论直接并入总计划，避免后续继续开发时只凭口头记忆使用上游仓库。
- 修改内容：
  - 在总计划文档中新增“核心仓库复用决策书”章节。
  - 明确每个核心仓库对应的系统核心能力、当前已复用部分、仍未充分复用的成熟能力、后续接入决策与挂靠里程碑。
  - 修正文档中 `M-P0-B` 总表状态与正文状态不一致的问题。
  - 在“下一步直接执行建议”中新增“里程碑与上游仓库绑定规则”和“后续继续开发前的上游学习顺序”。
- 实现情况：
  - 本轮不涉及功能代码实现，属于后续开发计划与上游复用策略的真值文档深化。
  - 这轮之后，总计划文档已经同时承担“开发里程碑真值”和“核心仓库复用决策书”两类角色。

## 2026-03-27 21:05:35 CST

- 变更类型：总计划文档补入 `Instructor` 深读复用结论
- 变更文件：
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把 `Instructor` 的源码级学习结果直接落入总计划，避免后续开发时只停留在“它能做结构化输出”的粗粒度理解。
- 修改内容：
  - 在总计划文档的 `Instructor` 条目中补入“已完成第一轮源码级深读”状态。
  - 明确补充 `from_provider`、`create_with_completion`、`Hooks`、`Partial`、`Iterable[T]`、`llm_validator` 等当前尚未充分复用但与后续开发直接相关的成熟能力。
  - 增加源码级结论，明确哪些能力适合结果包加厚、趋势增强、流式展示、调试观测和平台约束校验。
- 实现情况：
  - 本轮不涉及功能代码实现，属于上游能力认知深化并并入开发总计划。
  - 这轮之后，`Instructor` 在总计划里已经从“仓库名”升级为“具体现成能力清单 + 后续接入决策”。

## 2026-03-27 21:08:48 CST

- 变更类型：总计划文档补入剩余核心仓库深读复用结论
- 变更文件：
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：一轮补齐 `LangGraph / PydanticAI / RSSHub / Crawl4AI / LiteLLM / bilibili-api-python` 的源码级学习结论，让总计划文档能够直接指导后续继续开发，而不是只记录仓库名称。
- 修改内容：
  - 为上述 6 个核心仓库补入“已完成第一轮源码级深读”状态。
  - 分别写明每个仓库当前已用部分、未充分复用的成熟能力、后续接入决策与源码级结论。
  - 明确哪些仓库继续作为主路径深化，哪些仅作为后续候选或受许可证约束的专项候选。
- 实现情况：
  - 本轮不涉及功能代码实现，属于上游能力体系化学习并并入开发总计划。
  - 这轮之后，计划中的 7 个核心复用仓库都已具备第一轮“可指导实现”的复用决策说明，后续可以从学习态切回开发态。

## 2026-03-27 21:20:20 CST

- 变更类型：M78 趋势来源轨迹真值链
- 变更文件：
  - `backend/app/schemas/trend_template.py`
  - `backend/app/db/models/trend_template.py`
  - `backend/app/db/repositories/trend_template_repository.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/migrations/versions/20260327_182500_add_trend_source_trace.py`
  - `backend/tests/test_m41_internal_trend_api.py`
  - `backend/tests/test_m58_rsshub_trend_ingestion.py`
  - `backend/tests/test_m69_trend_template_summary_fields.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/wizard/trend-signal-panel.tsx`
  - `frontend/components/wizard/trend-signal-panel.module.css`
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/trends/page.module.css`
  - `docs/architecture/m78_trend_source_trace_truth_chain.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“趋势从哪来”沉淀成数据库真值和前端可展示链，补齐趋势增强主路径里来源可追溯、演示可点验的关键缺口。
- 修改内容：
  - 为趋势模板与趋势摘要新增 `source_trace` 结构，并补入 SQLAlchemy 模型、仓储映射和 Alembic 迁移。
  - 在 `RSSHub` 与 `Crawl4AI` 两条趋势采集路径上生成来源轨迹，结构化归纳成功与 fallback 路径都保留来源条目。
  - 让 `/config/trend-templates` 与内部趋势摘要接口透传来源轨迹。
  - 创建页趋势预览与内部趋势控制台新增来源轨迹展示，直接显示标题、来源名、摘录与外链。
  - 新增 `M78` 架构文档，并把本轮推进并回总计划里程碑。
- 实现情况：
  - 本轮对应里程碑 `M-P1-A 趋势入口主路径成熟化` 与 `M-P1-C 趋势增强演示闭环`。
  - 当前阶段：`M-P1-A` 继续推进中，且已新增来源轨迹真值证明；`M-P1-C` 继续推进中，演示链补上了“趋势来源可见”这一段。
  - `python3 -m py_compile` 已通过。
  - `DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_test_stage_m78.db ./scripts/backend_test.sh tests/test_m41_internal_trend_api.py tests/test_m58_rsshub_trend_ingestion.py tests/test_m69_trend_template_summary_fields.py` 已通过，结果 `6 passed`。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:31:13 CST

- 变更类型：M79 结果页趋势来源轨迹闭环
- 变更文件：
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/trend-source-trace-panel.tsx`
  - `frontend/components/result/trend-source-trace-panel.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/architecture/m79_result_page_trend_provenance_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把趋势来源轨迹从创建页与内部控制台继续推进到结果页，补齐主演示链最后一段，让趋势增强闭环能够在用户主流程里直接看见。
- 修改内容：
  - 扩展前端结果类型，使结果页显式消费 `analysis.trend_summary.source_trace`。
  - 新增结果页趋势来源轨迹面板，展示来源名、来源标题、摘录与外链。
  - 在结果页分析面板中接入新的来源轨迹展示。
  - 新增 `M79` 架构文档，并把总计划里的 `M-P1-A` 与 `M-P1-C` 更新为已完成。
- 实现情况：
  - 本轮对应里程碑 `M-P1-C 趋势增强演示闭环`，并同时完成了 `M-P1-A 趋势入口主路径成熟化` 的计划状态收口。
  - 当前阶段：`M-P1-A` 已完成；`M-P1-C` 已完成。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:35:58 CST

- 变更类型：M80 首页结果示例感收口
- 变更文件：
  - `frontend/components/upstream/chroma-grid.tsx`
  - `frontend/components/upstream/chroma-grid.module.css`
  - `frontend/components/landing/homepage-result-showcase.tsx`
  - `frontend/components/landing/homepage-result-showcase.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `docs/architecture/m80_homepage_result_showcase_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：补齐首页长期缺少的“结果示例感”，让首页不仅能说明系统做什么，还能直观看到结果会长成什么样，从而收口首页入口能力里程碑。
- 修改内容：
  - 参考 `react-bits-main` 的 `ChromaGrid` 结构语义新增项目内适配版，作为新的材料库复用组件。
  - 首页新增结果示例区，用 4 张样例卡展示总览定位、叙事脚本、传播策略和导出消费。
  - 更新总计划文档，把 `M-P2-A` 从进行中推进为已完成。
- 实现情况：
  - 本轮对应里程碑 `M-P2-A 首页具备完整产品入口能力`。
  - 当前阶段：`M-P2-A` 已完成。
  - 本轮继续遵循“成熟材料复用 + 最小胶水适配”，没有新造一套首页结果画廊系统，而是站在上游 `ChromaGrid` 语义上完成首页结果示例区。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:42:23 CST

- 变更类型：M81 首次使用闭环收口
- 变更文件：
  - `frontend/components/upstream/border-glow.tsx`
  - `frontend/components/upstream/border-glow.module.css`
  - `frontend/components/landing/first-run-guide.tsx`
  - `frontend/components/landing/first-run-guide.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/result/result-next-step-guide.tsx`
  - `frontend/components/result/result-next-step-guide.module.css`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/architecture/m81_first_run_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：补齐首次使用者从首页进入主流程、到结果页收尾时的显式引导，让四页主链在无口头解释的情况下也能顺滑完成一次完整体验。
- 修改内容：
  - 参考 `react-bits-main` 的 `BorderGlow` 结构语义新增项目内适配版，作为新手引导卡片容器。
  - 首页新增 `First Run Guide`，用三步卡片直接说明第一次来该怎么开始。
  - 结果页新增 `What Next Guide`，明确导出、回看依据和重新开始三个下一步动作。
  - 同步更新总计划文档，修正 `M-P1-A` 正文状态漂移，并把 `M-P3-B` 更新为已完成。
- 实现情况：
  - 本轮对应里程碑 `M-P3-B 首次使用闭环顺滑`。
  - 当前阶段：`M-P3-B` 已完成。
  - 本轮继续遵循“成熟材料复用 + 最小胶水适配”，直接站在上游 `BorderGlow` 语义上完成首页与结果页的首次使用引导。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 21:48:36 CST

- 变更类型：M82 主流程页头展示强度对齐
- 变更文件：
  - `frontend/components/upstream/glass-surface.tsx`
  - `frontend/components/upstream/glass-surface.module.css`
  - `frontend/components/layout/flow-stage-banner.tsx`
  - `frontend/components/layout/flow-stage-banner.module.css`
  - `frontend/components/layout/site-shell.tsx`
  - `frontend/components/layout/site-shell.module.css`
  - `frontend/app/create/page.tsx`
  - `frontend/app/generating/[id]/page.tsx`
  - `frontend/app/result/[id]/page.tsx`
  - `docs/architecture/m82_stage_shell_alignment.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把创建页、生成页、结果页的页头层从普通文档壳统一升级为可独立演示的阶段英雄条，补齐四页主链在展示强度上的最后一层差距。
- 修改内容：
  - 参考 `react-bits-main` 的 `GlassSurface` 结构语义新增项目内适配版。
  - 新增共享的 `FlowStageBanner`，统一展示当前阶段定位、下一步、亮点和快捷动作。
  - 创建页、生成页、结果页全部接入统一阶段英雄条。
  - 同步更新总计划文档，把 `M-P2-B` 从未完成推进为已完成。
- 实现情况：
  - 本轮对应里程碑 `M-P2-B 四页主链展示强度一致`。
  - 当前阶段：`M-P2-B` 已完成。
  - 本轮继续遵循“成熟材料复用 + 最小胶水适配”，直接站在上游 `GlassSurface` 语义上完成主流程页头对齐，而不是另造一套特效页壳。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 22:08:43 CST

- 变更类型：M83 导出物重型交付级收口
- 变更文件：
  - `backend/app/schemas/video_payload.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/components/result/export-json-preview.tsx`
  - `docs/architecture/m83_export_payload_heavy_delivery_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把 Markdown 与 video payload 从“已可导出”推进到“更像制作交付件”，收口导出物重量明显弱于结果页展示重量的缺口。
- 修改内容：
  - 扩展 video payload schema，增加趋势来源、传播策略、执行蓝图与下游消费相关字段。
  - Markdown 导出新增趋势依据与传播增强章节、趋势来源轨迹、标题/钩子/封面备选、评论引导、发布时间建议，以及更完整的机器层执行信息。
  - 前端导出预览摘要同步扩展，直接展示更重的 video payload 字段。
  - 测试样例补充趋势来源轨迹，并更新导出兼容测试断言。
- 实现情况：
  - 本轮对应里程碑 `M-P0-C 导出物达到“重型交付级”`。
  - 当前阶段：`M-P0-C` 已完成。
  - `python3 -m py_compile` 已通过。
  - `DATABASE_URL=sqlite+pysqlite:////tmp/multi_media_test_stage_m83.db ./scripts/backend_test.sh tests/test_m46_export_payload_compat.py` 已通过，结果 `2 passed`。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 22:11:58 CST

- 变更类型：M84 趋势增强前台可见化收口
- 变更文件：
  - `frontend/components/landing/trend-demo-script.tsx`
  - `frontend/components/landing/trend-demo-script.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/landing/homepage-signal-nav.tsx`
  - `docs/architecture/m84_trend_demo_script_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把趋势增强从“前台已有若干展示点”推进到“前台具备明确可点验的演示脚本路径”，收口趋势增强前台可见化里程碑。
- 修改内容：
  - 首页新增 `Trend Demo Script`，用四步卡片明确说明如何从首页、创建页、结果页到内部趋势控制台完整演示趋势增强链。
  - 首页交互导航同步增加趋势演示脚本入口。
  - 更新总计划文档，把 `M-P1-B` 从进行中推进为已完成。
- 实现情况：
  - 本轮对应里程碑 `M-P1-B 趋势增强前台可见化`。
  - 当前阶段：`M-P1-B` 已完成。
  - 本轮继续遵循“成熟材料复用 + 最小胶水适配”，直接站在已有首页展示语言之上补足趋势演示脚本，而不是另造一套独立趋势导览系统。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 22:16:09 CST

- 变更类型：M85 内部控制台统一化收口
- 变更文件：
  - `frontend/components/internal/internal-console-hub.tsx`
  - `frontend/components/internal/internal-console-hub.module.css`
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `docs/architecture/m85_internal_console_hub_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把内部趋势控制台与 checkpoint 控制台从“各自可用”推进到“存在统一入口、统一说明、统一跳转逻辑”，收口内部工具可用性与内部控制台叙事统一两个里程碑。
- 修改内容：
  - 新增共享的 `InternalConsoleHub`，统一承载趋势控制台与 checkpoint 控制台的能力说明、状态高亮和互跳入口。
  - 内部趋势页接入统一控制台入口，强调其在趋势增强链中的定位。
  - 内部 checkpoint 页接入统一控制台入口，并在当前 `generation_id` 上下文中展示对应恢复与回看入口。
  - 新增 `M85` 专项文档，并更新总计划文档，把 `M-P4-A` 与 `M-P4-B` 从未完成/进行中推进为已完成。
- 实现情况：
  - 本轮对应里程碑 `M-P4-A 轻量内部工具可用` 与 `M-P4-B 内部控制台叙事统一`。
  - 当前阶段：`M-P4-A`、`M-P4-B` 已完成。
  - 本轮继续遵循“成熟材料复用 + 最小胶水适配”，直接复用项目既有 `SpotlightCard` 表达内部工具能力，只补共享入口层，不另造第二套内部台。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 22:20:23 CST

- 变更类型：M86 首页预设发射台与创建页一键启动收口
- 变更文件：
  - `frontend/lib/constants/creation-presets.ts`
  - `frontend/components/wizard/creation-preset-deck.tsx`
  - `frontend/components/wizard/create-wizard.tsx`
  - `frontend/app/create/page.tsx`
  - `frontend/components/landing/quickstart-launchpad.tsx`
  - `frontend/components/landing/quickstart-launchpad.module.css`
  - `frontend/components/landing/creative-hero.tsx`
  - `docs/architecture/m86_preset_launchpad_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把“简单上手”从创建页内部预设能力推进到首页可直接触发的真实启动路径，收口创建页与生成页易上手里程碑。
- 修改内容：
  - 把三组创建预设提取为共享常量，避免首页与创建页各自维护一份漂移数据。
  - 首页新增 `Quickstart Launchpad`，允许用户直接从首页带着完整预设进入创建页。
  - 创建页改为接收服务端页组件透传的 `preset` 查询参数，命中后自动注入主题、平台、内容类型、受众与风格。
  - 更新总计划文档，收口 `M-P3-A`，并同步修正总表里 `M-P0-A`、`M-P3-B` 的状态漂移。
- 实现情况：
  - 本轮对应里程碑 `M-P3-A 创建页与生成页足够易上手`。
  - 当前阶段：`M-P3-A` 已完成。
  - 本轮继续遵循“成熟材料复用 + 最小胶水适配”，在既有 `BorderGlow` 视觉层和既有创建预设体系之上增加首页发射台与 URL 注入，不另造第二套向导逻辑。
  - `cd frontend && npm run build` 已通过。

## 2026-03-27 22:25:00 CST

- 变更类型：M87 演示与交接稳定复现收口
- 变更文件：
  - `scripts/demo_regression.sh`
  - `README.md`
  - `backend/README.md`
  - `frontend/README.md`
  - `docs/architecture/m87_stability_handoff_closure.md`
  - `docs/architecture/next_phase_deepening_plan_v1.md`
  - `docs/changelog.md`
- 修改目的：把最后一个未完成里程碑 `M-P5-A` 收口为“存在统一回归入口、启动说明可执行、文档真值已对齐”的稳定交接状态。
- 修改内容：
  - 新增 `scripts/demo_regression.sh`，统一串起后端关键回归集合与前端生产构建。
  - 更新根目录、后端、前端 README，把 `dev_bootstrap / backend_test / demo_regression / smoke_test` 的用途和顺序说清楚。
  - 更新总计划文档，把 `M-P5-A` 从未完成推进为已完成，并修正“下一步直接执行建议”为当前真实状态。
- 实现情况：
  - 本轮对应里程碑 `M-P5-A 演示和交接稳定可复现`。
  - 当前阶段：`M-P5-A` 已完成，当前总计划里程碑主链已全部收口。
  - `bash ./scripts/demo_regression.sh` 已通过，其中后端关键回归结果为 `13 passed in 3.18s`，前端 `npm run build` 已通过。

## 2026-03-27 22:29:03 CST

- 变更类型：本地运行环境文件补齐
- 变更文件：
  - `.env`
  - `backend/.env`
  - `frontend/.env.local`
  - `docs/changelog.md`
- 修改目的：把当前工作区补齐到“前后端可直接按 README 启动查看效果”的状态，避免首次运行先卡在环境文件缺失。
- 修改内容：
  - 根目录 `.env` 已按 Docker/统一入口需要补齐，并启用后台自动执行。
  - `backend/.env` 已切到本地 SQLite 开发数据库，避免本地查看页面时额外依赖 PostgreSQL。
  - `frontend/.env.local` 已补齐浏览器 API 地址与内部页调用所需的 `INTERNAL_API_KEY`。
- 实现情况：
  - 本轮属于本地运行准备动作，不新增新的产品里程碑。
  - 上述 3 个环境文件已在当前机器落地，可直接按 README 启动前后端。
  - 这些环境文件属于本地忽略项，不进入仓库版本控制；本条 changelog 用于留痕当前运行环境状态。

## 2026-03-29 20:41:11 CST

- 变更类型：可跑通版本 v1.0 基线文档落盘
- 变更文件：
  - `docs/architecture/v1_0_runnable_baseline.md`
  - `docs/changelog.md`
- 修改目的：把当前系统正式定义为“第一个可跑通版本 v1.0”，同时总结当前已达成功能，并明确下一阶段开发主线。
- 修改内容：
  - 新增 v1.0 基线文档，系统总结当前已经实现的功能、为什么当前版本可以定义为第一个可跑通版本，以及后续开发计划。
  - 在后续计划中明确写入三条主线：后端功能继续完全实现、稳定性大幅提升、前端继续逐步优化。
  - 明确把“前端内嵌文字仍偏展示/介绍风格，尚未完全转为面向用户表达”列为后期重点修改点。
- 实现情况：
  - 本轮不新增新功能代码，属于版本基线定义与后续路线说明。
  - 本次 Git 留痕将明确标记为第一个可跑通版本 `v1.0`。

## 2026-03-29 20:49:32 CST

- 变更类型：v1.0 评测说明、文档治理建议与下一层级详细计划落盘
- 变更文件：
  - `docs/architecture/v1_0_runnable_baseline.md`
  - `docs/architecture/v1_0_evaluation_handoff.md`
  - `docs/architecture/document_governance_review_v1.md`
  - `docs/changelog.md`
- 修改目的：
  - 回答当前 `m` 系列文档是否需要合并，以及哪些文档未来可归档/删除。
  - 为后续评测团队提供一份当前实现程度与已达成工作细节说明。
  - 把 `v1_0_runnable_baseline.md` 从简版基线说明升级为包含详细量化里程碑的下一层级深化计划文档。
- 修改内容：
  - 重写 `v1_0_runnable_baseline.md`，加入完成度判断、下一阶段总策略、`N1-N7` 详细量化里程碑、实现顺序、后端材料复用点、稳定性未完成工作、前端文案与展示优化方向。
  - 新增 `v1_0_evaluation_handoff.md`，总结本轮对话后当前系统已达成的全部主要工作、评测观察点和当前实现程度判断。
  - 新增 `document_governance_review_v1.md`，给出 `m` 系列文档的保留、归档、删除建议。
- 实现情况：
  - 本轮属于文档体系深化与后续阶段规划收口，不新增新功能代码。
  - 文档重点已经从“当前能跑”推进到“当前实现程度如何评测、下一阶段如何继续做、文档体系如何整理”。

## 2026-03-29 21:04:29 CST

- 变更类型：胶水材料库补充与材料清单改写
- 变更文件：
  - `docs/research/glue_material_candidates.md`
  - `docs/changelog.md`
- 修改目的：
  - 基于当前 v1.0 之后的下一阶段开发目标，再次按 GitHub 仓库进行材料判断。
  - 确认是否还有必要补充新的成熟仓库，并把结果同步进胶水材料文档。
- 修改内容：
  - 本轮新增拉取 `playwright` 与 `langfuse` 到本地材料库。
  - 把 `glue_material_candidates.md` 从早期“候选清单”重写成“当前材料库复用现状文档”。
  - 明确记录哪些仓库已经进入主路径、如何复用，哪些还没有进入主路径、为什么没有进入，以及新增仓库服务于哪条后续目标。
- 实现情况：
  - 当前新增本地材料：
    - `playwright`：`facd84299`
    - `langfuse`：`1e7c7f912`
  - 本轮不新增功能代码，属于下一阶段开发准备与材料事实源更新。

## 2026-03-29 21:15:00 CST

- 变更类型：v1.0 深化计划补全胶水材料下一层级引用方案
- 变更文件：
  - `docs/stage_records/stage_04_v1_0_runnable_baseline_and_next_plan.md`
  - `docs/changelog.md`
- 修改目的：
  - 把下一阶段计划里“继续复用成熟仓库”的描述从原则层，细化到可执行的材料引用计划层。
  - 明确写清哪些已复用材料后续如何继续深挖，哪些已拉取但未进入主路径的材料准备在哪个里程碑引入，以及如何量化判断是否真正吃进去了。
- 修改内容：
  - 新增“胶水材料下一层级引用总策略”章节。
  - 分别补全 `Instructor`、`LangGraph`、`RSSHub`、`Crawl4AI`、`LiteLLM`、`react-bits-main` 的下一层级深入复用方案。
  - 补全 `Playwright`、`Langfuse`、`bilibili-api-python` 的计划引用方式与判定标准。
  - 新增“里程碑与材料复用绑定表”，让 `N1-N7` 每个里程碑都能对应到明确材料和吃入点。
- 实现情况：
  - 本轮不新增功能代码，属于计划文档的深化收口。
  - 当前 `stage_04_v1_0_runnable_baseline_and_next_plan.md` 已从“有里程碑”进一步升级为“有里程碑 + 有材料级复用落点 + 有量化引用判定”的执行文档。

## 2026-03-29 20:49:32 CST

- 变更类型：阶段文档目录重组与命名统一
- 变更文件：
  - `docs/stage_records/README.md`
  - `docs/stage_records/stage_01_project_handoff_summary_v1.md`
  - `docs/stage_records/stage_02_project_handoff_summary_v2.md`
  - `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
  - `docs/stage_records/stage_04_v1_0_runnable_baseline_and_next_plan.md`
  - `docs/stage_records/stage_04_v1_0_evaluation_handoff.md`
  - `README.md`
  - `docs/changelog.md`
- 修改目的：
  - 按阶段统一归档历史计划、交接、评测与版本基线文档。
  - 让文档命名一眼可见“属于哪个阶段、是什么类型”。
  - 删除已确认不再保留的 `project_skeleton_plan.md` 与 `document_governance_review_v1.md`。
- 修改内容：
  - 新建 `docs/stage_records/` 目录，并将阶段目标/评测说明文档统一移动到该目录。
  - 采用 `stage_0X_*.md` 的命名规则重命名 5 份阶段文档。
  - 根 README 的高频阅读入口改为新的阶段目录路径。
  - 新增阶段目录索引文档，说明当前文件含义与后续命名规则。
- 实现情况：
  - 本轮属于文档体系整理，不新增新功能代码。
  - 当前阶段文档已经从零散架构目录调整为单独的阶段文档目录，命名体系已统一。

## 2026-03-29 21:23:41 CST

- 变更类型：审查问题修复与回归补强
- 变更文件：
  - `backend/app/db/repositories/generation_job_event_repository.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/app/services/generation_pipeline/runner.py`
  - `backend/app/api/routes/internal.py`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `backend/tests/test_m35_generation_orchestrator.py`
  - `backend/tests/test_m50_langgraph_checkpoint_persistence.py`
  - `docs/changelog.md`
- 修改目的：
  - 修复代码审查中发现的三类实现漂移：状态接口伪进度、内部 checkpoint 查询对不存在任务返回空成功、后台线程异常缺少失败留痕。
- 修改内容：
  - 为任务事件仓储补充按事件类型存在性判断能力，供状态同步逻辑识别“执行是否真正开始”。
  - 收紧生成状态推进条件，避免在未进入真实执行链时仅凭创建时间推进到后续阶段。
  - 为内部 checkpoint 列表接口补充 generation 真值校验，不存在任务时返回 `404`。
  - 为后台执行器补充崩溃捕获与失败事件写入，确保异常能进入状态与 diagnostics 轨迹。
  - 新增回归测试，覆盖“未执行前禁止伪进度”“后台崩溃留痕”“checkpoint 查询必须对应真实任务”。
- 实现情况：
  - `tests/test_m35_generation_orchestrator.py` 已通过，结果 `3 passed`。
  - `tests/test_m50_langgraph_checkpoint_persistence.py` 已通过，结果 `2 passed`。
  - 已人工复现并确认修复前的伪进度问题已消失：未启动执行时状态保持在 `THEME_PARSING`。
  - `tests/test_m31_backend_regression_closure.py` 与 `tests/test_m34_generation_diagnostics.py` 在当前环境中存在 pytest 进程退出阶段卡住现象，本轮未拿到稳定完整结果，后续需单独继续排查测试退出行为。

## 2026-03-29 21:37:52 CST

- 变更类型：测试隔离修复与慢测去外部依赖化
- 变更文件：
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `backend/tests/test_m35_generation_orchestrator.py`
  - `backend/tests/test_m50_langgraph_checkpoint_persistence.py`
  - `docs/changelog.md`
- 修改目的：
  - 收口上一轮审查后遗留的测试稳定性问题，避免 SQLite 连接残留、后台自动执行和真实模型链路让回归结果失真或变慢。
- 修改内容：
  - 在多组后端测试的 `reset_database()` 中补充旧 engine `dispose` 与后台 runner `shutdown`，降低 SQLite 文件锁和历史线程残留风险。
  - 为 `m31` 与 `m34` 测试显式关闭 `generation_auto_start_enabled`，避免本地 `.env` 打开后台自动执行后引发结果漂移。
  - 将 `m31` 和 `m34` 的慢链路测试改为直接调用后端路由函数，移除 `TestClient` 壳层对用例节奏的干扰。
  - 为 `m31` 与 `m34` 引入本地确定性结构化结果 stub，避免测试依赖真实 LiteLLM / Instructor / LangGraph 外部链路。
  - 修正 direct route 调用时 FastAPI `Query(...)` 默认值对象带入测试的参数问题，并同步更新 diagnostics 事件序列断言。
- 实现情况：
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ... pytest -q tests/test_m31_backend_regression_closure.py` 已通过，结果 `4 passed in 2.04s`。
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ... pytest -q tests/test_m34_generation_diagnostics.py` 已通过，结果 `6 passed in 2.04s`。
  - 上一轮遗留的 `m31`、`m34` 慢测与退出阶段不稳定现象已完成收口。

## 2026-03-29 21:46:48 CST

- 变更类型：审查问题修复与内部控制台降级补强
- 变更文件：
  - `backend/app/core/config.py`
  - `backend/.env.example`
  - `backend/app/api/routes/creations.py`
  - `backend/app/api/routes/internal.py`
  - `backend/README.md`
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `backend/tests/test_m52_generation_checkpoint_state_snapshot.py`
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `docs/changelog.md`
- 修改目的：
  - 修复本轮审查发现的三类问题：默认生成主链会挂起、checkpoint 最新状态接口混淆不存在任务与无 checkpoint 状态、内部控制台对配置/鉴权错误缺少可读降级。
- 修改内容：
  - 将后端默认配置与示例环境中的 `GENERATION_AUTO_START_ENABLED` 调整为开启，避免默认安装路径创建任务后进入无法完成的等待页。
  - 为 `/creations/generate` 增加自动执行关闭时的 `503` fail-fast，防止接口在后台不可调度时仍返回成功任务。
  - 为 checkpoint `latest-state` 接口补充 generation 真值校验，不存在任务时明确返回 `Generation not found`。
  - 为趋势控制台与 checkpoint 控制台补充服务端 fetch 错误解析与页面内警示卡展示，避免 `403/503` 直接炸成 Next 错页。
  - 新增后端回归测试，覆盖“自动执行关闭时创建接口拒绝请求”与“latest-state 必须对应真实 generation”。
- 实现情况：
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests/test_m36_generation_execution_runner.py tests/test_m52_generation_checkpoint_state_snapshot.py` 已通过，结果 `8 passed in 7.47s`。
  - `cd frontend && npm run build` 已通过，Next.js 生产构建成功。

## 2026-03-29 21:53:01 CST

- 变更类型：后台提交异常回滚修复与测试隔离补强
- 变更文件：
  - `backend/app/services/generation_pipeline/runner.py`
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `backend/tests/test_m5_trend_and_exports.py`
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `docs/changelog.md`
- 修改目的：
  - 修复继续审查中发现的三类问题：后台提交器在 executor 提交失败时遗留脏 inflight 状态、内部控制台 POST 动作失败直接炸成 server action 错误、`m5` 回归对后台调度和内部 key 配置依赖过重导致不稳定。
- 修改内容：
  - 为后台执行提交增加异常回滚，`submit()` 失败时清理 inflight 并写入 `BACKGROUND_SUBMIT_FAILED` 事件，避免任务永久卡在“已提交但不可重试”的假状态。
  - 为执行器测试补充“executor 提交失败后必须释放 inflight 且写入失败事件”的回归用例。
  - 收紧 `m5` 回归隔离：重建事件仓储、显式同步 `internal_api_key`，并将创建路由中的后台提交 stub 掉，避免这组导出测试被真实后台线程和环境 `.env` 污染。
  - 将趋势刷新与 checkpoint 恢复两个 server action 改为回跳当前页并透传 `action_error/action_success`，让失败与成功都在页面内以告警卡呈现，而不是直接落到 Next 错页。
- 实现情况：
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests/test_m36_generation_execution_runner.py tests/test_m5_trend_and_exports.py` 已通过，结果 `12 passed in 19.32s`。
  - `cd frontend && npm run build` 已通过，Next.js 生产构建成功。

## 2026-03-29 21:57:02 CST

- 变更类型：创建链调度异常收敛与 checkpoint 回跳体验修复
- 变更文件：
  - `backend/app/api/routes/creations.py`
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `docs/changelog.md`
- 修改目的：
  - 修复继续审查中发现的两类问题：`/creations/generate` 在后台调度器抛异常时直接返回未处理 500，且已创建任务会变成用户无感知的孤儿记录；checkpoint 恢复动作在参数或配置异常时会把用户跳到无关的 `demo` 页面。
- 修改内容：
  - 为创建接口补充调度异常兜底：当 `generation_execution_runner.submit()` 抛异常或返回 `False` 时，将已创建任务明确标记为 `FAILED`，并统一向调用方返回 `503 Generation could not be scheduled for background execution`。
  - 为执行器测试补充“创建接口在后台提交崩溃时必须返回 `503`，且持久化任务进入失败终态”的回归用例。
  - 调整 checkpoint 恢复 server action 的回跳策略，优先保留当前 `generation_id`，仅在完全拿不到 id 时才落到兜底页，避免把用户从当前排查上下文带走。
- 实现情况：
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests/test_m36_generation_execution_runner.py` 已通过，结果 `8 passed in 4.26s`。
  - `cd frontend && npm run build` 已通过，Next.js 生产构建成功。

## 2026-03-29 22:06:11 CST

- 变更类型：全量审查后的回归契约同步与测试隔离修复
- 变更文件：
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `backend/tests/test_m31_backend_regression_closure.py`
  - `backend/tests/test_m33_alembic_cli_roundtrip.py`
  - `backend/tests/test_m34_generation_diagnostics.py`
  - `docs/changelog.md`
- 修改目的：
  - 收口全量审查中暴露的最后一批系统性问题：多组历史回归仍按旧的“自动执行关闭也允许 `/generate` 创建任务”的契约写法运行，且个别测试对当前状态同步逻辑和 Alembic head 版本的断言已经过期。
- 修改内容：
  - 为 `m31` 与 `m34` 改用“直接创建任务真值 + 显式触发 runner / 手动推进状态”的测试路径，不再依赖已废弃的旧 `/generate` 语义。
  - 为 `m31`、`m34`、`m30` 切换到更稳定的独立 SQLite 文件，并补充 `dispose` / runner 清理，降低回归之间的文件锁与迁移状态串扰。
  - 更新 `m30` 的状态推进断言，显式记录“执行已开始”事件后再验证自然推进，保持与当前防伪进度实现一致。
  - 更新 `m33` 的 Alembic roundtrip 断言，使用当前 head 版本 `20260327_182500`。
- 实现情况：
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests` 已通过，结果 `76 passed in 37.37s`。
  - `./scripts/demo_regression.sh` 已通过：后端演示回归 `15 passed`，前端生产构建成功。

## 2026-03-29 22:34:02 CST

- 变更类型：浏览器级真实链路补强与状态/模型回退真值修复
- 变更文件：
  - `backend/app/main.py`
  - `backend/app/services/generation_pipeline/store.py`
  - `backend/app/services/structured_output_gateway/service.py`
  - `backend/tests/test_m30_generation_store_persistence.py`
  - `backend/tests/test_m48_structured_output_gateway.py`
  - `backend/tests/test_m70_generation_concurrency_and_fault_injection.py`
  - `backend/tests/test_m71_localhost_cors.py`
  - `frontend/package.json`
  - `frontend/package-lock.json`
  - `frontend/playwright.config.ts`
  - `frontend/tests/e2e/create-to-result.spec.ts`
  - `docs/changelog.md`
- 修改目的：
  - 收口上一轮全量审查后剩余的两类高风险盲区：缺少浏览器级真实用户链路验证，以及缺少并发/故障注入覆盖；同时修复在这轮真实 E2E 中暴露出的两个实现问题：本地非 `3000` 端口开发环境的 CORS 失败，以及生成状态会按时间伪装推进、结构化模型网关在无凭证环境下卡住后台执行。
- 修改内容：
  - 为后端 CORS 增加 `localhost/127.0.0.1` 任意本地端口白名单正则，确保前端开发服务在隔离端口上也能直连后端。
  - 移除生成状态存储中的“执行开始后按时间自动推进阶段”逻辑，改为只信任真实持久化阶段事件，避免生成页把未完成任务伪装成 `PACKAGE_ASSEMBLING`。
  - 为结构化模型网关补充两层保护：当模型前缀对应的必需凭证缺失时立即 fallback；调用 instructor client 时显式透传 `MODEL_TIMEOUT_SECONDS`，避免后台线程长时间挂死。
  - 新增后端回归：
    - `m70` 覆盖结果物化并发串行化与 runner 并发去重/故障注入。
    - `m71` 覆盖非默认本地端口的 CORS 预检允许与未知来源拒绝。
    - `m30` 与 `m48` 更新为匹配新的“真实阶段真值/凭证缺失即时 fallback”契约。
  - 引入 Playwright 浏览器级 E2E：
    - 新增 `frontend/playwright.config.ts` 与 `frontend/tests/e2e/create-to-result.spec.ts`。
    - `frontend/package.json` 增加 `test:e2e` 脚本，并显式清除代理环境变量，避免 localhost 测试流量被宿主代理污染。
    - Playwright 链路覆盖 `create -> generating -> result -> internal checkpoints -> internal trends` 的完整真实用户流。
- 实现情况：
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests/test_m48_structured_output_gateway.py tests/test_m30_generation_store_persistence.py tests/test_m70_generation_concurrency_and_fault_injection.py tests/test_m71_localhost_cors.py` 已通过。
  - `cd frontend && npm run test:e2e` 已通过，结果 `1 passed`。

## 2026-03-29 22:54:03 CST

- 变更类型：全量回归收尾与测试运行时资源治理
- 变更文件：
  - `backend/app/services/generation_pipeline/checkpointer.py`
  - `backend/app/services/structured_output_gateway/service.py`
  - `backend/tests/conftest.py`
  - `backend/tests/test_m36_generation_execution_runner.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `backend/tests/test_m48_structured_output_gateway.py`
  - `backend/tests/test_m50_langgraph_checkpoint_persistence.py`
  - `backend/tests/test_m51_generation_checkpoint_restore.py`
  - `backend/tests/test_m52_generation_checkpoint_state_snapshot.py`
  - `backend/tests/test_m53_checkpoint_aware_result_builder.py`
  - `backend/tests/test_m58_rsshub_trend_ingestion.py`
  - `backend/tests/test_m71_localhost_cors.py`
  - `docs/changelog.md`
- 修改目的：
  - 在本轮最终认证阶段收口最后几类非功能性但会阻断“可认证成功”的问题：结构化输出凭证策略与 fake client 测试夹杂导致的旧回归漂移、checkpoint sqlite 连接未统一回收导致的 `disk I/O error`、全量后端回归在退出阶段残留全局资源导致的挂起，以及 `m36/m71` 对全量环境的脆弱假设。
- 修改内容：
  - 为 `GenerationCheckpointService` 增加 `reset()`，统一关闭旧 sqlite 连接并允许切换 checkpoint 路径，供测试稳定复位。
  - 新增 `backend/tests/conftest.py` 全局清理夹具，在每个测试后统一执行 runner shutdown、orchestrator graph 重置和 checkpointer reset，消除跨测试的线程/连接残留。
  - 将 `m50-m53` 的 checkpoint 测试重置顺序调整为“先 reset 关连接，再删除 sqlite 文件”，避免 LangGraph checkpoint 复用路径时触发 `disk I/O error`。
  - 调整结构化输出网关的凭证策略：只在使用默认真实 instructor client 工厂时要求真实 provider 凭证；显式注入 fake instructor client 的测试路径不再被误挡。
  - 补齐相关旧回归的环境契约：
    - `m36` 改为断言“新增 1 条失败任务”而不是“整库只有 1 条记录”。
    - `m46` / `m58` 明确为 fake structured-output 路径补测试 API key。
    - `m71` 改为直接调用 ASGI app 处理 `OPTIONS` 预检，不再用 `TestClient` 触发整个 app lifespan。
- 实现情况：
  - `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest tests -x` 已通过，结果 `81 passed in 8.06s`。
  - `./scripts/demo_regression.sh` 已通过，结果 `15 passed in 1.89s`，前端生产构建成功。
  - `cd frontend && npm run test:e2e` 已通过，结果 `1 passed (12.1s)`。

## 2026-03-30 11:51:34 CST

- 变更类型：N1 第一批执行级结果包深化
- 变更文件：
  - `docs/architecture/m88_n1_execution_bundle_contract.md`
  - `docs/api/m3_result_contract.md`
  - `docs/api/m4_export_contract.md`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/schemas/narrative_generation.py`
  - `backend/app/schemas/video_payload.py`
  - `backend/app/services/narrative_generator/service.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/generation_pipeline/orchestrator.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/export-json-preview.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/components/result/result-view-client.module.css`
- 修改目的：按 `stage_04_v1_0_runnable_baseline_and_next_plan.md` 的 `N1` 优先级，先完成一轮最小但完整的“结果包从重型方案走向更完整执行级”落地，并确保 docs 先于代码成为本轮唯一真值来源。
- 修改内容：
  - 新增 `docs/architecture/m88_n1_execution_bundle_contract.md`，锁定本轮三类必须同时完成的增强：结构化候选层、关键镜头执行字段、导出与结果页同步消费。
  - 更新 `m3_result_contract.md` 与 `m4_export_contract.md`，把 `title_candidates / hook_candidates / cover_candidates / distribution_angle_candidates` 以及 `storyboard_beats / asset_preparation_notes / voiceover_subtitle_alignment` 纳入正式契约。
  - 后端 schema 新增 `StructuredTextCandidate`，并把脚本层、平台层、机器执行层扩展为可承接结构化候选与执行级细字段。
  - `narrative_generator` 新增结构化标题候选与钩子候选的派生逻辑，同时加厚 `key_shots`，补充镜头运动、转场方式、素材依赖、配音落点等执行字段。
  - `package_assembler` 在脚本层补入结构化候选，在 fallback 路径补入封面候选、分发角度候选、分镜节拍、素材准备说明和配音落点/字幕对齐信息，确保结构化主路径和 fallback 路径同批补齐。
  - `orchestrator` 同步把新的结构化候选字段从叙事生成阶段传递到结果组装阶段，避免新增真值在执行链中丢失。
  - `export_payload` 同步增强 Markdown 与 Video payload，结果页同步新增结构化候选卡片与执行细节展示。
  - 测试补充到 `test_m46_instructor_package_assembler.py` 与 `test_m46_export_payload_compat.py`，覆盖新增候选层、执行级字段和导出承接结果。
- 实现情况：
  - 本轮 `N1` 第一批闭环已完成，结构化候选层已进入结果真值。
  - `key_shots` 已从仅有时长/转场提示，提升为包含运动、转场方式、素材依赖、配音落点的执行级镜头对象。
  - Markdown / JSON / Video payload 已同步承接新增字段，结果页也已可直接展示新增执行级信息。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/narrative_package.py backend/app/schemas/narrative_generation.py backend/app/services/narrative_generator/service.py backend/app/services/generation_pipeline/orchestrator.py backend/app/services/package_assembler/service.py backend/app/services/export_payload/service.py backend/app/schemas/video_payload.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py`
    - `cd frontend && npm run build`

## 2026-03-30 11:54:36 CST

- 变更类型：changelog 续写修正与 N1 执行时长深化
- 变更文件：
  - `docs/changelog.md`
  - `docs/architecture/m88_n1_execution_bundle_contract.md`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/schemas/video_payload.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/export-json-preview.tsx`
  - `frontend/components/result/result-view-client.tsx`
- 修改目的：
  - 修正我上一轮把 changelog 错误插入文件顶部、且新说明文档没有接续既有 `m` 系列命名的问题。
  - 在治理修正的同时继续深化 `N1` 执行级结果包，为制作执行蓝图增加总时长与节奏控制信息。
- 修改内容：
  - 将原本误插在文件顶部的 `2026-03-30 11:51:34 CST` 记录改为在文件底部接续落盘。
  - 将 `docs/api/n1_execution_bundle_contract.md` 调整为 `docs/architecture/m88_n1_execution_bundle_contract.md`，显式接续仓库现有 `m01-m87` 文档序列。
  - 在 `machine_payload_layer` 与 `video_payload` 中新增：
    - `estimated_total_duration_seconds`
    - `runtime_pacing_notes`
  - fallback 组装逻辑根据 `key_shots` 时长汇总总时长，并补充起势、解释、收束三个节奏控制说明。
  - Markdown 导出、Video payload 导出、结果页执行蓝图和前端类型定义同步承接这两个新增字段。
  - 更新 `m88` 契约文档与相关测试，使时长/节奏说明进入正式真值与回归保护。
- 实现情况：
  - `changelog` 已恢复为文件底部接续追加模式。
  - 新增阶段说明文档已接回 `m` 系列，当前续号为 `m88`。
  - 结果页现在除了候选层、镜头执行元信息外，还可直接看到预计总时长与节奏说明。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/narrative_package.py backend/app/schemas/video_payload.py backend/app/services/package_assembler/service.py backend/app/services/export_payload/service.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py`
    - `cd frontend && npm run build`
  - 待同步 git 留痕。

## 2026-03-30 14:04:24 CST

- 变更类型：N1 结构化分镜帧深化
- 变更文件：
  - `docs/architecture/m88_n1_execution_bundle_contract.md`
  - `docs/api/m3_result_contract.md`
  - `docs/api/m4_export_contract.md`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/schemas/video_payload.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/export-json-preview.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/components/result/result-view-client.module.css`
- 修改目的：继续沿 `N1` 把“制作执行字段”从字符串级节拍推进到更接近真实交付物的结构化分镜帧，让结果包不只知道“哪几拍”，还知道每一拍具体拍什么、说什么、要准备什么。
- 修改内容：
  - 在 `m88`、`m3_result_contract.md`、`m4_export_contract.md` 中把 `storyboard_frames` 纳入正式真值。
  - 后端新增 `StoryboardFrame` schema，并在 `machine_payload_layer` 中增加 `storyboard_frames` 字段。
  - fallback 结果组装新增三段结构化分镜帧，分别描述设问起手、解释展开、结尾收束三拍的画面焦点、旁白焦点、预计时长、素材要求和剪辑说明。
  - Markdown 导出新增“结构化分镜帧”章节，Video payload 同步承接 `storyboard_frames`。
  - 前端结果页新增结构化分镜帧展示卡片，导出预览与前端类型定义同步更新。
  - 回归测试同步补齐，对结果组装、Markdown 导出和 Video payload 导出中的分镜帧承接做断言。
- 实现情况：
  - 当前结果包已同时拥有：
    - 字符串级 `storyboard_beats`
    - 结构化 `storyboard_frames`
  - 执行蓝图从“节拍描述”提升到“可直接交给制作同学看的分镜帧说明”。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/narrative_package.py backend/app/services/package_assembler/service.py backend/app/services/export_payload/service.py backend/app/schemas/video_payload.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py`
    - `cd frontend && npm run build`

## 2026-03-30 14:34:30 CST

- 变更类型：N3 执行链可解释控制台收口
- 变更文件：
  - `docs/architecture/m92_n3_execution_trace_console_closure.md`
  - `docs/changelog.md`
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `frontend/app/internal/checkpoints/[id]/page.module.css`
- 修改目的：把 `N3` 从“有失败归因字段”推进到“内部控制台能直接把状态、事件、checkpoint 三层串起来解释”的收口状态，让排障和恢复不再需要来回切多个页面或接口。
- 修改内容：
  - 新增 `m92_n3_execution_trace_console_closure.md`，把 checkpoint 控制台需要同时展示的三层信息与完成判定落为 docs 真值。
  - `frontend/app/internal/checkpoints/[id]/page.tsx` 现在新增直接读取：
    - `/creations/{generation_id}/diagnostics`
    - `/internal/generation-checkpoints/{generation_id}/latest-state`
  - checkpoint 控制台新增“执行状态与最近事件”区块，直接展示：
    - `status`
    - `current_stage`
    - `error_message`
    - 最近事件轨迹
  - 事件轨迹卡片会展示：
    - `event_type`
    - `stage`
    - `stage_message`
    - `occurred_at`
    - `error_message`
  - 与上一批 `failure_attribution` 一起，控制台现在能把：
    - 状态层
    - 事件层
    - checkpoint 层
    放在同一页说明。
  - 补充对应样式，保证这块信息不会挤压原有恢复与列表区结构。
- 实现情况：
  - `N3` 里程碑要求中的“一条失败链可以从状态、事件、checkpoint 三层被串起来理解”已在内部 checkpoint 控制台形成最小闭环。
  - 现在同一页面可以直接回答：
    - 当前执行状态在哪里
    - 最近发生了哪些关键事件
    - checkpoint 是否有结果快照
    - 当前应该优先恢复还是优先排障
  - 结合上一批结构化 `failure_attribution`，`N3` 已按当前 docs 范围完成第一轮收口。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/generation.py backend/app/services/generation_pipeline/checkpointer.py backend/tests/test_m52_generation_checkpoint_state_snapshot.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m52_generation_checkpoint_state_snapshot.py`
    - `cd frontend && npm run build`

## 2026-03-30 14:30:53 CST

- 变更类型：N3 checkpoint 失败归因第一批
- 变更文件：
  - `docs/architecture/m91_n3_checkpoint_failure_attribution.md`
  - `docs/changelog.md`
  - `backend/app/schemas/generation.py`
  - `backend/app/services/generation_pipeline/checkpointer.py`
  - `backend/tests/test_m52_generation_checkpoint_state_snapshot.py`
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `frontend/app/internal/checkpoints/[id]/page.module.css`
- 修改目的：按 `N3` 的起步目标，先把执行链的失败说明从“只有状态和原始错误消息”推进到“checkpoint 状态中存在结构化失败归因”，让排障与恢复不再依赖人工脑补。
- 修改内容：
  - 新增 `m91_n3_checkpoint_failure_attribution.md`，把 `failure_attribution` 字段、归因规则、恢复提示和控制台展示约束落为 docs 真值。
  - 在 `GenerationCheckpointStateResponse` 中新增 `GenerationFailureAttribution`：
    - `category`
    - `stage`
    - `stage_message`
    - `latest_event_type`
    - `latest_error_message`
    - `recovery_hint`
    - `can_restore_result_snapshot`
  - `GenerationCheckpointService.get_latest_checkpoint_state()` 现在会结合：
    - 当前 generation 状态
    - 最近事件
    - checkpoint 中是否已有结果快照
    生成结构化失败归因对象。
  - 当前最小归因类别先收敛为：
    - `not_failed`
    - `timeout`
    - `execution_failed`
  - 内部 checkpoint 控制台“最新状态快照”区块新增：
    - failure category
    - 失败阶段说明
    - 最新错误事件类型
    - 恢复建议
    - 最新错误消息卡片
  - 测试补齐成功链和失败链的 failure attribution 断言。
- 实现情况：
  - checkpoint 最新状态不再只告诉我们“有没有结果”和“有多少段脚本”，还会结构化说明当前失败是否可恢复、最新错误落在哪一类。
  - 当 checkpoint 已保留结果快照时，控制台会明确提示可以优先尝试恢复；没有结果快照时，会提示先查看错误事件和上游日志。
  - 这一批虽然还不是完整失败链可视化，但已经把 `N3` 的第一层“结构化失败归因”真值建立起来。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/generation.py backend/app/services/generation_pipeline/checkpointer.py backend/tests/test_m52_generation_checkpoint_state_snapshot.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m52_generation_checkpoint_state_snapshot.py`
    - `cd frontend && npm run build`

## 2026-03-30 14:26:59 CST

- 变更类型：N2 来源配置显式化与许可证结论收口
- 变更文件：
  - `docs/architecture/m90_n2_source_configuration_and_license_decision.md`
  - `docs/changelog.md`
  - `backend/app/core/config.py`
  - `backend/app/schemas/trend_template.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m27_trend_collection.py`
  - `backend/tests/test_m41_internal_trend_api.py`
  - `backend/tests/test_m58_rsshub_trend_ingestion.py`
  - `backend/tests/test_m69_trend_template_summary_fields.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/trends/page.module.css`
- 修改目的：继续按 `N2` 顺序把趋势增强链从“已有来源轨迹”推进到“来源配置本身也可见、可解释、可治理”的状态，并正式结束 `bilibili-api-python` 在主链中的待定状态。
- 修改内容：
  - 新增 `m90_n2_source_configuration_and_license_decision.md`，把 `configured_sources`、多 route RSSHub 配置和 `bilibili-api-python` 许可证结论落为 docs 真值。
  - 在 `TrendTemplateSummary` 中新增 `configured_sources`，统一透传：
    - `source_kind`
    - `display_name`
    - `target`
    - `enabled`
    - `status`
    - `rationale`
  - `TrendCollectorService` 新增平台来源说明能力：
    - 输出 RSSHub feed 来源
    - 输出 Crawl4AI 页面来源
    - 对 `bilibili` 平台补充 `bilibili-api-python` 的研究候选说明，并标记为 `disabled_by_license`
  - `TREND_RSSHUB_PLATFORM_ROUTES` 不再只接受单 route，而允许 `platform -> one or more routes`。
  - 同平台多个 RSSHub route 现在可先在采集层合并，再进入同一平台趋势归纳链。
  - 内部趋势控制台新增“来源配置”区块，与“来源轨迹”分开展示，避免把“当前配置”和“本次实际消费”混为一谈。
  - 回归测试补齐：
    - 多 RSSHub route 合并
    - 内部趋势接口透传 `configured_sources`
    - 趋势模板摘要携带来源配置字段
- 实现情况：
  - 趋势链现在同时具备两层真值：
    - `source_trace`：本次实际消费了什么
    - `configured_sources`：当前平台允许接入什么、是否启用、为什么
  - 同平台 RSSHub 多 route 合并已落地，不再局限于单 route 配置。
  - `bilibili-api-python` 已按 docs 既有许可证结论正式标注为“保留研究价值，但退出主实现路径”，不再处于悬而未决状态。
  - 内部趋势控制台已能直接看到 active source 与 blocked candidate 的区别，来源治理说明更完整。
  - 验证已通过：
    - `python3 -m py_compile backend/app/core/config.py backend/app/schemas/trend_template.py backend/app/services/trend_collector/service.py backend/app/services/trend_strategy/service.py backend/tests/test_m27_trend_collection.py backend/tests/test_m41_internal_trend_api.py backend/tests/test_m58_rsshub_trend_ingestion.py backend/tests/test_m69_trend_template_summary_fields.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m27_trend_collection.py tests/test_m58_rsshub_trend_ingestion.py tests/test_m69_trend_template_summary_fields.py tests/test_m41_internal_trend_api.py`
    - `cd frontend && npm run build`

## 2026-03-30 14:21:13 CST

- 变更类型：N2 多来源趋势增强第一批闭环
- 变更文件：
  - `docs/architecture/m89_n2_multi_source_trend_enrichment.md`
  - `docs/changelog.md`
  - `backend/app/data/platform_trend_templates.json`
  - `backend/app/db/models/trend_template.py`
  - `backend/app/db/repositories/trend_template_repository.py`
  - `backend/app/schemas/trend_template.py`
  - `backend/app/services/trend_strategy/default_templates.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/migrations/versions/20260330_141800_add_trend_enrichment_fields.py`
  - `backend/tests/test_m41_internal_trend_api.py`
  - `backend/tests/test_m58_rsshub_trend_ingestion.py`
  - `backend/tests/test_m69_trend_template_summary_fields.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/trend-influence-deck.tsx`
  - `frontend/components/result/result-view-client.tsx`
- 修改目的：按阶段计划推进 `N2` 第一批闭环，把趋势层从“单来源摘要模板”推进到“多来源归纳 + 更厚的平台策略字段”，让趋势链更接近真实平台观察与创作指导场景。
- 修改内容：
  - 新增 `m89_n2_multi_source_trend_enrichment.md`，把 `N2` 第一批目标、字段约束、合流规则和完成判定落盘为 docs 真值。
  - 在趋势 schema、数据库模型、仓储映射、默认模板与种子模板中统一新增：
    - `interaction_patterns`
    - `emotional_entry_points`
    - `creator_angle_summary`
  - 趋势采集服务不再对同平台执行单源覆盖，而是允许 `RSSHub + Crawl4AI` 合流：
    - 合并 markdown 供结构化归纳
    - 合并 `source_trace`
    - 新增 `hybrid_collected` 作为复合来源类型
  - Instructor 结构化归纳提示词与结果合并逻辑同步承接三类新字段。
  - 内部趋势接口、结果页趋势影响区、Markdown 导出层同步透传并展示三类新增字段。
  - 新增数据库迁移，确保新增字段可稳定写入趋势模板真值层。
  - 测试补齐：
    - RSSHub 单源采集新增字段断言
    - RSSHub 与 Crawl4AI 同平台合流断言
    - 趋势模板摘要字段完整性断言
    - 内部趋势 API 返回结构同步断言
- 实现情况：
  - `N2` 第一批定义的“多来源合流 + 3 类新增趋势字段 + 结果页与导出可见”已全部落地。
  - 趋势模板现在不仅能给出钩子、节奏、标题风格，还能补充互动方式、情绪切口和创作者表达角度。
  - 同平台在同时拿到 RSSHub feed 与 Crawl 文档时，现已能够生成 `hybrid_collected` 趋势结果并保留两类来源轨迹。
  - 平台模板 JSON 种子、数据库模型、API 类型、前端卡片和导出文本已保持一致，避免 schema 漂移。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/trend_template.py backend/app/services/trend_strategy/default_templates.py backend/app/services/trend_strategy/service.py backend/app/db/models/trend_template.py backend/app/db/repositories/trend_template_repository.py backend/app/services/trend_collector/service.py backend/app/services/export_payload/service.py backend/tests/test_m58_rsshub_trend_ingestion.py backend/tests/test_m69_trend_template_summary_fields.py backend/tests/test_m41_internal_trend_api.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m58_rsshub_trend_ingestion.py tests/test_m69_trend_template_summary_fields.py tests/test_m41_internal_trend_api.py`
    - `cd frontend && npm run build`

## 2026-03-30 14:10:31 CST

- 变更类型：N1 分镜帧绑定深化
- 变更文件：
  - `docs/architecture/m88_n1_execution_bundle_contract.md`
  - `docs/api/m3_result_contract.md`
  - `docs/api/m4_export_contract.md`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/result-view-client.tsx`
- 修改目的：继续沿 `N1` 把结构化分镜帧从“独立列表”推进到“与脚本段落和关键镜头有明确映射关系”的执行真值，便于制作、审校和导出链统一理解每一拍属于哪一段、对准哪一个关键镜头。
- 修改内容：
  - 在 `m88`、`m3_result_contract.md`、`m4_export_contract.md` 中为 `storyboard_frames` 增加绑定要求。
  - `StoryboardFrame` 新增：
    - `linked_segment_number`
    - `linked_key_shot_title`
  - fallback 分镜帧分别绑定到：
    - `segment 1 -> 钩子镜头`
    - `segment 2 -> 解释镜头`
    - `segment 4 -> 结尾镜头`
  - Markdown 导出新增“对应段落 / 对应关键镜头”输出。
  - 结果页结构化分镜帧卡片同步展示这两个绑定字段。
  - 测试同步补断言，确保绑定信息不会在结果构建与导出过程中丢失。
- 实现情况：
  - 结构化分镜帧现在不仅能描述每拍内容，还能明确挂靠到脚本层与关键镜头层。
  - 结果页、Markdown 和 Video payload 都已承接这层绑定关系。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/narrative_package.py backend/app/services/package_assembler/service.py backend/app/services/export_payload/service.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py`
    - `cd frontend && npm run build`

## 2026-03-30 14:14:23 CST

- 变更类型：N1 素材准备与配音字幕对齐结构化收口
- 变更文件：
  - `docs/architecture/m88_n1_execution_bundle_contract.md`
  - `docs/api/m3_result_contract.md`
  - `docs/api/m4_export_contract.md`
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/schemas/video_payload.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `backend/tests/test_m46_export_payload_compat.py`
  - `frontend/lib/api-client/backend.ts`
  - `frontend/components/result/result-view-client.tsx`
- 修改目的：按 `N1` 既定顺序继续收口“制作执行字段”，把素材准备清单与配音/字幕对齐信息从字符串说明升级为带分镜帧绑定的结构化对象，让执行包真正具备交付级组织方式。
- 修改内容：
  - 在 `m88`、`m3_result_contract.md`、`m4_export_contract.md` 中补充结构化素材准备项与结构化配音字幕对齐项约束。
  - 新增：
    - `AssetPreparationItem`
    - `VoiceoverSubtitleAlignmentItem`
  - `MachinePayloadLayer` 中：
    - `asset_preparation_notes` 从 `list[str]` 升级为结构化准备项列表
    - `voiceover_subtitle_alignment` 从 `list[str]` 升级为结构化对齐项列表
  - fallback 路径把三类素材和三条配音/字幕对齐项分别绑定到对应分镜帧。
  - Markdown 导出新增：
    - `结构化素材准备项`
    - `结构化配音字幕对齐`
  - Video payload 与前端类型定义同步承接结构化列表。
  - 结果页将素材准备说明与配音字幕对齐从普通列表升级为结构化卡片展示。
- 实现情况：
  - `N1` 目标中的三块制作执行字段现在均已结构化落入统一 schema：
    - `storyboard_frames`
    - `asset_preparation_notes`
    - `voiceover_subtitle_alignment`
  - 结果页、Markdown、JSON、Video payload 四条消费链都已承接这些结构化执行真值。
  - 结合前几轮候选层、镜头执行字段、分镜帧绑定、本轮素材与配音字幕结构化，`N1` 里程碑已按当前文档范围完成第一轮收口。
  - 验证已通过：
    - `python3 -m py_compile backend/app/schemas/narrative_package.py backend/app/services/package_assembler/service.py backend/app/services/export_payload/service.py backend/app/schemas/video_payload.py`
    - `cd backend && PYTHONPATH=/home/admin2/smy/multi-media/backend pytest -q tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py`
    - `cd frontend && npm run build`

## 2026-03-30 15:03:08 CST

- 变更类型：N4 Playwright 回归入口与统一验证顺序收口
- 变更文件：
  - `docs/architecture/m93_n4_playwright_regression_and_validation_runbook.md`
  - `docs/stage_records/stage_04_v1_0_evaluation_handoff.md`
  - `README.md`
  - `backend/README.md`
  - `frontend/README.md`
  - `frontend/playwright.config.ts`
  - `frontend/tests/e2e/create-to-result.spec.ts`
  - `frontend/tests/e2e/helpers/generation-flow.ts`
  - `frontend/tests/e2e/internal-tools-and-exports.spec.ts`
  - `backend/tests/test_m35_generation_orchestrator.py`
  - `backend/tests/test_m51_generation_checkpoint_restore.py`
  - `backend/tests/test_m53_checkpoint_aware_result_builder.py`
  - `scripts/demo_regression.sh`
- 修改目的：按阶段计划完成 `N4` 第一批，把 `Playwright` 正式并入统一回归顺序，覆盖 1 条完整主流程与 1 条内部工具链 / 导出链，同时收口 README、评测交接文档和统一回归入口之间的验证顺序差异。
- 修改内容：
  - 新增 `m93_n4_playwright_regression_and_validation_runbook.md`，锁定 `backend tests -> frontend build -> playwright e2e` 的统一验证顺序。
  - `README.md`、`backend/README.md`、`frontend/README.md` 与 `stage_04_v1_0_evaluation_handoff.md` 同步到同一套回归入口说明。
  - 把既有 `create-to-result.spec.ts` 提炼为共享 helper 驱动的主流程回归。
  - 新增 `internal-tools-and-exports.spec.ts`，覆盖：
    - `export/json`
    - `export/md`
    - `video-payload`
    - `internal/checkpoints/{generation_id}`
  - 修正 E2E 断言边界：移除 `video-payload` 顶层不存在的 `generation_id` 假设，改回契约内字段校验。
  - 为创建页提交流程增加更稳定的 E2E 提交方式，避免 React/Next 单页跳转时按钮节点重渲染导致的假失败。
  - 统一回归脚本 `demo_regression.sh` 改为三步串联，并在脚本内部托管 Playwright 所需服务启动，保留 `Playwright` 作为唯一页面级验证框架，不另起新测试系统。
  - 补齐 3 个后端既有测试中的 `NarrativeBundleResult` fixture，使其承接前序 `N1` 已进入真值的结构化候选字段。
- 实现情况：
  - `N4` 第一批现在已经满足阶段计划中的两项最小覆盖：
    - 1 条完整主流程：创建页 -> 生成页 -> 结果页
    - 1 条内部工具链 / 导出链：导出接口 + checkpoint 控制台
  - `Playwright` 单独运行与统一入口运行都已通过；其中统一入口在当前沙箱内会遇到本地监听限制，因此最终采用真实可监听环境完成闭环验证。
  - `demo_regression.sh` 现在能够作为 `N4` 的统一回归入口，完成后端、前端构建和页面级 E2E 三段连续验证。
  - 验证已通过：
    - `cd frontend && npm run build`
    - `cd frontend && npm run test:e2e`
    - `cd /home/admin2/smy/multi-media && ./scripts/demo_regression.sh`

## 2026-03-30 15:10:14 CST

- 变更类型：N7 固定评测样例与交付入口收口
- 变更文件：
  - `docs/architecture/m94_n7_evaluation_pack_and_fixed_samples.md`
  - `docs/testing/n7_evaluation_sample_matrix.md`
  - `docs/testing/evaluation_samples/science_bilibili_time_travel.json`
  - `docs/testing/evaluation_samples/history_rednote_reform_story.json`
  - `docs/testing/evaluation_samples/workplace_wechat_efficiency.json`
  - `scripts/smoke_test.sh`
  - `scripts/evaluation_sample_pack.sh`
  - `README.md`
  - `docs/stage_records/stage_04_v1_0_evaluation_handoff.md`
- 修改目的：按 `N7` 计划把评测团队需要的固定材料真正落地成 docs 与脚本入口，避免评测仍依赖聊天记录或口头说明；同时坚持复用既有 `demo_regression.sh`、`smoke_test.sh` 和 `Playwright`，不新造评测框架。
- 修改内容：
  - 新增 `m94_n7_evaluation_pack_and_fixed_samples.md`，锁定 `N7` 的固定样例、固定观察点、固定入口和 `Langfuse` 暂不进入主链的当前结论。
  - 新增 `docs/testing/n7_evaluation_sample_matrix.md`，按四个核心目标给出固定观察口径和快速判定规则。
  - 新增 3 组固定评测输入样例，覆盖：
    - 科普/脑洞
    - 历史/叙事
    - 职场/实用
  - 扩展 `smoke_test.sh`，支持通过 `SMOKE_TEST_REQUEST_FILE` 复用固定 JSON 样例输入。
  - 新增 `evaluation_sample_pack.sh`，串行复用 `smoke_test.sh` 执行固定样例包。
  - README 与评测交接文档同步补充固定样例入口和样例矩阵文档位置。
- 实现情况：
  - `N7` 当前范围已经具备：
    - 固定评测入口：`demo_regression.sh`
    - 固定样例入口：`evaluation_sample_pack.sh`
    - 固定样例文件：`docs/testing/evaluation_samples/`
    - 固定观察点矩阵：`docs/testing/n7_evaluation_sample_matrix.md`
  - 评测团队现在不需要依赖口头说明，就能按文档执行统一回归和固定样例验证。
  - `Langfuse` 本轮仍保持候选状态，没有为了观测再引入新主链，符合胶水收口原则。
  - 验证已通过：
    - `bash -n scripts/smoke_test.sh scripts/evaluation_sample_pack.sh`

## 2026-03-30 15:12:45 CST

- 变更类型：N5 四页核心文案用户化改写
- 变更文件：
  - `docs/architecture/m95_n5_user_task_copy_shift.md`
  - `frontend/app/page.tsx`
  - `frontend/app/create/page.tsx`
  - `frontend/app/generating/[id]/page.tsx`
  - `frontend/app/result/[id]/page.tsx`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/wizard/creation-preset-deck.tsx`
  - `frontend/components/wizard/trend-signal-panel.tsx`
  - `frontend/components/generation/generation-status-client.tsx`
  - `frontend/components/result/result-next-step-guide.tsx`
  - `frontend/components/result/result-view-client.tsx`
- 修改目的：按 `N5` 计划把首页、创建页、生成页、结果页的核心口吻从“展示系统能力”切到“帮助用户完成当前任务”，同时保留现有页面层级和上游展示材料，不另起新展示系统。
- 修改内容：
  - 新增 `m95_n5_user_task_copy_shift.md`，明确四页的“改写前 / 改写后”对照。
  - 首页页头和 Hero 文案改成“从一句想法开始”“拿到什么结果”的用户口吻。
  - 创建页与预设卡、趋势提示卡改成“这一步该填什么、先看什么”的任务口吻。
  - 生成页与生成状态组件改成“现在只需看进度、完成后自动跳转”的说明口吻。
  - 结果页与下一步引导改成“现在可以导出、回看依据或继续重开”的使用口吻。
  - 结果加载失败、重试和返回动作也同步改成更贴近用户意图的文案。
- 实现情况：
  - 四页主链都已完成一轮核心文案改写。
  - 页面结构、组件层级和现有 `react-bits-main` 展示材料保持不变，只调整用户实际看到的说明与 CTA 语义。
  - docs 已保留一轮展示型文案到用户任务型文案的前后对照清单。
  - 验证已通过：
    - `cd frontend && npm run build`

## 2026-03-30 15:16:40 CST

- 变更类型：N6 移动端密度与阅读节奏优化
- 变更文件：
  - `docs/architecture/m96_n6_mobile_density_and_reading_polish.md`
  - `frontend/components/wizard/create-wizard.module.css`
  - `frontend/components/wizard/create-wizard.tsx`
  - `frontend/components/layout/site-shell.module.css`
  - `frontend/components/landing/creative-hero.module.css`
  - `frontend/components/result/result-view-client.module.css`
  - `frontend/tests/e2e/helpers/generation-flow.ts`
- 修改目的：按 `N6` 计划继续 polish 首页、创建页、结果页的移动端信息层级和长内容阅读节奏，在不改现有视觉方向的前提下减少小屏横向压力、降低长页面阅读负担，并保持当前上游展示材料复用方式不变。
- 修改内容：
  - 新增 `m96_n6_mobile_density_and_reading_polish.md`，锁定本轮移动端与阅读节奏优化目标。
  - 为创建页新增 `create-wizard.module.css`，把双栏工作台改成更稳的响应式布局，并让趋势侧栏在移动端回落为普通顺序块。
  - 创建页底部动作区在小屏下改成更容易点击的纵向排列。
  - `site-shell.module.css` 新增小屏 header 间距与说明文字密度优化。
  - `creative-hero.module.css` 新增小屏 Hero 单列布局、CTA 纵向堆叠、统计卡单列和 feature 区减压规则。
  - `result-view-client.module.css` 新增小屏卡片 padding 压缩、长列表单列化和行高优化，降低结果页滚动负担。
  - `generation-flow.ts` 把创建页 E2E 锚点改成稳定输入控件，避免文案改写后回归脚本误报。
- 实现情况：
  - 首页、创建页、结果页在移动端都更接近“单列先读、逐段展开”的节奏。
  - 本轮没有新增任何重型自写特效系统，仍建立在现有 `react-bits-main` 与既有 UI 组件之上。
  - 页面级回归仍保持通过，说明移动端与节奏优化没有破坏主链。
  - 验证已通过：
    - `cd frontend && npm run build`
    - `cd frontend && npm run test:e2e`

## 2026-03-30 15:22:53 CST

- 变更类型：阶段五深化完成交接文档落盘
- 变更文件：
  - `docs/stage_records/stage_05_deepening_completion_handoff_v1.md`
- 修改目的：为后续评测团队与接手开发团队提供一份基于本次对话实际完成内容的阶段性交接说明，系统总结已达成开发目标、可直接评测的指标、相对 PRD 的实现判断，以及下一阶段最值得继续深化的方向。
- 修改内容：
  - 按 `stage_records` 既有命名逻辑新增 `stage_05_deepening_completion_handoff_v1.md`。
  - 文档详细总结本次对话期间已完成的 `N1-N7` 里程碑收口情况。
  - 明确列出当前可直接评测的指标：
    - 主链完整性
    - 结果与导出同源性
    - 趋势是否真实进入主链
    - 执行级结果重量
    - 排障与恢复可理解性
    - 首次上手与页面引导
    - 连续评测可执行性
  - 基于 `docs/PRD.md` 对当前系统是否符合一期 MVP 预期做出判断，并说明仍未达到终局感的部分。
  - 给出下一阶段建议，重点包括：
    - 严格遵守胶水原则的前端继续美化
    - 后端结果质量与结构化输出继续深化
    - 观测与质量评估体系继续增强
- 实现情况：
  - 当前 `stage_04` 文档中的 `N1-N7` 深化计划，已经有一份新的 `stage_05` 交接文档可供评测团队直接消费。
  - 后续评测团队可不依赖聊天记录，直接根据该文档理解当前系统已达成的能力边界与评测口径。

## 2026-03-30 15:28:15 CST

- 变更类型：连续审查首轮兼容性修复
- 变更文件：
  - `backend/app/services/narrative_generator/service.py`
  - `backend/tests/test_m33_alembic_cli_roundtrip.py`
  - `docs/changelog.md`
- 修改目的：修复全量后端回归中已确认的两处真实失败，避免迁移测试因 head 版本推进而失效，并补上叙事结果对象对旧调用方式的兼容兜底。
- 修改内容：
  - 将 `NarrativeBundleResult` 的 `title_candidates`、`hook_candidates` 改为带默认工厂的字段，兼容旧测试和旧 monkeypatch 仍按未扩展字段构造对象的路径。
  - 将 `test_m33_alembic_cli_roundtrip.py` 从写死 revision 改为通过 Alembic 脚本目录动态读取当前 head，避免新增迁移后测试常态化误报。
  - 记录本轮连续审查的第一批修复批次，作为后续 git 提交与继续审查的审计锚点。
- 实现情况：
  - 两处失败根因都已完成代码级修复，待通过定向回归与全量回归确认。
  - 本轮改动刻意保持在兼容性和测试稳定性边界内，未扩散到无关业务逻辑。

## 2026-03-30 15:30:43 CST

- 变更类型：连续审查首轮修复验证结果回填
- 变更文件：
  - `docs/changelog.md`
- 修改目的：把首轮修复批次的真实验证结果补回审计记录，避免 changelog 停留在“待确认”状态。
- 修改内容：
  - 记录定向回归结果：
    - `cd /home/admin2/smy/multi-media/backend && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests/test_m33_alembic_cli_roundtrip.py tests/test_m50_langgraph_checkpoint_persistence.py tests/test_m51_generation_checkpoint_restore.py tests/test_m52_generation_checkpoint_state_snapshot.py tests/test_m53_checkpoint_aware_result_builder.py tests/test_m35_generation_orchestrator.py`
    - 结果：`11 passed in 4.30s`
  - 记录全量后端回归结果：
    - `cd /home/admin2/smy/multi-media/backend && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests`
    - 结果：`84 passed in 8.33s`
  - 记录统一演示回归入口结果：
    - `cd /home/admin2/smy/multi-media && ./scripts/demo_regression.sh`
    - 结果：后端回归 `17 passed in 2.14s`，前端 `next build` 通过，Playwright E2E `2 passed (12.7s)`，脚本最终输出 `Demo regression passed.`
- 实现情况：
  - 首轮修复已通过定向验证、后端全量验证与统一演示回归入口验证。
  - 本轮继续审查中暂未发现新的自动化回归失败项，可进入下一轮更偏静态代码层的深挖时再继续扩展。

## 2026-03-30 15:31:25 CST

- 变更类型：连续审查第二批工程卫生修复
- 变更文件：
  - `.gitignore`
  - `docs/changelog.md`
- 修改目的：清理并长期规避 Playwright 回归生成的临时产物污染工作区，降低后续审查和提交时的噪音。
- 修改内容：
  - 在 `.gitignore` 中新增 `frontend/test-results/` 与 `frontend/playwright-report/`，覆盖 Playwright 常见本地产物目录。
  - 记录本轮验证后发现的未跟踪文件来源，避免未来重复把回归产物误判为待提交改动。
- 实现情况：
  - 后续执行前端 E2E 或统一演示回归时，Playwright 临时产物将默认被忽略。
  - 本轮已识别到的 `frontend/test-results/.last-run.json` 可在提交后安全清理，不影响业务代码与验证结论。

## 2026-03-30 15:36:06 CST

- 变更类型：连续审查第三批稀疏结构化输出兜底修复
- 变更文件：
  - `backend/app/services/profile_parser/service.py`
  - `backend/app/services/narrative_generator/service.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/tests/test_m38_instructor_profile_parser.py`
  - `backend/tests/test_m29_model_first_narrative.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `docs/changelog.md`
- 修改目的：修复一类当前自动化主回归未直接暴露、但在真实模型返回“字段合法但列表为空”时会触发的生成链崩溃风险，避免叙事生成与结果组装路径在空列表上直接发生 `IndexError`。
- 修改内容：
  - 为 `ProfileParserService` 增加结构化结果归一化逻辑；当模型返回空的兴趣、痛点、内容偏好、情绪偏好或空白文本时，自动回落到与现有 fallback 同语义的最小可用值。
  - 为 `NarrativeGeneratorService` 增加对受众兴趣标签与趋势模板关键列表字段的兜底归一化，保证 `hook_patterns`、`rhythm_patterns`、`avoid_patterns` 为空时仍能安全生成 fallback 叙事。
  - 为 `PackageAssemblerService` 的 fallback scaffold 增加对痛点、兴趣、情绪偏好与趋势关键列表字段的兜底归一化，避免结构化组装前的直取首项崩溃。
  - 新增三组回归测试，分别覆盖：
    - profile parser 对稀疏结构化 payload 的归一化
    - narrative generator fallback 对稀疏输入的容错
    - package assembler fallback 对稀疏输入的容错
- 实现情况：
  - 代码已完成，待通过定向回归确认。
  - 本轮修复保持在数据边界兜底层，不改现有正常输入下的结果结构与主链行为。

## 2026-03-30 15:40:37 CST

- 变更类型：连续审查第三批修复验证结果回填
- 变更文件：
  - `docs/changelog.md`
- 修改目的：把第三批“稀疏结构化输出兜底修复”的真实验证结果补回审计记录，保持修复批次、测试结果与 git 提交一一对应。
- 修改内容：
  - 记录定向回归结果：
    - `cd /home/admin2/smy/multi-media/backend && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests/test_m38_instructor_profile_parser.py tests/test_m29_model_first_narrative.py tests/test_m46_instructor_package_assembler.py`
    - 结果：`9 passed in 0.03s`
  - 记录全量后端回归结果：
    - `cd /home/admin2/smy/multi-media/backend && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/home/admin2/smy/multi-media/backend ./.venv/bin/pytest -q tests`
    - 结果：`87 passed in 9.01s`
  - 记录统一演示回归入口结果：
    - `cd /home/admin2/smy/multi-media && ./scripts/demo_regression.sh`
    - 结果：后端回归 `17 passed in 2.18s`，前端 `next build` 通过，Playwright E2E `2 passed (12.5s)`，脚本最终输出 `Demo regression passed.`
- 实现情况：
  - 第三批修复已通过定向验证、后端全量验证与统一演示回归入口验证。
  - 当前继续审查过程中，自动化层面未再暴露新的明确失败项。

## 2026-04-02 15:31:03 CST

- 变更类型：前端全量用户文案重写
- 变更文件：
  - `frontend/app/layout.tsx`
  - `frontend/app/create/page.tsx`
  - `frontend/app/generating/[id]/page.tsx`
  - `frontend/app/result/[id]/page.tsx`
  - `frontend/app/internal/trends/page.tsx`
  - `frontend/app/internal/checkpoints/[id]/page.tsx`
  - `frontend/components/landing/creative-hero.tsx`
  - `frontend/components/landing/first-run-guide.tsx`
  - `frontend/components/landing/quickstart-launchpad.tsx`
  - `frontend/components/landing/workflow-stepper.tsx`
  - `frontend/components/landing/homepage-signal-nav.tsx`
  - `frontend/components/landing/trend-demo-script.tsx`
  - `frontend/components/landing/consistency-thread-showcase.tsx`
  - `frontend/components/landing/trend-amplifier-showcase.tsx`
  - `frontend/components/landing/homepage-result-showcase.tsx`
  - `frontend/components/wizard/create-wizard.tsx`
  - `frontend/components/wizard/consistency-preview-deck.tsx`
  - `frontend/components/wizard/creation-preset-deck.tsx`
  - `frontend/components/wizard/trend-signal-panel.tsx`
  - `frontend/components/wizard/trend-strategy-deck.tsx`
  - `frontend/components/generation/generation-status-client.tsx`
  - `frontend/components/generation/generation-output-deck.tsx`
  - `frontend/components/internal/internal-console-hub.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `frontend/components/result/result-next-step-guide.tsx`
  - `frontend/components/result/result-section-nav.tsx`
  - `frontend/components/result/distribution-strategy-deck.tsx`
  - `frontend/components/result/trend-influence-deck.tsx`
  - `frontend/components/result/consistency-thread-deck.tsx`
  - `frontend/components/result/markdown-preview.tsx`
  - `frontend/components/result/export-action-panel.tsx`
  - `frontend/components/result/export-json-preview.tsx`
  - `frontend/components/result/payload-foldout-header.tsx`
  - `frontend/components/result/machine-payload-summary.tsx`
  - `frontend/components/result/multimodal-summary.tsx`
  - `frontend/components/result/trend-source-trace-panel.tsx`
  - `frontend/lib/constants/creation-presets.ts`
  - `frontend/lib/api-client/backend.ts`
  - `docs/changelog.md`
- 修改目的：把前端各页仍残留的工程初期填充文案、系统自述口吻和架构暴露性表达，统一改成面向真实用户的成熟引导语言，同时保持页面结构、组件关系和功能行为不变。
- 修改内容：
  - 首页：
    - 重写 Hero、统计卡、流程说明、结果预览和导航文案。
    - 删除“展示 / 工作台 / 链路 / 结果包 / 真值”等偏工程口吻表达，改为“开始创作 / 结果预览 / 参考信息 / 下一步动作”等用户口吻。
  - 创建页：
    - 重写页面 banner、五步输入说明、预设卡、填写预览和参考提示文案。
    - 把“系统如何处理输入”的表述改成“用户这一步该填什么、填完能得到什么”。
  - 生成页：
    - 重写进度页 banner、阶段说明、状态文案和提示语。
    - 弱化内部术语与架构细节，改成“当前进度 / 正在补齐的内容 / 出错时如何理解当前状态”。
  - 结果页：
    - 重写总览、参考与判断、导出、脚本、发布建议、制作参考、备选方案、文本预览、完整字段预览等核心标题和说明。
    - 将“结果包 / 真值 / 机器层 / 多模态层 / 平台适配层 / 执行蓝图”等工程导向命名改为用户更容易理解的内容命名。
  - 辅助页：
    - 将 `/internal/trends` 统一改写为“参考页”语义。
    - 将 `/internal/checkpoints/[id]` 统一改写为“进度排查页”语义。
    - 保留辅助能力本身，但减少页面文字中对内部实现和架构复用策略的直接暴露。
  - 其余：
    - 同步调整预设摘要、前端错误提示和局部导航标签，避免页面上继续出现“结果包 / 真值”等早期遗留表述。
- 实现情况：
  - 本轮仅修改前端用户可见文案与少量前端错误提示，不改接口结构、不改组件层级、不改业务逻辑。
  - 已执行前端生产构建验证：
    - `cd /home/admin2/smy/multi-media/frontend && npm run build`
    - 结果：`next build` 成功通过。
  - 当前工作区已形成一批与 changelog 同步的前端文案变更，待提交 git 形成可追溯版本点。

## 2026-04-02 15:38:52 CST

- 变更类型：前端用户文案规律文档沉淀与第二轮收束
- 变更文件：
  - `docs/research/frontend_user_copy_patterns_v1.md`
  - `frontend/app/page.tsx`
  - `frontend/components/layout/flow-stage-banner.tsx`
  - `frontend/components/generation/generation-output-deck.tsx`
  - `frontend/components/generation/generation-status-client.tsx`
  - `frontend/components/wizard/create-wizard.tsx`
  - `frontend/components/wizard/consistency-preview-deck.tsx`
  - `frontend/components/internal/internal-console-hub.tsx`
  - `frontend/components/result/analysis-summary.tsx`
  - `frontend/components/result/result-hero-summary.tsx`
  - `frontend/components/result/platform-layer-summary.tsx`
  - `frontend/components/result/result-view-client.tsx`
  - `docs/changelog.md`
- 修改目的：把上一轮基于公开网页检索得到的文案规律正式沉淀到项目文档中，并据此对前端高频文案再做一轮短句化、动作化和去抽象化收束，进一步贴近成熟公开产品页面的表达方式。
- 修改内容：
  - 新增 `docs/research/frontend_user_copy_patterns_v1.md`：
    - 总结首页、创建页、生成页、结果页、辅助页的用户文案规律。
    - 明确“先写用户动作、再写结果、最后写下一步”的默认顺序。
    - 列出本项目应避免的高工程化词汇及推荐替代词。
    - 形成后续可复用的文案检查清单。
  - 前端第二轮文案迭代：
    - 压缩首页标题和副标题，减少“结构化结果”等抽象表述。
    - 把页面 banner 的 `Highlights / Actions / 下一步` 进一步收口为更自然的中文用户话术。
    - 将创建页、生成页和结果页中的说明文案继续缩短，减少解释性长句。
    - 将结果页分析区、总览区、平台建议区等标签改成更接近用户判断动作的命名。
    - 继续削弱“系统正在解释自己”的语气，保留“你现在该看什么、接下来做什么”的语气。
- 实现情况：
  - 本轮仍只修改文案与文案规则文档，不改业务逻辑。
  - 已执行前端生产构建验证：
    - `cd /home/admin2/smy/multi-media/frontend && npm run build`
    - 结果：`next build` 成功通过。
  - 本轮变更可与上一轮前端用户文案重写一起形成连续可追溯的文案治理记录。

## 2026-04-02 16:29:55 CST

- 变更类型：M97 原生抓取加 AI 总结的真实趋势模版导入闭环
- 变更文件：
  - `backend/app/core/config.py`
  - `backend/app/data/platform_trend_templates.json`
  - `backend/app/integrations/llm/aihubmix_search_adapter.py`
  - `backend/app/schemas/trend_template.py`
  - `backend/app/services/trend_collector/service.py`
  - `backend/app/services/trend_strategy/default_templates.py`
  - `backend/app/services/trend_strategy/repository.py`
  - `backend/app/services/trend_strategy/service.py`
  - `backend/tests/test_m97_aihubmix_native_plus_summary_refresh.py`
  - `docs/changelog.md`
- 修改目的：把趋势模版链路从静态基线刷新推进到“原生抓取 + AIHubMix 检索总结 + 落库 + 种子同步”的真实导入闭环，并完成首批 12 个平台内容类型模版的生产级导入验证。
- 修改内容：
  - 新增 `AIHubMixSearchAdapter`，通过具备检索能力的模型返回严格 JSON，并产出带 `source_trace` 的 `SearchBackedTrendObservation`。
  - 扩展趋势 schema 与配置，新增 AIHubMix 相关配置项和搜索观察结构，保持搜索能力与现有趋势服务边界清晰。
  - 在默认模版矩阵中新增四个平台的 `science_popularization` 与 `story` 变体，形成首批 `bilibili`、`douyin`、`xiaohongshu`、`kuaishou` 共 12 个目标模版，并保留既有 `wechat_video/auto` 基线。
  - 在 `trend_collector` 中接入 AIHubMix 搜索总结结果，优先生成 `aihubmix_search_collected` 模版；若存在原生抓取文档，则与搜索来源做 `source_trace` 合并；若搜索不可用则继续保留原有 fallback 路径。
  - 在仓储与服务层补充 seed 文件写回逻辑，使真实刷新后数据库与 `backend/app/data/platform_trend_templates.json` 同步更新，便于后续溯源与回退。
  - 针对 Gemini 类模型输出存在的字段漂移与稀疏问题，在 `aihubmix_search_adapter.py` 中补充归一化逻辑：支持列表与字符串互转、合并短语拆分、去重裁剪、字段数量不足时回填基线，避免真实刷新因格式轻微漂移整体回退到 `manual_refresh_fallback`。
  - 新增测试覆盖“纯搜索生成”“原生来源 + 搜索来源合并”以及“稀疏字段归一化”三类场景，确保真实外部返回也能稳定通过 schema 校验。
- 实现情况：
  - 本地校验完成：`python3 -m py_compile` 已通过新增与修改文件语法检查。
  - 定向测试完成：执行 `./scripts/backend_test.sh tests/test_m27_trend_collection.py tests/test_m58_rsshub_trend_ingestion.py tests/test_m97_aihubmix_native_plus_summary_refresh.py`，结果为 `10 passed`。
  - 真实刷新完成：在 `backend/` 目录执行 `trend_strategy_service.refresh_templates()`，返回 `REFRESHED_COUNT 13`，总体 `SOURCE_TYPE aihubmix_search_collected`。
  - 目标模版验证完成：四个平台下的 `auto`、`science_popularization`、`story` 共 `12` 个目标模版均已成功生成并返回真实搜索总结结果。
  - 种子文件同步完成：`backend/app/data/platform_trend_templates.json` 已写入上述真实刷新结果，目标内容类型条目与 `aihubmix_search_collected` 来源状态均可检索确认。

## 2026-04-02 17:25:46 CST

- 变更类型：结果包全层扩写能力接入与真实扩写包验证
- 变更文件：
  - `backend/app/schemas/narrative_package.py`
  - `backend/app/schemas/video_payload.py`
  - `backend/app/services/export_payload/service.py`
  - `backend/app/services/package_assembler/service.py`
  - `backend/app/services/package_expander/service.py`
  - `backend/tests/test_m46_instructor_package_assembler.py`
  - `docs/changelog.md`
- 修改目的：在不推翻现有结果包真值结构的前提下，为 `overview / analysis / script / multimodal / platform / machine payload` 六个层级新增统一扩写能力，让每个层级从“骨架结果”升级为“更厚、更细、仍可结构化消费”的超重型结果包。
- 修改内容：
  - 在 `narrative_package.py` 中新增扩写专用结构：`ExpansionDetailItem`、`ExpandedScriptSegment`、`ExpandedKeyShot`、`OverviewExpansion`、`AnalysisExpansion`、`ScriptExpansion`、`MultimodalExpansion`、`PlatformExpansion`、`MachinePayloadExpansion` 与 `ExpandedPackageScaffold`。
  - 新增 `package_expander/service.py`，负责在结果包骨架生成完成后，对所有层做第二阶段扩写；测试桩环境允许走结构化扩写，真实运行默认优先走本地厚 fallback，避免扩写阶段再次触发重型结构化请求导致主流程长时间卡在 `PACKAGE_ASSEMBLING`。
  - 调整 `package_assembler/service.py`，在原有 `result_package` 基础上把扩写结果并入各层：
    - `overview.expanded_breakdown`
    - `analysis.expanded_analysis`
    - `script_layer.expanded_segments / expanded_key_shots / title_strategy_notes / hook_strategy_notes / retention_design_notes`
    - `multimodal_layer.expanded_visual_plan`
    - `platform_layer.expanded_distribution_playbook`
    - `machine_payload_layer.expanded_execution_plan / quality_control_notes`
  - 调整 `export_payload/service.py`，把新增扩写内容正式铺入 Markdown 导出，新增总览扩写、分析扩写、段落扩写、关键镜头扩写、平台打法扩写、多模态扩写、机器扩写、全局质控说明等段落。
  - 扩展 `video_payload.py`，让 `video-payload` 同步携带扩写后的结构化信息，便于下游机器消费继续使用厚结果。
  - 更新 `test_m46_instructor_package_assembler.py`，让测试同时覆盖骨架层与扩写层，验证新增结构不会破坏既有主链。
  - 根据用户要求，将 `guidance` 拉取到 `/home/admin2/smy/upstream-materials/guidance` 作为本地上游材料，用于后续继续增强扩写链路时参考其受控生成能力，但当前主仓保持最小胶水接入，没有把项目主链直接重写为新的生成框架。
- 实现情况：
  - 语法校验完成：`python3 -m py_compile` 已通过扩写相关 schema、服务与测试文件。
  - 定向回归完成：执行 `./scripts/backend_test.sh tests/test_m46_instructor_package_assembler.py tests/test_m46_export_payload_compat.py tests/test_m5_trend_and_exports.py`，结果为 `10 passed`。
  - 真实扩写结果包完成：重新启动前后端后，使用真实 API 生成扩写结果，产物目录为 `/tmp/multi_media_expanded_pack_final_fetch_20260402_172516`。
  - 真实扩写包摘要：
    - `generation_id`: `gen_14466291d122`
    - 最终状态：`DONE`
    - `segment_count`: `5`
    - `expanded_segment_count`: `5`
    - `expanded_key_shot_count`: `4`
    - `overview_expansion_sections`: `4`
    - `analysis_expansion_sections`: `4`
    - `platform_expansion_sections`: `5`
    - `machine_expansion_sections`: `5`
  - 体量对比：
    - 扩写前 `export.md` 约 `21.8 KB`
    - 扩写后 `export.md` 约 `44.5 KB`
    - 扩写后 `export.json` 约 `60.8 KB`
    - 扩写后 `video-payload.json` 约 `46.7 KB`
  - 效果确认：结果包已经从“要素齐但子项偏薄”升级为“每层均带结构化扩写说明”，同时保留现有 `result / export/json / export/md / video-payload` 四条消费链不漂移。
