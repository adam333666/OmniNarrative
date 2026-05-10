# M89 N2 多来源趋势增强第一批

## 1. 背景

当前趋势链已经具备：

- `RSSHub` feed 入口
- `Crawl4AI` 页面抓取入口
- `Instructor` 结构化归纳链
- `source_trace` 来源轨迹

但当前同平台仍偏“单来源覆盖”，还没有形成真正的多来源输入层。

## 2. 本轮目标

本轮作为 `N2` 的第一批闭环，锁定两件事：

1. 同平台允许同时吸收 `RSSHub + Crawl4AI` 两类来源
2. 趋势模板关键字段再加厚 3 类

## 3. 新增趋势字段

在 `PlatformTrendTemplate / StructuredTrendObservation / TrendTemplateSummary` 中新增：

- `interaction_patterns`
- `emotional_entry_points`
- `creator_angle_summary`

含义：

- `interaction_patterns`：近期更容易触发评论、转发、补充讨论的互动方式
- `emotional_entry_points`：近期更有效的情绪切入点
- `creator_angle_summary`：当前平台更适合创作者采用的表达角度摘要

## 4. 多来源合流约束

### 4.1 同平台来源合流

若同一平台同时获得：

- `RSSHub` feed 文档
- `Crawl4AI` 页面文档

则不得再使用“先到先覆盖”的单源策略，而应：

- 合并 markdown 供结构化归纳使用
- 合并 `source_trace`
- 记录复合 `source_type`

### 4.2 `source_type` 规则

允许新增：

- `hybrid_collected`

表示本次趋势模板由多来源共同生成。

## 5. 导出与展示约束

- 结果页趋势影响区必须能看到新增字段
- Markdown 导出必须输出新增字段
- 内部趋势接口 `/config/trend-templates` 与 `/internal/trend-summary/{platform}` 必须透传新增字段

## 6. 完成判定

满足以下条件即可视为 `N2` 第一批闭环完成：

1. 趋势模板比当前新增至少 3 类字段
2. 同平台可同时保留两类来源轨迹
3. 结果页与导出层均能看见新增字段
