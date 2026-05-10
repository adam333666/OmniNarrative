# M37 联调与环境收口

## 1. 目标

把当前仓库从“代码与测试可运行”继续收口到“新接手开发者可按文档完成环境准备、启动主链并执行最小 smoke 验证”。

本阶段对齐 `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md` 中：
- 阶段 L：前后端联调与运行脚本收口
- 阶段 M：部署与环境说明收口

## 2. 当前补齐内容

本阶段新增或补齐：
- 根目录 `.env.example`
- `backend/.env.example`
- `frontend/.env.local.example`
- `scripts/dev_bootstrap.sh`
- `scripts/smoke_test.sh`
- 根 `README.md` 与前后端 `README.md` 的启动说明
- `deploy/docker-compose.yml` 的环境变量外置入口
- `deploy/frontend.Dockerfile` 的依赖安装链与前端 `node_modules` 卷

## 3. 环境文件职责

### 3.1 根目录 `.env`

用途：
- 为 `docker compose -f deploy/docker-compose.yml up` 提供统一环境变量入口。

主要字段：
- `APP_ENV`
- `FRONTEND_PORT`
- `BACKEND_PORT`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `INTERNAL_API_KEY`
- `NEXT_PUBLIC_API_BASE_URL`
- `MODEL_PROVIDER`
- `MODEL_NAME`
- `MODEL_TIMEOUT_SECONDS`
- `MODEL_MAX_RETRIES`
- `MODEL_TEMPERATURE`
- `GENERATION_AUTO_START_ENABLED`
- `GENERATION_BACKGROUND_WORKERS`
- `OPENAI_API_KEY`

### 3.2 `backend/.env`

用途：
- 本地直接运行 FastAPI 时，由 `pydantic-settings` 自动加载。

原则：
- 仅承载后端运行所需配置。
- provider secret 只在真实模型链需要时填写。

### 3.3 `frontend/.env.local`

用途：
- 本地直接运行 Next.js 时指定后端 API 地址。

## 4. 脚本职责

### 4.1 `scripts/dev_bootstrap.sh`

职责：
- 安装前端依赖
- 创建后端虚拟环境
- 安装后端开发依赖
- 提示复制环境示例文件

边界：
- 不自动启动数据库或应用进程
- 不隐式改写用户现有 `.env`

### 4.2 `scripts/smoke_test.sh`

职责：
- 校验 `/health`
- 校验 `/config/input-options`
- 提交一次最小 `generate`
- 轮询 `status`
- 在进入 `PACKAGE_ASSEMBLING` 或 `DONE` 后验证 `result / export/json / export/md / video-payload`

边界：
- 只覆盖最小主链
- 不替代 pytest 回归

## 5. Docker Compose 收口原则

`deploy/docker-compose.yml` 当前改为支持环境变量覆盖，目标是：
- 允许不同开发者在不改 compose 文件的前提下调整端口和密钥
- 让 compose 与 `.env.example` 对齐
- 保持当前一期原型三服务边界不变：`frontend / backend / db`

补充约束：
- `NEXT_PUBLIC_API_BASE_URL` 是浏览器可见变量，因此 compose 默认值必须是宿主机可访问地址 `http://127.0.0.1:8000/api/v1`。
- 前端开发容器通过 `frontend_node_modules` 命名卷保留依赖，避免 bind mount 抹掉镜像内已安装的 `node_modules`。

## 6. 验收口径

完成标准：
- 新接手开发者可以直接从 example 文件复制得到本地环境模板
- 能通过 `scripts/dev_bootstrap.sh` 完成最小依赖准备
- 能通过 README 找到本地运行方式和 compose 运行方式
- 在服务已启动前提下，可以通过 `scripts/smoke_test.sh` 完成最小主链验证

## 7. 后续边界

本阶段仍未覆盖：
- 一键拉起全部本地进程的进程管理器
- 生产级部署编排
- 完整 CI smoke pipeline
- 真正外部 provider 凭证分发与 secrets 管理

这些内容仍属于后续更深一层的工程化工作，而不是当前一期原型收口范围。
