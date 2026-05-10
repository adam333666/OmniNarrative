# M76 首页趋势增强闭环 Showcase

## 1. 背景

里程碑 `M-P1-C` 需要形成“趋势入口 -> 结构化归纳 -> 创建前展示 -> 结果影响”的完整演示闭环。  
此前创建页和结果页已经分别完成趋势策略预览与趋势影响展示，但首页仍缺少对这条链路的前置说明。

## 2. 本轮目标

- 在首页直接讲清“趋势增强是如何一路进入最终方案的”
- 同时服务 `M-P1-C` 与 `M-P2-A`
- 继续复用已接入的上游 `CardSwap`

## 3. 方案

- 新增 `trend-amplifier-showcase.tsx`
- 用翻卡方式说明成熟入口、结构化归纳、创建前展示、结果影响四段链路
- 放在首页一致性 showcase 之后，形成第二条核心卖点的完整前置叙事

## 4. 变更范围

- `frontend/components/landing/trend-amplifier-showcase.tsx`
- `frontend/components/landing/trend-amplifier-showcase.module.css`
- `frontend/components/landing/creative-hero.tsx`

## 5. 预期结果

- 首页、创建页、结果页三处能够共同组成趋势增强的演示闭环
- 首页更接近完整产品入口，而不只是能力标题集合
- 本轮继续是“已有产品叙事说明 + 已接入上游组件复用”的薄胶水实现
