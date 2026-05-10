# M4 导出与 Payload 契约

## 1. 文档目标

本文件用于锁定一期 `M4` 导出链路的接口、行为与结构约束。

本阶段覆盖：
- `GET /api/v1/creations/{generation_id}/export/json`
- `GET /api/v1/creations/{generation_id}/export/md`
- `GET /api/v1/creations/{generation_id}/video-payload`
- 结果页导出按钮区最小联通

---

## 2. 顶层原则

- JSON 是系统唯一真值导出格式。
- Markdown 必须从统一结果结构派生，不允许手写另一套独立内容。
- Video payload 必须从统一结果结构映射生成，不允许拼接一段无结构文本冒充 payload。
- 导出链路不得绕开 `result` 结构。

---

## 3. 接口定义

### 3.1 `GET /api/v1/creations/{generation_id}/export/json`

用途：返回与结果页一致的结构化 JSON。

行为约束：
- 若 `generation_id` 不存在，返回 `404`。
- 若生成状态仍早于 `PACKAGE_ASSEMBLING`，返回 `409`。
- 若生成状态已进入 `PACKAGE_ASSEMBLING`，接口可以触发最终结果物化，并返回与 `result` 一致的结构化 JSON。
- 返回内容与 `result` 接口结构一致。

### 3.2 `GET /api/v1/creations/{generation_id}/export/md`

用途：返回从结果结构渲染得到的 Markdown 文本。

行为约束：
- Markdown 派生应复用与 `result` 相同的最终物化逻辑，不得自行重算另一套结果。
- Markdown 必须至少包含：
  - 项目总览层
  - 叙事脚本层
  - 平台适配层
  - 中间分析摘要
- 不允许 Markdown 成为新的系统真值。

### 3.3 `GET /api/v1/creations/{generation_id}/video-payload`

用途：返回面向下游视频系统的结构化 payload。

行为约束：
- Video payload 的派生必须复用与 `result` 相同的最终物化逻辑，不得绕过统一结果真值。

最小字段必须包含：
- `video_meta`
- `segments`
- `shots`
- `characters`
- `scenes`
- `style_constraints`
- `subtitle_blocks`
- `audio_guides`
- `negative_constraints`
- `storyboard_beats`
- `storyboard_frames`
- `asset_preparation_notes`
- `voiceover_subtitle_alignment`
- `title_candidates`
- `hook_candidates`
- `cover_candidates`
- `distribution_angle_candidates`

其中 `storyboard_frames` 必须保留对 `segment_number / key_shot_title` 的绑定信息，不能在导出时丢失。
其中 `asset_preparation_notes / voiceover_subtitle_alignment` 若已升级为结构化列表，导出时也必须保留分镜帧绑定信息。

---

## 4. 结果页联动约束

- 结果页必须至少提供三个可触发动作：
  - 查看结构化结果
  - 导出 JSON
  - 导出 Markdown
- Video payload 可以先以可查看 JSON 的方式呈现，不要求立即下载文件。

---

## 5. 当前阶段允许的简化

- JSON 导出可以直接返回 `result` 同结构对象。
- Markdown 导出可以先由后端模板函数生成。
- Video payload 可以先聚焦于脚本数组、关键镜头、风格约束和字幕块。
- 但在 `N1` 第一批之后，Video payload 必须同步承接执行级候选层与制作对齐字段。
- 前端导出按钮可以先使用新窗口打开对应接口，而不是做复杂的下载管理。
