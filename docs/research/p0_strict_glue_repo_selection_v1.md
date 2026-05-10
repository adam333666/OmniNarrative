# P0 强胶水仓库选型与本地准入记录 V1

## 1. 文档目标

本文档用于落实 `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md` 中的 P0 阶段：

> 先完成 GitHub 候选仓库检索、主备仓判断、本地源码拉取、许可证判断与最小准入结论，再进入关键业务能力实现。

本文档只回答以下问题：
- 哪些仓库已经拉到本地
- 它们各自覆盖什么能力
- 它们的许可证是否适合直接进入主实现路径
- 下一步应优先接哪个，哪些必须暂缓

---

## 2. 当前结论摘要

### 2.1 已通过主路径准入的候选

- `567-labs/instructor`
  - 用途：结构化输出、Pydantic 校验、response model 驱动生成
  - 许可证：MIT
  - 结论：可作为**结构化输出主方案**

- `pydantic/pydantic-ai`
  - 用途：typed agent runtime、工具调用、可观测生成编排
  - 许可证：MIT
  - 结论：可作为**执行编排主候选之一**

- `langchain-ai/langgraph`
  - 用途：状态图式 agent / workflow orchestration
  - 许可证：MIT
  - 结论：可作为**执行编排主候选之一**

### 2.2 已拉取但暂不建议直接进入主路径的候选

- `DIYgod/RSSHub`
  - 用途：站点 / 平台 feed 聚合与 route 生态
  - 许可证：AGPL-3.0
  - 结论：**暂不直接并入主实现路径**
  - 原因：网络服务型 copyleft 风险高，需要先做明确许可证策略判断

- `Nemo2011/bilibili-api`
  - 用途：Bilibili 专项 API 封装
  - 许可证：GPL-3.0
  - 结论：**暂不直接并入主实现路径**
  - 原因：GPL-3.0 对主仓直接集成风险较高，需先完成许可证兼容性判断

---

## 3. 本地拉取结果

| 仓库 | 本地路径 | 当前 commit | 许可证 | 当前准入结论 |
| :--- | :--- | :--- | :--- | :--- |
| `567-labs/instructor` | `/home/admin2/smy/upstream-materials/instructor` | `41f050c7` | MIT | 通过 |
| `pydantic/pydantic-ai` | `/home/admin2/smy/upstream-materials/pydantic-ai` | `f82046b8` | MIT | 通过 |
| `langchain-ai/langgraph` | `/home/admin2/smy/upstream-materials/langgraph` | `ae76f33c` | MIT | 通过 |
| `DIYgod/RSSHub` | `/home/admin2/smy/upstream-materials/RSSHub` | `5ae7432b2` | AGPL-3.0 | 暂缓 |
| `Nemo2011/bilibili-api` | `/home/admin2/smy/upstream-materials/bilibili-api-python` | `0147ab61` | GPL-3.0 | 暂缓 |

---

## 4. 各仓库能力判断

## 4.1 `instructor`

### 代码级定位

从 README 与本地源码可确认：
- 核心定位是“Structured Outputs for LLMs”
- 以 Pydantic model 作为输出真值
- 适合直接替换当前仓内自写的：
  - 受众画像抽取
  - 风格画像抽取
  - 结构化结果子块生成

### 为什么契合当前项目

当前项目已经有：
- FastAPI
- Pydantic schema
- LiteLLM / model gateway

因此 `Instructor` 可以直接站在现有 schema 上工作，不需要新建另一套数据定义体系。

### 当前建议

优先用于：
- `AudienceProfile`
- `StyleProfile`
- `NarrativePackage` 的部分子结构生成

---

## 4.2 `pydantic-ai`

### 代码级定位

从 README 与本地源码可确认：
- 是 “GenAI Agent Framework, the Pydantic way”
- 强调 typed agent、tool calling、structured workflows

### 为什么契合当前项目

它与当前项目的 Pydantic / FastAPI 技术栈一致，适合作为：
- 生成链编排层候选
- 类型化 LLM 调用控制层候选

### 当前建议

优先作为：
- `generation_pipeline` 替代主候选之一

---

## 4.3 `langgraph`

### 代码级定位

