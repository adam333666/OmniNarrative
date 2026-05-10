# M6 前端视觉增强方案

## 目标

在不偏离一期 PRD 主链路的前提下，对首页和结果页进行第一轮去占位化视觉升级。

本阶段的目标不是新增业务能力，而是：
- 提升首页的展示张力与品牌感。
- 提升结果页的信息分层、节奏感与可读性。
- 严格基于本地上游源码材料做复用，不凭空发明动画与视觉结构。

## 原材料来源

本阶段优先参考以下本地源码材料：
- /home/admin2/smy/upstream-materials/react-bits-main/src/components/landing/Hero/Hero.jsx
- /home/admin2/smy/upstream-materials/react-bits-main/src/components/landing/FeatureCards/FeatureCards.jsx
- /home/admin2/smy/upstream-materials/react-bits-main/src/components/landing/PlasmaWave/PlasmaWaveV2.jsx

执行原则：
- 优先复用这些材料中的成熟结构、节奏、布局和视觉语义。
- 对于 OGL / WebGL 等当前项目未引入的重依赖，不直接硬接，而是保留视觉语义，用轻量 CSS 方式承接。
- 不为了一点动效引入一整套不必要运行时依赖。

## 变更范围

### 首页
- 现有简单卡片首页升级为 Hero + 指标卡片 + 行动区三段式结构。
- 保留“开始创作”主按钮。
- 引入基于 react-bits Hero 语义的渐变光晕、标签徽标、主副标题节奏。
- 引入基于 react-bits FeatureCards 语义的 bento 风格信息卡。

### 结果页
- 保留现有数据结构与导出能力。
- 优化左侧分析面板与右侧结果区的卡片层级。
- 强化总览层、脚本层、平台层的标题、标签和段落可读性。
- 不改动 result API 契约，不改动导出链路。

## 当前阶段明确不做
- 不引入新的前端运行时依赖。
- 不接入完整 PlasmaWave WebGL 组件。
- 不改变既有主链路逻辑与接口。
- 不做第二套结果展示真值。

## 验证要求
- 前端页面文件和样式文件完成后，至少进行一次静态结构自检。
- docs、代码、changelog 和 git commit 必须保持同批次一致。
