# M2 输入与状态主链路 API 契约

## 1. 文档目标

本文件用于锁定 `M2 输入与状态主链路` 的接口契约、前后端交互约束和最小行为预期。

本阶段只覆盖：
- `input-options`
- `generate`
- `status`

不覆盖：
- `result`
- `export`
- `video-payload`
- 内部趋势刷新接口

---

## 2. 前端交互约束

- 输入流程为五步顺序式，不允许跳步回退。
- 当前步未通过校验，不允许进入下一步。
- 所有输入在前端先经过 schema 校验，再发送到后端。
- 提交成功后，前端必须跳转到生成状态页。
- 生成状态页必须轮询 `status` 接口，并展示五个阶段消息。
- 状态为 `DONE` 后，前端跳转结果页。
- 状态为 `FAILED` 或 `TIMEOUT` 后，前端停止轮询并展示错误提示。

---

## 3. 接口定义

### 3.1 `GET /api/v1/config/input-options`

用途：获取前端五步向导使用的枚举和示例提示。

响应示例：

```json
{
  "content_types": [
    { "value": "science_popularization", "label": "科普型" },
    { "value": "story", "label": "故事型" },
    { "value": "mixed", "label": "混合型" },
    { "value": "auto", "label": "自动判断" }
  ],
  "platforms": [
    { "value": "douyin", "label": "抖音" },
    { "value": "kuaishou", "label": "快手" },
    { "value": "xiaohongshu", "label": "小红书" },
    { "value": "bilibili", "label": "B站" },
    { "value": "wechat_video", "label": "视频号" }
  ],
  "style_tones": [
    { "value": "suspense", "label": "悬疑" },
    { "value": "healing", "label": "治愈" }
  ],
  "example_prompts": [
    "我想做一个关于时间旅行悖论的内容",
    "我想做一个关于高三学生焦虑的内容",
    "我想做一个讲猫为什么会踩奶的内容"
  ]
}
```

### 3.2 `POST /api/v1/creations/generate`

用途：提交一次创作请求，生成 `generation_id` 并启动阶段式处理。

请求体：

```json
{
  "theme_text": "我想做一个关于时间旅行悖论的内容",
  "content_type": "science_popularization",
  "target_platform": "bilibili",
  "target_audience_text": "喜欢脑洞和科学设定的大学生与年轻上班族",
  "style_tone": "mysterious",
  "custom_style_text": "有一点哲学感，但不要太晦涩"
}
```

响应体：

```json
{
  "generation_id": "gen_xxxxx",
  "current_status": "THEME_PARSING",
  "created_at": "2026-03-25T00:00:00Z"
}
```

### 3.3 `GET /api/v1/creations/{generation_id}/status`

用途：返回当前生成阶段。

响应体：

```json
{
  "generation_id": "gen_xxxxx",
  "status": "PROFILE_PARSING",
  "current_stage": "PROFILE_PARSING",
  "stage_message": "正在抽取受众与风格标签",
  "error_message": null,
  "created_at": "2026-03-25T00:00:00Z",
  "updated_at": "2026-03-25T00:00:02Z",
  "completed_at": null,
  "total_elapsed_seconds": 2,
  "stage_elapsed_seconds": 0
}
```

---

## 4. 状态推进约束

M2 阶段允许使用最小内存态阶段推进机制，以打通展示链路。

状态必须覆盖：
- `THEME_PARSING`
- `PROFILE_PARSING`
- `TREND_ADAPTING`
- `NARRATIVE_GENERATING`
- `PACKAGE_ASSEMBLING`
- `DONE`
- `FAILED`
- `TIMEOUT`

对应文案必须覆盖：
- 正在解析创作主题
- 正在抽取受众与风格标签
- 正在进行平台与趋势适配
- 正在生成叙事骨架
- 正在组装多模态内容包

补充约束：
- `status` 与 `current_stage` 当前保持一致，均反映数据库真值层中的当前阶段。
- `created_at / updated_at / completed_at` 为状态诊断字段，用于支持当前阶段的排障与耗时展示。
- `total_elapsed_seconds / stage_elapsed_seconds` 为派生诊断字段，不改变任务主状态语义。
- 后台执行相关事件会进入内部 diagnostics 事件流，但不会改变 `status` 接口的主状态字段集合。

---

## 5. 数据校验规则

### 5.1 前端校验

- `theme_text` 必填，长度 1-500。
- `content_type` 必填，且必须是约定枚举之一。
- `target_platform` 必填，且必须是约定枚举之一。
- `target_audience_text` 必填，长度 1-500。
- `style_tone` 必填，且必须是约定枚举之一。
- `custom_style_text` 可选，长度不超过 300。

### 5.2 后端校验

- 后端必须重复执行同等约束，不能只依赖前端。
- 枚举非法时返回 422。
- 缺失必填项时返回 422。

---

## 6. 当前阶段边界

- 本阶段的 `generate` 与 `status` 以主链路联通为目标，不以最终内容质量为目标。
- 当前 `generation_id` 已持久化到数据库真值层，不再只存在于当前进程内存中。
- 后续结果链已经在 `M3/M4` 接入；本文件只聚焦输入与状态接口，不再描述结果接口行为。
