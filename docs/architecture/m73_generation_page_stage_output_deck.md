# M73 生成页阶段产物 Deck

## 1. 背景

生成页当前已经能展示真实状态和阶段轨道，但“每个阶段到底会产出什么”还不够直观。  
这会让第一次使用的人仍然容易把这一页理解成单纯等待页，而不是理解系统如何一步步长成最终结果。

## 2. 本轮目标

- 让生成页更像“解释系统在做什么”的工作台
- 强化第四核心点“简单上手的操作逻辑”在等待过程中的可理解性
- 继续复用已接入的上游 `CardSwap`

## 3. 方案

- 新增 `generation-output-deck.tsx`
- 将主题真值、受众风格画像、趋势约束、叙事骨架、结构化结果包拆成五张翻卡
- 接入生成页阶段轨道下方

## 4. 变更范围

- `frontend/components/generation/generation-output-deck.tsx`
- `frontend/components/generation/generation-output-deck.module.css`
- `frontend/components/generation/generation-status-client.tsx`

## 5. 预期结果

- 用户更容易理解生成页不是“空等”，而是“系统正在加工不同层的真值”
- 第四核心点从创建页继续延伸到生成页
- 本轮继续是“已有工作流语义说明 + 已接入上游组件复用”的薄胶水实现
