# M51 基于 LangGraph Checkpoint 的结果恢复

## 1. 目标

把 `M50` 已接入的 LangGraph durable checkpoint，从“可查看”推进到“可恢复”。

本轮继续复用上一轮已经整块引入的上游成熟代码切片：

- `langchain-ai/langgraph`
- `libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/__init__.py`
- `libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/utils.py`

---

## 2. 本轮原则

- 不手写新的 checkpoint 存储机制
- 不手写新的执行恢复框架
- 直接基于上游 `SqliteSaver` 已持久化的 `channel_values` 做最小恢复胶水

---

## 3. 本轮新增能力

### 3.1 从最新 checkpoint 恢复结果快照

新增内部接口：

- `POST /api/v1/internal/generation-checkpoints/{generation_id}/restore-latest`

能力边界：

- 当某次生成已经执行过，且最新 checkpoint 中已有 `result` channel 时
- 即使结果快照还没落回本地 `generation_results`
- 也可以直接从 checkpoint 恢复结果真值并补写回结果仓

### 3.2 恢复后自动收口状态

恢复成功后：

- 当前 generation 的结果快照会重新保存
- generation 状态会被收口到 `DONE`

---

## 4. 验收标准

- 生成执行后，即使结果仓仍为空，也可以从 checkpoint 恢复结果
- 恢复成功后 `generation_results` 中可重新读到结果真值
- generation 状态同步变为 `DONE`
- 本轮实现继续基于上游 LangGraph checkpoint 持久化能力，而不是仓内重新发明恢复机制
