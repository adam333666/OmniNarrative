# M65 主流程页内部控制台入口胶水

## 1. 背景

当前系统已经有：

- 内部趋势控制台
- 内部 checkpoint 控制台

但它们还停留在“知道路径才能打开”的状态，没有自然地接回生成页和结果页主流程。

## 2. 本轮目标

在不新增任何后端逻辑的前提下，把既有内部工具页入口接到主流程里：

- 生成页可直达 checkpoint 控制台与趋势控制台
- 结果页可直达 checkpoint 控制台与趋势控制台

## 3. 实现方式

本轮只修改现有前端页面：

- `frontend/components/generation/generation-status-client.tsx`
- `frontend/components/generation/generation-status-client.module.css`
- `frontend/components/result/result-view-client.tsx`
- `frontend/components/result/result-view-client.module.css`

没有新增：

- 新后端接口
- 新内部页面
- 新数据模型

## 4. 验证

- `cd frontend && npm run build`

## 5. 阶段意义

这轮对应总计划中的：

- `P3` 轻量内部管理能力

并且是非常典型的薄胶水实现：只把已有内部工具页自然挂回主流程，提高演示时的连贯性和可发现性。
