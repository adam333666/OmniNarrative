# M92 N3 执行链可解释控制台收口

## 1. 背景

`N3` 第一批已经让 checkpoint 最新状态具备：

- `failure_attribution`

但当前内部 checkpoint 控制台仍主要是：

- checkpoint 列表
- checkpoint 状态
- 恢复按钮

这还不足以让评测和排障人员在一页里看清：

- 当前 status 在哪
- 最近发生了哪些事件
- checkpoint 给出的恢复建议是什么

## 2. 本轮目标

把内部 checkpoint 控制台推进到“一页能串起状态、事件、checkpoint”的最小闭环。

## 3. 展示要求

内部 checkpoint 控制台必须同时展示三层信息：

1. `status_snapshot`
2. 最近事件轨迹
3. checkpoint 状态与失败归因

## 4. 最小完成形态

### 4.1 状态层

至少显示：

- `status`
- `current_stage`
- `error_message`
- `total_elapsed_seconds`

### 4.2 事件层

至少显示最近若干条事件，并保留：

- `event_type`
- `stage`
- `stage_message`
- `occurred_at`
- `error_message`

### 4.3 checkpoint 层

继续显示：

- `has_result`
- `result_title`
- `script_segment_count`
- `failure_attribution`

## 5. 完成判定

满足以下条件即可视为 `N3` 里程碑收口：

1. 内部 checkpoint 控制台能同时看见状态、事件、checkpoint 三层
2. 失败链可以在同一页被串起来理解
3. 控制台能直接给出恢复还是排障的下一步提示