从 README 与本地源码可确认：
- 是“Low-level orchestration framework for building stateful agents”
- 更强调状态图、可恢复工作流与图式编排

### 为什么契合当前项目

当前项目已有：
- generation status 持久化
- 事件轨迹
- diagnostics

这些都与状态图式执行框架有天然耦合点，因此 `LangGraph` 很适合作为当前自写 `orchestrator/coordinator/runner` 的替代方向。

### 当前建议

优先作为：
- `generation_pipeline` 替代主候选之一
- 与 `pydantic-ai` 并列做 PoC 对比

---

## 4.4 `RSSHub`

### 代码级定位

从 README 可确认：
- 核心定位是“Everything is RSSible”
- 适合作为平台 feed / route 聚合入口

### 为什么有价值

如果许可证允许，它能显著降低：
- 自己维护各平台入口 route 的成本
- 自己手写 feed 聚合的成本

### 当前阻塞

许可证为 **AGPL-3.0**。

在当前阶段，尚未完成：
- 主仓许可证策略判断
- 是否允许以服务调用方式旁路使用
- 是否允许直接代码集成

### 当前结论

可继续作为**研究与参考材料**，但在许可证未明确前：
- 不得直接进入主实现路径
- 不得直接作为主仓依赖方案写入代码

---

## 4.5 `bilibili-api-python`

### 代码级定位

从 README 可确认：
- 是 Bilibili 专项 API 封装
- 提供较多结构化能力

### 为什么有价值

如果许可证允许，它有潜力替代纯 HTML 抓取方式，对 B 站平台趋势源更稳定。

### 当前阻塞

许可证为 **GPL-3.0**。

因此在未完成许可证审查前：
- 不得直接进入主实现路径

### 当前结论

可继续作为**平台专项研究候选**，当前不纳入直接接入计划。

---

## 5. P0 阶段的最终主备仓判断

### 5.1 结构化输出链

- 主仓：`instructor`
- 备仓：继续评估 `pydantic-ai` 内部结构化输出能力

### 5.2 执行编排链

- 主候选 A：`pydantic-ai`
- 主候选 B：`langgraph`
- 下一步：必须做本地 PoC 后二选一

### 5.3 趋势追踪链

- 页面抽取主仓：`crawl4ai`（已在本地）
- feed / route 研究候选：`RSSHub`
- 平台专项研究候选：`bilibili-api-python`

### 5.4 当前可直接进入实现阶段的仓库

当前只建议直接进入后续 PoC / 代码接入的仓库：
- `instructor`
- `pydantic-ai`
- `langgraph`
- 已有的 `crawl4ai`
- 已有的 `litellm`

---

## 6. 下一步实施建议

P0 完成后，下一步应立即进入：

### 6.1 P1-A：`Instructor` 结构化输出 PoC

目标：
- 用真实本地 schema 替换 `profile_parser` 的规则主路径

建议 PoC 范围：
- `AudienceProfile`
- `StyleProfile`

### 6.2 P2-A：`PydanticAI` vs `LangGraph` 执行编排 PoC

目标：
- 比较哪一个更适合替换当前 `generation_pipeline`

比较维度：
- 与当前 Pydantic schema 的耦合度
- 与数据库状态表的接入难度
- 与 diagnostics / events 的整合复杂度
- 需要保留多少仓内自写 glue

### 6.3 趋势链许可证前置判断

在许可证未明确前：
- `RSSHub`
- `bilibili-api-python`

只能继续做研究，不得直接进入主实现路径。

---

## 7. 当前阶段结论

P0 当前已经完成了最关键的一步：

> 不是停留在“脑内推荐哪些 GitHub 仓库”，而是把主候选仓库真正拉到了本地，并完成了第一轮许可证与准入判断。

从现在开始，后续开发应遵循以下新基线：

- 能用 `Instructor` 的地方，不再默认自写结构化解析
- 能用 `PydanticAI / LangGraph` 的地方，不再默认扩写本仓执行框架
- 能用 `Crawl4AI` 的地方，不再自写通用抓取器
- `RSSHub` 与 `bilibili-api-python` 在许可证未确认前只做研究参考，不进入主实现路径
