# M69 创建页趋势策略真值展示

## 1. 背景

创建页已经能显示趋势摘要，但还没有把趋势模板中更有价值的结构化策略字段完整展示出来。  
当前后端真值里实际上已经有 `hook_patterns`、`rhythm_patterns`、`title_cover_style`、`avoid_patterns`、`audience_preference_summary`，只是前端没有完整消费。

## 2. 本轮目标

- 让创建页真正展示“趋势如何参与传播增强”
- 不新造趋势逻辑，只把现有后端趋势真值更完整地透传给前端
- 继续复用项目中已接入的上游 `CardSwap`

## 3. 方案

- 扩展 `/config/trend-templates` 的摘要响应字段
- 前端 `TrendTemplateSummary` 对齐新增字段
- 在 `TrendSignalPanel` 中新增趋势策略 deck
- 继续复用 `frontend/components/upstream/card-swap.tsx`

## 4. 变更范围

- `backend/app/schemas/trend_template.py`
- `backend/app/services/trend_strategy/service.py`
- `backend/tests/test_m69_trend_template_summary_fields.py`
- `frontend/lib/api-client/backend.ts`
- `frontend/components/wizard/trend-signal-panel.tsx`
- `frontend/components/wizard/trend-strategy-deck.tsx`
- `frontend/components/wizard/trend-strategy-deck.module.css`

## 5. 预期结果

- 用户在创建前就能看到趋势摘要之外的策略真值
- 趋势增强不再只是“说系统会参考趋势”，而是可直接展示“系统当前掌握了哪些传播策略”
- 这轮继续遵循“现有后端真值透传 + 上游展示组件复用”的胶水边界
