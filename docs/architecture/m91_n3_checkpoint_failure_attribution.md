# M91 N3 Checkpoint 失败归因第一批

## 1. 背景

当前系统已经有：

- checkpoint 列表
- 最新状态快照
- 从最新 checkpoint 恢复结果

但失败链仍偏“开发者自己推断”，因为 checkpoint 快照里还缺少一层结构化失败归因。

## 2. 本轮目标

本轮作为 `N3` 第一批闭环，先补最小但高价值的一层：

- 在最新 checkpoint 状态中补充结构化 `failure_attribution`
- 让内部 checkpoint 控制台直接展示失败类别、失败阶段、最新错误事件与恢复建议

## 3. 新增字段

在 `GenerationCheckpointStateResponse` 中新增：

- `failure_attribution`

其最少包含：

- `category`
- `stage`
- `stage_message`
- `latest_event_type`
- `latest_error_message`
- `recovery_hint`
- `can_restore_result_snapshot`

## 4. 归因规则

### 4.1 类别规则

- 正常未失败：`not_failed`
- 超时：`timeout`
- 失败：`execution_failed`

### 4.2 恢复提示规则

- 若当前 checkpoint 已保留结果快照，则应明确提示可优先尝试恢复
- 若当前失败态没有结果快照，则应提示先查看错误事件、失败阶段和上游日志

## 5. 展示约束

内部 checkpoint 控制台的“最新状态快照”区块必须直接显示：

- 当前 failure category
- 当前失败阶段说明
- 最新错误事件类型
- 恢复建议

## 6. 完成判定

满足以下条件即可视为 `N3` 第一批完成：

1. 最新 checkpoint 状态接口返回结构化 `failure_attribution`
2. 成功链和失败链都能产出明确 category
3. 内部 checkpoint 控制台可直接看到恢复建议，而不是只显示原始字段
