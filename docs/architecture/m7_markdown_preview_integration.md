# M7 Markdown 预览接入方案

## 目标

把一期已经存在的 Markdown 导出链路接回前端结果页，让用户无需离开结果页就能预览 Markdown 结果。

本阶段目标：
- 保持 Markdown 仍然由后端统一结果结构派生生成。
- 前端只负责安全渲染，不创造第二套 Markdown 真值。
- 接入 `react-markdown` 作为成熟渲染材料，而不是自写 Markdown 渲染逻辑。

## 原材料来源

本阶段直接参考本地上游源码材料：
- `/home/admin2/smy/upstream-materials/react-markdown/readme.md`
- `/home/admin2/smy/upstream-materials/react-markdown/index.js`
- `/home/admin2/smy/upstream-materials/react-markdown/lib/index.js`

执行原则：
- 按上游推荐方式直接使用默认导出的 `Markdown` 组件。
- 当前阶段不额外引入 GFM 插件，先保持最小安全渲染链路。
- 不把 Markdown 结果落成新的本地缓存真值。

## 变更范围

### 前端依赖
- 在 `frontend/package.json` 中声明 `react-markdown` 依赖。

### API 客户端
- 新增获取 Markdown 导出文本的方法。
- 继续复用既有 `/export/md` 接口，不新增额外后端接口。

### 结果页
- 增加 Markdown 预览区域。
- 采用懒加载式客户端获取，不影响当前 JSON 结果结构加载。
- 保留既有导出按钮，不替代导出动作。

## 当前阶段明确不做
- 不引入 remark-gfm、rehype 等额外插件。
- 不做 Markdown 编辑器。
- 不改动后端 Markdown 生成逻辑。

## 验证要求
- 代码静态检查需保证导入路径和类型结构一致。
- 若当前环境尚未安装前端依赖，需要如实记录未完成的运行时验证，不得伪造通过。
