# M43 前端错误信息透传与 Markdown 预览恢复

## 1. 文档定位

本文档用于补齐前端当前仍存在的一类体验问题：

> 当前 API client 在请求失败时大多直接抛固定文案，
> 导致后端已提供的 `detail`、状态语义和更具体错误原因没有传到界面；
> 同时 `MarkdownPreview` 错误态仍缺少显式重试入口。

本文档受以下事实源约束：
- `docs/PRD.md`
- `docs/stage_records/stage_02_project_handoff_summary_v2.md`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
- `docs/changelog.md`

---

## 2. 当前问题

当前 `frontend/lib/api-client/backend.ts` 的问题是：
- `submitCreationRequest / fetchGenerationStatus / fetchGenerationResult / fetchMarkdownExport` 在失败时大多只抛固定字符串
- 后端 `HTTPException.detail` 无法透传到前端

当前 `MarkdownPreview` 的问题是：
- 加载失败后只有错误文案，没有显式重试动作

---

## 3. 本轮目标

1. 为前端 API client 增加统一的错误规范化逻辑
2. 尽量透传后端返回的 `detail`
3. Markdown 预览增加“重新加载”动作
4. 不改动后端契约，只在前端做胶水收口

---

## 4. 技术方案

### 4.1 API client

- 增加 `readErrorMessage()` / `assertOk()` 一类统一辅助函数
- 若后端返回 JSON 且包含 `detail`，优先透传
- 否则回退到前端默认文案

### 4.2 MarkdownPreview

- 增加重试按钮
- 失败后允许手动重新拉取 Markdown

---

## 5. 验证口径

- 前端 `npm run build` 通过
- `docs/changelog.md` 已追加记录

---

## 6. 完成标准

- 后端具体错误信息能够更稳定地透传到前端
- Markdown 预览失败后可手动重试
- `npm run build` 通过
- 有对应 changelog 和 git 提交
