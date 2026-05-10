# M57 结果包重型化与执行蓝图展示

## 1. 背景

当前系统的结果包已经具备五层结构和基础导出能力，但用户在结果页上看到的仍主要是中等重量的创作方案。对于演示和答辩场景，这还不够突出“系统能生成接近可交付成品”的核心卖点。

与此同时，`package_assembler` 已经切到了 `Instructor + Pydantic schema` 主路径，因此当前更合适的深化方向不是回退到仓内手写模板，而是继续沿着成熟结构化输出主路径，把结果包加厚一层。

## 2. 本轮目标

本轮目标是把结果包从“结构完整”推进到“更重、更可执行、更适合直接展示”：

- 在 `StructuredPackageScaffold` 中补充更多下游可执行字段
- 让 `Instructor` 主路径优先生成这些字段，fallback 只做最小兜底
- 将新字段同步消费到结果页和 Markdown 导出

## 3. 具体实现

### 3.1 结果包 schema 加厚

新增以下结构化字段：

- `multimodal_layer.scene_progression`
- `multimodal_layer.motion_cues`
- `multimodal_layer.asset_props`
- `platform_layer.comment_guidance`
- `platform_layer.publish_timing_suggestions`
- `machine_payload_layer.thumbnail_prompt_block`
- `machine_payload_layer.voiceover_prompt_block`
- `machine_payload_layer.asset_checklist`

### 3.2 结果页新增“制作执行蓝图”

结果页新增一块更面向演示和交付的内容区，集中展示：

- 场景推进
- 镜头运动提示
- 发布时间建议
- 评论区引导
- 素材与道具
- 缩略图提示 / 配音提示 / 素材清单

### 3.3 Markdown 导出同步增强

Markdown 导出新增“制作执行蓝图”章节，确保导出物也能体现这一轮加厚结果，而不是只有前端页面能看到。

## 4. 验证方式

- 后端测试：
  - `tests/test_m46_instructor_package_assembler.py`
  - `tests/test_m46_export_payload_compat.py`
- 前端验证：
  - `cd frontend && npm run build`

## 5. 预期收益

- 更贴近 PRD 里“极其详细、极其重”的结构化成品方向
- 结果页更适合演示、答辩和直接向非技术角色说明价值
- 继续坚持强胶水编程原则，核心内容加厚依旧站在 `Instructor` 结构化输出主路径上，而不是回退到仓内手写大模板
