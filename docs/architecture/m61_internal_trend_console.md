# M61 轻量内部趋势控制台

## 1. 背景

当前系统已经具备内部趋势接口与趋势刷新主链，但这些能力主要停留在后端接口层。对演示和接手开发来说，还缺少一个可直接打开、可手动刷新、可查看各平台趋势摘要的轻量入口。

## 2. 本轮目标

新增一个轻量前端页面，把下面这些能力可视化：

- 手动刷新趋势
- 查看各平台当前趋势摘要
- 查看趋势来源类型
- 查看热点摘要

## 3. 具体实现

新增页面：

- `frontend/app/internal/trends/page.tsx`
- `frontend/app/internal/trends/page.module.css`

页面能力：

- 服务端读取 `INTERNAL_API_KEY`
- 调用后端内部接口获取各平台趋势摘要
- 通过服务端 action 调用内部趋势刷新接口
- 用卡片方式展示 `platform / source_type / updated_at / hot_topics_summary`

## 4. 环境补充

为了让前端服务端页面能调用内部趋势接口，本轮补充：

- `frontend/.env.local.example` 增加 `INTERNAL_API_KEY`
- `README.md` 增加内部趋势控制台说明

## 5. 验证

- `cd frontend && npm run build`

## 6. 阶段意义

这轮对应总计划中的：

- `P3` 轻量内部管理能力

它的意义是把“外部趋势导入与传播增强”从纯后端能力推进到一个可以直接展示、手动操作、方便解释的页面入口。
