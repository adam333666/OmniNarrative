# M3 最小结果链路契约

## 1. 文档目标

本文件用于锁定 `M3 最小结果链路` 的统一结果结构、`result` 接口行为以及结果页最小展示约束。

本阶段覆盖：
- `GET /api/v1/creations/{generation_id}/result`
- 最小 `AudienceProfile`
- 最小 `StyleProfile`
- 最小 `PlatformTrendTemplate`
- 最小 `NarrativePackage`
- 结果页左侧分析区与右侧三层展示区

---

## 2. 结果接口约束

### 2.1 `GET /api/v1/creations/{generation_id}/result`

用途：返回当前 `generation_id` 的统一结果包。

行为约束：
- 若 `generation_id` 不存在，返回 `404`。
- 若生成状态仍早于 `PACKAGE_ASSEMBLING`，返回 `409`。
- 若生成状态已进入 `PACKAGE_ASSEMBLING`，接口可以触发最终结果物化，并在返回统一结果结构的同时把任务收口为 `DONE`。
- 若生成状态已 `DONE`，直接返回统一结果结构。
- 返回结构必须同时包含：
  - `request_summary`
  - `analysis`
  - `result_package`
  - `export_meta`

---

## 3. 顶层结构

```json
{
  "request_summary": {},
  "analysis": {},
  "result_package": {},
  "export_meta": {}
}
```

### 3.1 `request_summary`

必须包含：
- `theme_text`
- `content_type`
- `target_platform`
- `target_audience_text`
- `style_tone`
- `custom_style_text`

### 3.2 `analysis`

必须包含：
- `audience_profile`
- `style_profile`
- `trend_summary`
- `key_design_decisions`

### 3.3 `result_package`

必须包含：
- `overview`
- `script_layer`
- `multimodal_layer`
- `platform_layer`
- `machine_payload_layer`

### 3.4 `export_meta`

必须包含：
- `schema_version`
- `generation_id`
- `generated_at`

---

## 4. 最小结构定义

### 4.1 `audience_profile`

必须包含：
- `raw_text`
- `age_group_guess`
- `interest_tags`
- `pain_points`
- `content_preference`
- `emotion_preference`

### 4.2 `style_profile`

必须包含：
- `style_label`
- `emotion_label`
- `intensity_level`
- `custom_notes`

### 4.3 `trend_summary`

必须包含：
- `platform`
- `summary`
- `hook_patterns`
- `rhythm_patterns`
- `title_cover_style`
- `audience_preference_summary`
- `avoid_patterns`
- `hot_topics_summary`

### 4.4 `overview`

必须包含：
- `main_title`
- `one_sentence_summary`
- `content_positioning`
- `target_platform`
- `target_audience_summary`
- `style_summary`
- `design_summary`

### 4.5 `script_layer`

必须包含：
- `segments`
- `key_shots`
- `script_note`
- `title_alternatives`
- `hook_alternatives`
- `title_candidates`
- `hook_candidates`

每个 `segment` 必须包含：
- `segment_number`
- `segment_title`
- `segment_goal`
- `narration`
- `subtitle_text`
- `visual_description`
- `emotion`
- `rhythm`

每个 `key_shot` 在当前阶段至少应支持：
- `shot_title`
- `shot_focus`
- `shot_duration_seconds`
- `transition_hint`
- `camera_movement`
- `transition_style`
- `asset_dependency`
- `voiceover_cue`

每个 `storyboard_frame` 在当前阶段至少应支持：
- `beat_number`
- `beat_title`
- `linked_segment_number`
- `linked_key_shot_title`
- `visual_focus`
- `narration_focus`
- `estimated_duration_seconds`
- `asset_requirement`
- `editing_note`

每个 `*_candidate` 在当前阶段至少应支持：
- `candidate_text`
- `usage_scenario`
- `design_reason`

### 4.6 `platform_layer`

必须包含：
- `platform_strategy`
- `trend_summary`
- `audience_adaptation`
- `hook_design_reason`
- `rhythm_structure_reason`
- `title_cover_style`
- `publishing_copy_suggestion`
- `avoid_patterns`
- `cover_copy_alternatives`
- `distribution_angles`
- `thumbnail_copy_candidates`
- `cover_candidates`
- `distribution_angle_candidates`

### 4.7 `machine_payload_layer`

当前阶段在既有字段基础上，必须继续承接以下执行级字段：
- `storyboard_beats`
- `storyboard_frames`
- `asset_preparation_notes`
- `voiceover_subtitle_alignment`

其中：
- `asset_preparation_notes` 允许从字符串列表升级为带 `linked_beat_number` 的结构化准备项列表
- `voiceover_subtitle_alignment` 允许从字符串列表升级为带 `linked_beat_number` 的结构化对齐项列表

---

## 5. 结果页展示约束

### 左侧区域必须展示
- 输入摘要
- 受众标签抽取结果
- 平台趋势摘要
- 关键设计决策说明

### 右侧区域在 M3 必须展示
- 项目总览层
- 叙事脚本层
- 平台适配层

### 右侧区域在 M3 可以先折叠展示
- 多模态生成层
- 机器可执行提示层

---

## 6. 当前阶段允许的简化

- `profile_parser` 可以先基于规则与轻量逻辑输出结构化标签。
- `trend_strategy` 可以先从内置默认模板读取，而不是数据库真实查询。
- `narrative_generator` 可以先使用结构化模板生成稳定结果，而不是接入真实模型。
- `package_assembler` 优先保证结构完整、字段清晰、层间一致。
- 结构化候选层允许由统一 schema 生成后，再同步派生旧版字符串数组用于兼容消费端。

前提是：
- 结果必须是结构化对象，不允许用一段大文本冒充。
- 平台适配层必须有真实策略字段，不能写成空泛文案。
