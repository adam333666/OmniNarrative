# Frontend

前端采用 Next.js，负责：
- 首页展示
- 五步输入向导
- 生成状态展示
- 结果页展示
- 导出触发

## 视觉策略

前端视觉优先使用三类成熟能力：
- `shadcn/ui`：基础组件
- `react-bits`：动效与背景强化
- 本地参考仓库 `taxonomy`：页面结构与信息密度控制

## 当前阶段

当前已完成：
- 首页、输入页、生成页、结果页四页展示闭环
- 五步输入向导与后端 `generate` 接口联通
- 生成状态轮询与完成后自动跳转结果页
- 结果页真实结果结构、趋势来源轨迹与导出消费预览接入
- JSON / Markdown / Video payload 导出入口接入
- 首页品牌入口、创建页趋势预览、生成页阶段解释、结果页重型工作台与内部控制台入口均已完成

当前仍待深化：
- 更细的视觉与交互 polish
- 移动端与内容密度的继续打磨

## 本地启动

1. 复制 `frontend/.env.local.example` 为 `frontend/.env.local`。
2. 安装依赖：`cd frontend && npm install`
3. 启动开发服务器：`npm run dev`
4. 页面级闭环验证：`npm run test:e2e`
5. 演示前统一验证：`cd .. && ./scripts/demo_regression.sh`

默认前端会通过 `NEXT_PUBLIC_API_BASE_URL` 指向后端 `http://127.0.0.1:8000/api/v1`。
