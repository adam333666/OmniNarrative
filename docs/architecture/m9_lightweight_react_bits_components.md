# M9 轻量 React Bits 组件实装方案

## 目标

在当前前端已完成视觉增强、Markdown 预览和构建验证的基础上，继续从 `react-bits-main` 中引入真正可运行的轻量组件模式，而不是只借结构语义。

本阶段目标：
- 在不引入额外运行时依赖的前提下，实装文字高光与卡片聚光两类轻量交互。
- 继续坚持“基于本地上游源码材料适配”，不自己发明一套效果。
- 只选择当前项目最容易承接、最不易引发漂移的轻量组件。

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/TextAnimations/ShinyText/ShinyText.tsx`
- `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/TextAnimations/ShinyText/ShinyText.css`
- `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/Components/SpotlightCard/SpotlightCard.tsx`
- `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/Components/SpotlightCard/SpotlightCard.css`

## 适配原则

- `ShinyText`：保留其高光扫过的视觉语义，但不引入 `motion/react`，直接用 CSS keyframes 实现最小等价效果。
- `SpotlightCard`：保留其鼠标聚光交互逻辑，用轻量 React 事件和 CSS 自定义变量实现。
- 所有适配都要围绕当前项目的暖色调视觉系统重新设色，避免直接复制上游暗色卡片风格造成漂移。

## 变更范围

### 首页
- 主标题或强调文案引入 ShinyText 效果。
- Bento 信息卡切换为 SpotlightCard 包裹，增加可交互聚光层。

### 结果页
- 总览层与 Markdown 预览卡增加 SpotlightCard 交互。
- 继续保持结果结构与导出链路不变。

## 当前阶段明确不做
- 不引入 `motion/react`。
- 不引入 WebGL / Canvas 动效。
- 不改动结果 API、Markdown API、Video payload API。

## 验证要求
- 变更后继续执行 `npm run build`。
- docs、代码、changelog、git commit 必须保持同批次一致。
