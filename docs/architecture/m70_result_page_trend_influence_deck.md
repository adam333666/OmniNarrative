# M70 结果页趋势影响 Deck

## 1. 背景

结果页已经能展示趋势摘要，但“趋势如何影响最终方案”仍然不够直观。  
这会削弱系统第二核心卖点，也就是“导入外部趋势后对传播性进行增强改造”。

## 2. 本轮目标

- 在结果页直接展示趋势影响的具体结构
- 不新增后端逻辑，只消费已经存在于分析层的趋势真值
- 继续复用已接入的上游 `CardSwap`

## 3. 方案

- 新增 `trend-influence-deck.tsx`
- 直接消费 `analysis.trend_summary`
- 将钩子模式、节奏模式、标题封面风格、规避点、热点线索做成翻卡策略组
- 将其放入结果页分析面板中

## 4. 变更范围

- `frontend/components/result/trend-influence-deck.tsx`
- `frontend/components/result/trend-influence-deck.module.css`
- `frontend/components/result/result-view-client.tsx`

## 5. 预期结果

- 用户在结果页能更直观看到“趋势如何改造内容设计”
- 第二核心卖点从抽象表述变成结果页可讲解、可演示的具体结构
- 本轮继续是“已有真值消费 + 已接入上游组件复用”的薄胶水实现
