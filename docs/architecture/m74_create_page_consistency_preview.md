# M74 创建页一致性预览 Deck

## 1. 背景

里程碑 `M-P0-B` 的完成判定要求：

- 用户在结果页能直接看到主题、受众、风格、趋势、执行围绕同一中心编排
- 至少 1 个首页或创建页入口也能提前预告这条一致性逻辑

当前结果页侧已经通过 `M71` 有了设计一致性 deck，但创建前仍缺少一个前置入口来解释“输入并不是分散表单，而是在织同一条主线”。

## 2. 本轮目标

- 把“内部对齐 / 设计一致性”的逻辑前置到创建页
- 不新增后端逻辑，只消费当前表单真值
- 继续复用已接入的上游 `CardSwap`

## 3. 方案

- 新增 `consistency-preview-deck.tsx`
- 直接消费当前输入中的主题、受众、平台、风格
- 通过翻卡方式说明这四层如何共同组成统一中心
- 放在创建页输入流程上方，作为预设 deck 之后的第二层说明

## 4. 变更范围

- `frontend/components/wizard/consistency-preview-deck.tsx`
- `frontend/components/wizard/consistency-preview-deck.module.css`
- `frontend/components/wizard/create-wizard.tsx`

## 5. 预期结果

- 用户在创建页就能理解系统不是填几项表单，而是在先搭一条“内部对齐”的主线
- `M-P0-B` 不再只在结果页成立，而是已经前置到创建页
- 本轮继续是“已有表单真值消费 + 已接入上游组件复用”的薄胶水实现
