# M53 Checkpoint 感知的结果物化

## 1. 目标

把 `M50/M51/M52` 已接入的 LangGraph durable checkpoint 能力真正接到用户主链上。

本轮目标不是继续新增一个内部调试接口，而是让：

- `/creations/{generation_id}/result`
- `/creations/{generation_id}/export/json`
- `/creations/{generation_id}/export/md`
- `/creations/{generation_id}/video-payload`

在结果仓暂时为空时，优先尝试从最新 checkpoint 恢复结果，而不是重新跑一遍 orchestrator。

---

## 2. 本轮原则

- 不重写新的恢复引擎
- 不在结果链上再造一套缓存系统
- 直接复用已经落地的上游 LangGraph checkpoint 持久化能力
- 本仓只在结果物化协调层补最小判断和回填胶水

---

## 3. 本轮新增能力

### 3.1 结果链自动尝试 checkpoint 恢复

当 `generation_results` 中没有结果，但当前 generation 已到：

- `PACKAGE_ASSEMBLING`
- `DONE`

时，结果物化协调层会先尝试从最新 checkpoint 读取 `result` channel：

- 如果读到结果，就直接补写回结果仓并返回
- 如果没有结果，再按原逻辑继续执行 orchestrator

### 3.2 用户主链自动受益

因为前端结果页和三类导出都统一经过 `generation_result_builder`，所以这一轮不是只加了后端小能力，而是让用户主链直接具备更强的结果恢复韧性。

---

## 4. 本轮意义

这轮属于“批量收口直接服务功能”的典型例子：

- 如果只做 checkpoint 列表、恢复、快照接口，系统仍然需要人工触发恢复
- 只有把 checkpoint 恢复能力接进结果物化主链，之前整块复制进来的上游 durable execution 能力才开始直接提升产品可用性

---

## 5. 验收标准

- 当结果仓为空但 checkpoint 已含 `result` 时，`generation_result_builder` 不再重跑 orchestrator
- 会直接从 checkpoint 恢复结果并补写回结果仓
- 恢复后 generation 状态收口为 `DONE`
- 本轮仍然继续站在上游 LangGraph checkpoint 持久化能力之上，不新增仓内自写恢复核心
