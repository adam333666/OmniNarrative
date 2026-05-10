# 胶水编程原材料清单与当前复用现状

## 1. 文档定位

本文档用于记录 `/home/admin2/smy/multi-media` 当前“胶水编程原材料”的最新状态。

它不再只是一期早期的候选仓库清单，而是同时回答四件事：

- 当前材料库里有哪些仓库
- 哪些已经进入主路径
- 哪些还没有进入主路径
- 基于当前 v1.0 之后的下一层级计划，是否还需要补充新的成熟仓库

本文档的判断依据包括：

- 当前仓库实际代码
- 当前 `upstream-materials` 本地材料池
- 当前阶段计划与 v1.0 后续深化目标

---

## 2. 总结结论

### 2.1 当前文档结论

当前材料库已经不是“缺少原材料”的状态，而是：

- 主链所需的大部分核心上游材料已经具备
- 其中一批已经明确进入主路径
- 另一批还处于研究储备或参考级位置

当前真正需要补的，不是大量继续加仓库，而是：

- 继续更深地复用已经拉下来的成熟仓库
- 只针对下一阶段明确目标补充少量必要仓库

### 2.2 本轮新增结论

基于 v1.0 之后的下一层级计划，这轮新判断并已拉取的仓库有：

- `microsoft/playwright`
  - 本地已拉取
  - 当前定位：下一阶段稳定性与评测主线的重要新增原材料
- `langfuse/langfuse`
  - 本地已拉取
  - 当前定位：下一阶段 LLM 观测、Tracing、评测和运行透明度增强候选

本轮没有新增更多仓库，原因是：

- 当前下一阶段最明确缺口在“评测/稳定性”而不是“再换一批底层框架”
- 其余核心能力所需上游材料，当前大多已经齐备

---

## 3. 当前材料库状态总表

### 3.1 已拉取到本地的核心仓库

本地目录：`/home/admin2/smy/upstream-materials`

| 仓库 | 本地路径 | 固定版本 | 当前角色 |
| --- | --- | --- | --- |
| `next.js` | `/home/admin2/smy/upstream-materials/next.js` | `aa3ba7ed` | 前端框架主基座 |
| `shadcn-ui` | `/home/admin2/smy/upstream-materials/shadcn-ui` | `b75796e` | 前端组件与组织参考 |
| `react-hook-form` | `/home/admin2/smy/upstream-materials/react-hook-form` | `f29f546` | 表单状态主路径 |
| `zod` | `/home/admin2/smy/upstream-materials/zod` | `c780507` | 输入校验主路径 |
| `react-markdown` | `/home/admin2/smy/upstream-materials/react-markdown` | `fda7fa5` | Markdown 渲染主路径 |
| `react-bits-main` | `/home/admin2/smy/upstream-materials/react-bits-main` | 用户提供源码快照 | 前端动效/展示组件主来源 |
| `fastapi` | `/home/admin2/smy/upstream-materials/fastapi` | `937d307` | 后端 API 框架主基座 |
| `sqlalchemy` | `/home/admin2/smy/upstream-materials/sqlalchemy` | `1aa259f` | ORM 主路径 |
| `alembic` | `/home/admin2/smy/upstream-materials/alembic` | `7b510dc` | 迁移主路径 |
| `httpx` | `/home/admin2/smy/upstream-materials/httpx` | `b5addb6` | HTTP 客户端主路径 |
| `litellm` | `/home/admin2/smy/upstream-materials/litellm` | `0af114f` | 模型统一接入层 |
| `instructor` | `/home/admin2/smy/upstream-materials/instructor` | `41f050c7` | 结构化输出主路径 |
| `langgraph` | `/home/admin2/smy/upstream-materials/langgraph` | `ae76f33c` | 执行编排主路径 |
| `RSSHub` | `/home/admin2/smy/upstream-materials/RSSHub` | `5ae7432b2` | 趋势入口主路径 |
| `crawl4ai` | `/home/admin2/smy/upstream-materials/crawl4ai` | `af648e1` | 趋势抓取/抽取主路径 |
| `pydantic-ai` | `/home/admin2/smy/upstream-materials/pydantic-ai` | `f82046b8` | Agent/runtime 储备候选 |
| `bilibili-api-python` | `/home/admin2/smy/upstream-materials/bilibili-api-python` | `0147ab61` | B 站专项候选 |
| `full-stack-fastapi-template` | `/home/admin2/smy/upstream-materials/full-stack-fastapi-template` | `8bf0025` | 工程结构参考 |
| `taxonomy` | `/home/admin2/smy/upstream-materials/taxonomy` | `651f984` | 前端结构参考 |
| `playwright` | `/home/admin2/smy/upstream-materials/playwright` | `facd84299` | 新增：稳定性/评测主候选 |
| `langfuse` | `/home/admin2/smy/upstream-materials/langfuse` | `1e7c7f912` | 新增：LLM 观测/评测候选 |

