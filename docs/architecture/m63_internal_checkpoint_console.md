# M63 轻量内部 Checkpoint 控制台

## 1. 背景

当前系统已经具备：

- `LangGraph` 编排主路径
- durable checkpoint 持久化
- checkpoint 最新状态读取
- checkpoint 恢复结果

但这些能力主要还是停留在内部 API 层，缺少一个可直接打开和演示的轻量入口。

## 2. 本轮目标

新增一个轻量内部 checkpoint 页面，用最小前端胶水直接消费已有内部接口：

- 查看 checkpoint 列表
- 查看最新 checkpoint 状态
- 触发“从最新 checkpoint 恢复结果”

## 3. 具体实现

新增页面：

- `frontend/app/internal/checkpoints/[id]/page.tsx`
- `frontend/app/internal/checkpoints/[id]/page.module.css`

页面特征：

- 不新增任何新的后端执行或存储逻辑
- 只消费现有内部接口
- 用服务端 action 触发恢复动作
- 用卡片和列表方式展示 checkpoint 真值

## 4. 验证

- `cd frontend && npm run build`

## 5. 阶段意义

这轮对应总计划中的：

- `P3` 轻量内部管理能力

并且是明确的薄胶水实现：前端只做展示与调用，`LangGraph`、checkpoint 持久化与恢复主逻辑保持完全复用现有后端能力。
