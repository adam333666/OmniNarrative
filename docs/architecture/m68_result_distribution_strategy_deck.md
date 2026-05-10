# M68 结果页传播策略 Deck

## 1. 背景

结果页已经有“传播备选区”，但目前仍主要是列表式展示。  
这会让重型结果包的展示偏静态，不够适合答辩、演示和快速切换传播重点。

## 2. 本轮目标

- 让传播备选区更像一个可讲解的策略 deck
- 不新增后端逻辑，继续只消费现有结果真值
- 继续复用项目里已经接入的上游 `CardSwap`

## 3. 方案

- 新增 `distribution-strategy-deck.tsx`
- 继续复用已有的 `frontend/components/upstream/card-swap.tsx`
- 把标题备选、开场钩子、封面文案、传播角度按组做成翻卡
- 原有列表区继续保留，翻卡区负责更强的展示入口

## 4. 变更范围

- `frontend/components/result/distribution-strategy-deck.tsx`
- `frontend/components/result/distribution-strategy-deck.module.css`
- `frontend/components/result/result-view-client.tsx`

## 5. 预期结果

- 传播备选区更适合演示与答辩
- 用户可以更直观地感知系统并不是只给一个结果，而是给多组传播策略备选
- 本轮继续坚持“上游组件复用 + 最小胶水接入”
