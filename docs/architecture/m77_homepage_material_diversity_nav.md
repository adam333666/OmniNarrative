# M77 首页材料库组件多样化导航

## 1. 背景

前几轮前端展示虽然已经接入多种上游组件，但从用户可感知层面看，`CardSwap` 仍然占比较高。  
为了避免展示语言长期单一，需要继续把材料库中的不同组件引入到主链页面。

## 2. 本轮目标

- 在首页引入除 `CardSwap` 之外的新上游交互组件
- 让首页的交互语言更丰富
- 同时服务 `M-P2-A` 首页入口能力与首页可导航性

## 3. 方案

- 新增 `upstream/gooey-nav.tsx`
- 参考 `react-bits-main` 的 `GooeyNav` 做最小适配
- 在首页新增 `homepage-signal-nav.tsx`
- 用它把一致性主线、趋势增强链、结果成品、立即开始等锚点连起来

## 4. 变更范围

- `frontend/components/upstream/gooey-nav.tsx`
- `frontend/components/upstream/gooey-nav.module.css`
- `frontend/components/landing/homepage-signal-nav.tsx`
- `frontend/components/landing/homepage-signal-nav.module.css`
- `frontend/components/landing/creative-hero.tsx`
- `frontend/components/landing/consistency-thread-showcase.tsx`
- `frontend/components/landing/trend-amplifier-showcase.tsx`

## 5. 预期结果

- 首页不再长期主要依赖翻卡组件形成主要交互
- 材料库组件复用更加多样
- 首页整体更像一个可交互的产品入口，而不是一组静态展示块
