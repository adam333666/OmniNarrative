# M75 首页一致性主线 Showcase

## 1. 背景

里程碑 `M-P0-B` 的最后一段缺口，是首页还没有承担“内部对齐 / 设计一致性”的前置说明。  
此前这一能力已经在创建页和结果页建立，但首页还没有把这条逻辑提前讲给用户。

## 2. 本轮目标

- 让首页也承担一致性主线的前置说明
- 形成“首页 -> 创建页 -> 结果页”的一致性讲述链
- 继续复用已接入的上游 `CardSwap`

## 3. 方案

- 新增 `consistency-thread-showcase.tsx`
- 用翻卡方式说明主题、受众、风格、趋势、结果包如何围绕同一中心继续生长
- 放在首页 workflow 区之后，作为四个核心点之外的结构性说明层

## 4. 变更范围

- `frontend/components/landing/consistency-thread-showcase.tsx`
- `frontend/components/landing/consistency-thread-showcase.module.css`
- `frontend/components/landing/creative-hero.tsx`

## 5. 预期结果

- 首页、创建页、结果页三处都能直接解释“内部内容设计一致性”
- 里程碑 `M-P0-B` 可以进入完成态
- 本轮继续是“已有产品叙事说明 + 已接入上游组件复用”的薄胶水实现