---

## 4. 哪些材料已经得到复用

### 4.1 已进入主路径的材料

#### `next.js`

- 当前状态：已复用
- 如何复用：
  - 作为前端应用基座
  - 承载首页、创建页、生成页、结果页与内部页
- 当前落地：
  - `frontend/app/`

#### `react-hook-form`

- 当前状态：已复用
- 如何复用：
  - 作为创建页五步输入向导的表单状态和校验驱动层
- 当前落地：
  - `frontend/components/wizard/create-wizard.tsx`

#### `zod`

- 当前状态：已复用
- 如何复用：
  - 作为创建请求输入 schema 和约束层
- 当前落地：
  - `frontend/lib/schemas/creation-request.ts`

#### `react-markdown`

- 当前状态：已复用
- 如何复用：
  - 作为结果页 Markdown 预览的渲染层
- 当前落地：
  - `frontend/components/result/markdown-preview.tsx`

#### `react-bits-main`

- 当前状态：已大量复用
- 如何复用：
  - 直接复制上游组件源码
  - 做最小适配后接入当前项目
- 当前已落地组件包括：
  - `dot-grid`
  - `text-type`
  - `card-swap`
  - `card-nav`
  - `pill-nav`
  - `gooey-nav`
  - `chroma-grid`
  - `glass-surface`
  - `border-glow`
- 当前意义：
  - 首页、创建页、生成页、结果页都已大量站在该材料之上

#### `fastapi`

- 当前状态：已复用
- 如何复用：
  - 作为后端 API 主框架
- 当前落地：
  - `backend/app/api/`

#### `sqlalchemy`

- 当前状态：已复用
- 如何复用：
  - 作为数据库模型、repository、session 与查询层
- 当前落地：
  - `backend/app/db/`

#### `alembic`

- 当前状态：已复用
- 如何复用：
  - 作为 migration 主路径
- 当前落地：
  - `backend/migrations/`

#### `httpx`

- 当前状态：已复用
- 如何复用：
  - 作为 RSSHub feed 等外部 HTTP 调用层
- 当前落地：
  - `backend/app/integrations/rss/rsshub_adapter.py`

#### `litellm`

- 当前状态：已复用
- 如何复用：
  - 作为模型统一接入层
  - 作为 `Instructor` 的 provider 底座
- 当前落地：
  - `backend/app/integrations/llm/litellm_adapter.py`
  - `backend/app/services/structured_output_gateway/service.py`

#### `instructor`

- 当前状态：已核心复用
- 如何复用：
  - 作为结构化输出主路径
  - 通过 `Instructor + LiteLLM + Pydantic schema` 生成结构化对象
- 当前落地模块：
  - `profile_parser`
  - `narrative_generator`
  - `package_assembler`
  - `trend_collector`
  - `structured_output_gateway`

#### `langgraph`

- 当前状态：已核心复用
- 如何复用：
  - 作为执行编排主路径
  - 作为 checkpoint 持久化、恢复、状态快照与结果恢复基础
- 当前落地模块：
  - `generation_pipeline/orchestrator`
  - `generation_pipeline/checkpointer`
  - `generation_pipeline/recovery`
  - vendored `checkpoint-sqlite`

#### `RSSHub`

- 当前状态：已复用
- 如何复用：
  - 作为趋势入口层
- 当前落地：
  - `backend/app/integrations/rss/rsshub_adapter.py`
  - `backend/app/services/trend_collector/service.py`

#### `crawl4ai`

- 当前状态：已复用
- 如何复用：
  - 作为趋势抓取、正文抽取与 Markdown 结果来源层
- 当前落地：
  - `backend/app/integrations/crawler/crawl4ai_adapter.py`
  - `backend/app/services/trend_collector/service.py`

---

## 5. 哪些材料还没有进入主路径

### 5.1 研究储备级

#### `pydantic-ai`

