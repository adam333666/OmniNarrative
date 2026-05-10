# M8 前端构建收尾方案

## 目标

在 M7 已完成真实依赖安装和 Next.js 构建通过的基础上，进一步消除当前前端构建过程中的环境级噪音，提升后续迭代的可重复性。

## 当前问题

`npm run build` 虽已通过，但 Next.js 仍提示：
- 检测到多个 lockfile
- 推断的 workspace root 可能不正确

该问题当前不阻塞构建，但会影响后续日志清晰度与环境确定性。

## 处理原则

- 优先使用 Next.js 官方建议的 `outputFileTracingRoot` 进行显式收敛。
- 不删除用户环境中的其他 lockfile。
- 不通过规避日志而掩盖真实问题，要让配置明确表达当前项目根。

## 变更范围

- 更新 `frontend/next.config.ts`
- 重新执行 `npm run build`
- 将验证结果回写 changelog

## 验证要求

- 构建应继续通过。
- 构建日志中不应再出现 workspace root 推断警告。
