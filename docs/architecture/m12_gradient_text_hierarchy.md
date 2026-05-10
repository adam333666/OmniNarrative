# M12 标题层级渐变文本增强

## 目标

在 `M10` 完成首页流程与指标增强、`M11` 完成结果页信息聚焦列表增强之后，继续从本地 `react-bits-main` 源码中借成熟的标题表现语义，提升页面分区层级感。

本阶段目标：
- 让首页与结果页的关键分区标题具备更强的视觉层次。
- 保持信息结构不变，只增强标题表现。
- 不引入 `motion/react` 或其他新依赖。

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/TextAnimations/GradientText/GradientText.tsx`

## 适配原则

- 保留上游 `GradientText` 的核心语义：通过渐变色流动提升标题层次感。
- 不引入 `motion/react`；改用纯 CSS background-clip 与 keyframes 实现轻量等价效果。
- 颜色体系继续服从当前项目的暖色与青绿色双主色，不复制上游默认紫色方案。
- 仅用于标题和分区强调，不扩散到正文，避免影响可读性。

## 变更范围

### 首页
- 为首页的主分区标题接入渐变文本样式。

### 结果页
- 为结果页关键总览标题接入渐变文本样式。
- 不改动分析面板、脚本层和导出动作的结构。

## 当前阶段明确不做

- 不改动接口、数据结构和导出链路。
- 不引入逐字动画或重型背景动效。
- 不替换现有 `ShinyText` 的主标题职责。

## 验证要求

- 变更后执行 `npm run build`。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口。