- 当前状态：未进入主路径
- 为什么没有用：
  - 当前主编排已经明确站到 `LangGraph`
  - 下一阶段不适合再并入第二套 agent/runtime 主内核
- 当前定位：
  - 研究储备
  - 后续如需 typed tool-calling、deps 注入、event stream，可局部评估

#### `langfuse`

- 当前状态：本轮新拉取，未进入主路径
- 为什么现在还没用：
  - v1.0 已经完成，本轮只是为下一阶段做材料补充
  - 目前项目已有基本 diagnostics，但还没有完整 tracing / eval / prompt trace 平台
- 当前定位：
  - 下一阶段 `N3/N4/N7` 的观测与评测候选

### 5.2 待法律/策略判断级

#### `bilibili-api-python`

- 当前状态：未进入主路径
- 为什么没有用：
  - 许可证风险尚未最终收口
  - 当前 `RSSHub + Crawl4AI` 已经能支撑趋势增强链
- 当前定位：
  - B 站专项入口候选
  - 如许可证不能接受，则正式放弃

### 5.3 参考级

#### `full-stack-fastapi-template`

- 当前状态：未直接进入主路径
- 为什么没有用：
  - 它更适合作为工程组织参考
  - 不适合整仓继承，否则会把无关能力一起带入
- 当前定位：
  - 只读工程参考

#### `taxonomy`

- 当前状态：未直接进入主路径
- 为什么没有用：
  - 它更适合作为页面结构和信息密度参考
  - 不是当前项目的直接代码来源
- 当前定位：
  - 前端结构参考

#### `shadcn-ui`

- 当前状态：当前未作为大规模直接代码来源
- 为什么没有用得更多：
  - 当前前端展示更依赖 `react-bits-main` 复制适配组件
  - `shadcn-ui` 主要被作为组织方式与基础组件参考，而不是当前主视觉来源
- 当前定位：
  - 轻参考 / 备用组件来源

---

## 6. 本轮新增仓库判断

### 6.1 `microsoft/playwright`

- 当前状态：本轮新增并已拉取
- 固定版本：`facd84299`
- 新增原因：
  - 下一阶段最明确的新目标之一是稳定性与评测能力增强
  - 当前虽然已有 `backend_test.sh`、`demo_regression.sh`、`smoke_test.sh`
  - 但还缺前端/全链路自动化评测框架
- 为什么值得加入：
  - 它是前端与 E2E 测试的成熟事实标准之一
  - 直接契合 `N4` 和 `N7`
- 计划复用方向：
  - 页面级主流程回归
  - 结果页/导出入口检查
  - 首次使用路径评测

### 6.2 `langfuse/langfuse`

- 当前状态：本轮新增并已拉取
- 固定版本：`1e7c7f912`
- 新增原因：
  - 下一阶段需要更强的 LLM 观测、trace、prompt 级追踪与评测能力
- 为什么值得加入：
  - 当前项目已经有 `Instructor + LiteLLM + LangGraph`
  - 后续如要做更完整的运行透明度与评测体系，Langfuse 是明确成熟候选
- 计划复用方向：
  - 模型调用 trace
  - 结构化输出观测
  - 后续评测/质量观察体系

### 6.3 本轮没有新增的方向

#### `Radix UI`

- 当前状态：本轮未拉取
- 原因：
  - 当前已有 `shadcn-ui`
  - 这一层当前不是下一阶段最关键缺口

#### 其他重型工作流、任务系统、后台模板

- 当前状态：本轮未引入
- 原因：
  - 当前下一阶段目标不在“换主框架”
  - 当前重点仍然是继续深挖已有成熟材料

---

## 7. 当前材料库是否还需要继续扩仓

当前判断：

- 短期内不需要再大量补充新的仓库
- 下一阶段最重要的是：
  1. 更深地复用 `Instructor`
  2. 更深地复用 `LangGraph`
  3. 更深地复用 `RSSHub + Crawl4AI`
  4. 把 `Playwright` 和 `Langfuse` 逐步接入稳定性/评测主线

也就是说，当前缺的已经不是“更多仓库”，而是“把已经有的成熟材料吃得更完整”。

---

## 8. 结论

当前材料库状态可以概括为：

- 核心主链材料已经齐备
- 主链关键能力已经明确站在成熟上游仓库之上
- 新增最值得补充的方向已经补为：
  - `Playwright`
  - `Langfuse`
- 其余下一阶段工作，应优先围绕现有材料继续深化，而不是继续盲目扩仓
