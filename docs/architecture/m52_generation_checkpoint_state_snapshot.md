# M52 基于 LangGraph Checkpoint 的最新状态快照读取

## 1. 目标

把 `M50/M51` 已接入的 LangGraph durable checkpoint 能力继续往前推进，补齐“读取最新状态快照”的内部能力。

本轮仍然继续直接站在上游成熟代码切片之上：

- `langchain-ai/langgraph`
- `libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/__init__.py`
- `libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/utils.py`

---

## 2. 本轮原则

- 不重写 checkpoint 状态机
- 不重写新的执行诊断系统
- 直接读取上游 checkpoint 中已有的 `channel_values` 与 metadata
- 本仓只补最小 schema、路由与结果预览胶水

---

## 3. 本轮新增能力

新增内部接口：

- `GET /api/v1/internal/generation-checkpoints/{generation_id}/latest-state`

返回内容包括：

- 最新 checkpoint id / namespace / created_at
- 当前已有的 channel keys
- 是否已经包含 `result`
- 结果标题 / 一句话摘要 / script segment 数量

---

## 4. 本轮意义

这轮属于“必须批量补完的收口”，但它的意义不是文档化，而是把已经复制进来的上游 checkpoint 能力真正变成可消费的系统功能。

只有把：

- checkpoint 列表
- checkpoint 恢复
- checkpoint 最新状态快照

一起补齐，之前引入的上游 durable execution 才算真正进入系统，而不是只停留在代码文件数量增加。

---

## 5. 验收标准

- 生成执行后，可以读取到最新 checkpoint 的状态快照
- 快照中能稳定看到 `channel_keys`
- 若结果已进入 checkpoint，能读取到标题、摘要和脚本段数量
- 本轮继续基于上游 LangGraph checkpoint 持久化能力，不新增仓内自写 checkpoint 引擎
