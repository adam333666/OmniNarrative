# M71 结果页设计一致性 Deck

## 1. 背景

系统第一核心卖点是“内部内容设计一致性”，也就是不同输出形态都围绕同一个中心进行编排。  
但在结果页里，这件事还没有被直接可视化，用户需要自己从各块信息里推断。

## 2. 本轮目标

- 在结果页把“同一中心如何贯穿主题、受众、风格、趋势、执行”直接展示出来
- 不新增后端逻辑，只消费现有结果真值
- 继续复用已接入的上游 `CardSwap`

## 3. 方案

- 新增 `consistency-thread-deck.tsx`
- 直接消费 `request_summary`、`analysis` 与 `result_package`
- 将主题、受众、风格、趋势、执行拆成五张翻卡
- 放入结果页总览层，成为总览之前的可讲解入口

## 4. 变更范围

- `frontend/components/result/consistency-thread-deck.tsx`
- `frontend/components/result/consistency-thread-deck.module.css`
- `frontend/components/result/result-view-client.tsx`

## 5. 预期结果

- 第一核心卖点在结果页可被直接感知，而不再只是一句抽象说明
- 结果页更清楚地展示“这是一套围绕同一中心被编排出来的方案”
- 本轮继续坚持“已有真值消费 + 已接入上游组件复用”的薄胶水实现
