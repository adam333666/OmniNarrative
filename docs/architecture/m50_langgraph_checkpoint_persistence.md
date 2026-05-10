# M50 LangGraph Checkpoint 持久化接入

## 1. 目标

把 `LangGraph` 的 checkpoint 持久化能力真正接入当前生成编排链，而不是只停留在 `StateGraph` 内存执行层。

本轮直接复用上游成熟代码切片：

- `langchain-ai/langgraph`
- `libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/__init__.py`
- `libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/utils.py`

---

## 2. 本轮原则

- 优先整块复用上游 checkpoint-sqlite 核心实现
- 本仓只补最小胶水：
  - 本地路径配置
  - checkpointer 单例管理
  - orchestrator 调用时注入 `thread_id`
  - 内部查询接口

---

## 3. 本轮新增能力

### 3.1 编排 checkpoint 持久化

当前 `generation_pipeline/orchestrator.py` 编译图时已注入 SQLite checkpointer。

这意味着：

- 同一 `generation_id` 的图执行会留下 LangGraph checkpoint
- 后续继续做后台执行链真实化时，不必从零重造 checkpoint 机制

### 3.2 内部 checkpoint 查询接口

新增内部接口：

- `GET /api/v1/internal/generation-checkpoints/{generation_id}`

用于读取：

- checkpoint id
- checkpoint namespace
- channel keys
- metadata
- pending write 数量

---

## 4. 验收标准

- 编排执行后会生成 SQLite checkpoint
- 内部接口可以读取对应 generation 的 checkpoint 列表
- 本轮实现主要来自上游 `LangGraph checkpoint-sqlite` 成熟代码切片，而不是仓内手写 checkpoint 持久化逻辑
