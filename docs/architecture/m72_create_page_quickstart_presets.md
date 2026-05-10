# M72 创建页 Quick Start 预设

## 1. 背景

系统第四核心点是“简单上手的操作逻辑”。  
当前创建页虽然已经有五步输入和示例提示，但第一次使用时仍然需要自己逐项构思和填写，启动成本还可以更低。

## 2. 本轮目标

- 让第一次进入创建页的用户可以一键套用完整配置
- 不只填一条主题，而是把平台、内容类型、受众、风格一起带入
- 继续复用已接入的上游 `CardSwap`

## 3. 方案

- 新增 `creation-preset-deck.tsx`
- 在创建页顶部展示 3 组完整预设
- 点击后直接写入 `theme_text / content_type / target_platform / target_audience_text / style_tone / custom_style_text`
- 保留原有五步输入链路，预设只是启动加速层

## 4. 变更范围

- `frontend/components/wizard/creation-preset-deck.tsx`
- `frontend/components/wizard/creation-preset-deck.module.css`
- `frontend/components/wizard/create-wizard.tsx`

## 5. 预期结果

- 创建页更容易上手，减少第一次使用时的构思成本
- “简单上手”这条核心卖点更具体、更可演示
- 本轮继续是“现有表单真值写入 + 已接入上游组件复用”的薄胶水实现
