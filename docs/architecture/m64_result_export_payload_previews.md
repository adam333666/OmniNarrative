# M64 结果页导出载荷预览

## 1. 背景

当前结果页已经可以展示结果真值，也能下载导出文件，但用户仍然需要离开当前页面或手动打开导出链接，才能直观看到：

- `/export/json`
- `/video-payload`

到底长什么样。

## 2. 本轮目标

在不新增任何后端导出逻辑的前提下，直接把现有导出接口预览到结果页上：

- JSON 导出预览
- Video Payload 预览

## 3. 具体实现

本轮新增：

- `frontend/components/result/export-json-preview.tsx`
- `frontend/components/result/export-json-preview.module.css`

并扩展：

- `frontend/lib/api-client/backend.ts`
- `frontend/components/result/result-view-client.tsx`
- `frontend/components/result/result-view-client.module.css`

实现方式：

- 直接调用既有 `/export/json`
- 直接调用既有 `/video-payload`
- 使用现有 `PayloadFoldoutHeader` 和 `MachinePayloadSummary` 做摘要与原始 JSON 展示

## 4. 验证

- `cd frontend && npm run build`

## 5. 阶段意义

这轮对应总计划中的：

- `P0` 结果包继续重型化
- 同时服务前端展示完成度

本轮属于典型薄胶水实现：没有新增导出真值，没有新增后端接口，只是把既有导出链更完整地展示到结果页。
