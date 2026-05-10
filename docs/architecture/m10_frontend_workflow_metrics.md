# M10 首页流程步进与指标组件增强

## 目标

在 `M9` 已接入 `ShinyText` 与 `SpotlightCard` 的基础上，继续从本地 `react-bits-main` 源码中借成熟组件语义，让首页同时具备：
- 更明确的主链路表达
- 更强的数值感知与节奏感
- 不引入新的重型运行时依赖

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/TextAnimations/CountUp/CountUp.tsx`
- `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/Components/Stepper/Stepper.tsx`

## 适配原则

- `CountUp`：保留“进入视口后开始递增”的数值感知语义，但不引入 `motion/react`，改用 `IntersectionObserver + requestAnimationFrame` 实现轻量等价效果。
- `Stepper`：保留“阶段指示器 + 当前步骤高亮 + 线性流程表达”的信息结构，但不引入原版的复杂翻页动画，只保留更适合首页的信息型步进条。
- 所有配色与层次继续服从当前项目的暖色系视觉系统，避免直接复制上游深色默认风格。

## 变更范围

### 首页指标区
- 将原有静态统计卡片升级为会在进入视口后递增的指标卡。
- 指标内容继续严格围绕当前产品真实主链路：五步输入、五层结果包、三类导出。

### 首页流程区
- 新增“创作主链路”可视化步进区。
- 使用轻量的阶段切换方式展示：输入、分析、叙事、结果、导出。
- 保持为展示型组件，不接入真实业务状态机。

## 当前阶段明确不做

- 不引入 `motion/react`。
- 不改写现有结果页与后端接口。
- 不做复杂拖拽、3D 或 WebGL 动效。

## 验证要求

- 变更后执行 `npm run build`。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口，保证 docs、代码、验证记录一致。
