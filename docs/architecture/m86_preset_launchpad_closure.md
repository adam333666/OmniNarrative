# M86 首页预设发射台与创建页一键启动收口

## 本轮目标

把“简单上手”从创建页内部能力，推进成首页可直接触发的真实启动路径。

这轮不是继续补解释文案，而是让首页直接带着一组完整预设进入创建页，使首次使用者不用先理解所有字段，也能立刻启动一轮完整创作。

## 修改范围

- `frontend/lib/constants/creation-presets.ts`
- `frontend/components/wizard/creation-preset-deck.tsx`
- `frontend/components/wizard/create-wizard.tsx`
- `frontend/components/landing/quickstart-launchpad.tsx`
- `frontend/components/landing/quickstart-launchpad.module.css`
- `frontend/components/landing/creative-hero.tsx`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`

## 实现说明

### 1. 预设真值提取为共享常量

把创建页内部使用的三组预设抽到共享常量，避免首页和创建页各自维护一份同义但可能漂移的数据。

### 2. 首页新增预设发射台

首页新增 `Quickstart Launchpad`，直接展示三组典型预设，并通过 URL 参数把完整预设键带到创建页。

### 3. 创建页支持 URL 预设注入

创建页读取 `preset` 查询参数，只要命中共享预设表，就自动把主题、平台、内容类型、受众和风格一起写入表单。

这意味着“从首页一键开始”不再只是跳到创建页，而是已经带着一组可直接提交的起始配置进入主流程。

## 对应里程碑

- `M-P3-A 创建页与生成页足够易上手`

## 收口判断

本轮完成后，`M-P3-A` 的退出条件已经满足：

- 创建页可通过预设快速启动
- 生成页能明确解释系统在做什么
- 首页现在也能直接把完整预设带进创建页，首次启动成本进一步下降
