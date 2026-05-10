# M88 N1 执行级结果包契约

## 1. 文档目标

本文件用于承接 `stage_04_v1_0_runnable_baseline_and_next_plan.md` 中 `N1` 的第一批具体落地约束。

本轮不是新增第六层结果包，而是在现有五层结构内继续把结果从“重型方案”推进到“更完整执行级”。

---

## 2. 本轮锁定范围

本轮必须同时完成以下三类增强：

1. 候选层结构化
2. 镜头执行字段加厚
3. 导出与结果页同步消费

本轮暂不进入：

- 趋势入口多源深化
- checkpoint / failure trace 深化
- 前端整体文案改写

---

## 3. 结构化候选约束

### 3.1 目标

以下原先主要以字符串数组存在的字段，需要同时具备“结构化候选层”：

- `script_layer.title_candidates`
- `script_layer.hook_candidates`
- `platform_layer.cover_candidates`
- `platform_layer.distribution_angle_candidates`

### 3.2 候选对象最小结构

每个候选对象至少必须包含：

- `candidate_text`
- `usage_scenario`
- `design_reason`

### 3.3 兼容约束

为了不打断现有消费链，本轮允许继续保留以下旧字段：

- `title_alternatives`
- `hook_alternatives`
- `cover_copy_alternatives`
- `distribution_angles`

但旧字段必须视为兼容派生层，不再是唯一表达。

---

## 4. 镜头执行字段约束

### 4.1 `key_shots`

每个关键镜头除了既有字段外，还必须支持：

- `camera_movement`
- `transition_style`
- `asset_dependency`
- `voiceover_cue`

### 4.2 执行承接目标

这些字段必须能够直接服务于：

- 分镜拆解
- 剪辑说明
- 素材准备
- 配音落点说明

---

## 5. 制作执行字段约束

在 `machine_payload_layer` 中，本轮至少新增：

- `storyboard_beats`
- `storyboard_frames`
- `asset_preparation_notes`
- `voiceover_subtitle_alignment`
- `estimated_total_duration_seconds`
- `runtime_pacing_notes`

含义约束：

- `storyboard_beats`：按镜头或画面节拍给出执行拆分
- `storyboard_frames`：以结构化分镜帧形式描述每一拍的画面焦点、旁白焦点、时长和素材要求
- `asset_preparation_notes`：列出需要提前准备的素材与道具说明
- `voiceover_subtitle_alignment`：明确旁白重点句与字幕呈现的对齐方式
- `estimated_total_duration_seconds`：给出当前执行包估算的总时长
- `runtime_pacing_notes`：说明当前内容在起势、解释、收束三个节奏段的控制要点

### 5.1 `storyboard_frames` 最小结构

每个结构化分镜帧至少必须包含：

- `beat_number`
- `beat_title`
- `linked_segment_number`
- `linked_key_shot_title`
- `visual_focus`
- `narration_focus`
- `estimated_duration_seconds`
- `asset_requirement`
- `editing_note`

绑定约束：

- 每个分镜帧必须显式指向一个 `segment_number`
- 若该拍对应关键镜头，则必须给出 `linked_key_shot_title`
- 结果页、Markdown、Video payload 都必须能看见这层绑定关系

### 5.2 `asset_preparation_notes` 结构化升级

当前从字符串清单继续升级为结构化准备项时，每项至少应支持：

- `item_name`
- `linked_beat_number`
- `requirement_detail`
- `ready_stage`

### 5.3 `voiceover_subtitle_alignment` 结构化升级

当前从字符串说明继续升级为结构化对齐项时，每项至少应支持：

- `linked_beat_number`
- `voiceover_line`
- `subtitle_line`
- `timing_note`

---

## 6. 导出与消费约束

### 6.1 JSON

- `/export/json` 必须直接承接全部新增字段

### 6.2 Markdown

- 必须可读地输出结构化候选层
- 必须输出新增镜头执行字段
- 必须输出新增制作执行字段

### 6.3 Video payload

- 必须承接新增镜头字段
- 必须承接 `storyboard_beats`
- 必须承接 `storyboard_frames`
- 必须承接 `asset_preparation_notes`
- 必须承接 `voiceover_subtitle_alignment`
- 必须承接 `estimated_total_duration_seconds`
- 必须承接 `runtime_pacing_notes`
- 必须承接结构化候选层，不能只保留旧版字符串数组

### 6.4 结果页

结果页本轮至少新增三类明显更细的执行级信息展示：

- 结构化候选卡片
- 关键镜头执行元信息
- 配音/字幕/素材准备对齐信息

---

## 7. 实现约束

- 优先通过统一 Pydantic schema 承接新增字段
- fallback 路径必须补齐同一批字段
- 不允许只在前端临时拼装“执行级内容”
- 不允许只改结果页而不改导出

---

## 8. 完成判定

若同时满足以下条件，则视为 `N1` 第一批落地完成：

1. 结果包中出现结构化候选层
2. `key_shots` 明显比 v1.0 基线更细
3. JSON / Markdown / Video payload 三种导出全部承接新增字段
4. 结果页可直接看见新增执行级字段
