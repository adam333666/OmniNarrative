# M41 内部趋势 API 对齐方案

## 1. 文档定位

本文档用于锁定一个明确的 PRD 功能缺口修复：

> 按 PRD 对齐内部趋势接口边界，
> 将当前混在 `/api/v1/config/*` 下的内部趋势能力，补齐为独立的 `/internal/*` 命名空间，
> 同时新增 `GET /internal/trend-summary/{platform}`。

本文档受以下事实源约束：
- `docs/PRD.md`
- `docs/stage_records/stage_01_project_handoff_summary_v1.md`
- `docs/stage_records/stage_02_project_handoff_summary_v2.md`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
- `docs/changelog.md`

---

## 2. 当前问题

PRD 当前明确要求：
- `POST /internal/trend-refresh`
- `GET /internal/trend-summary/{platform}`

而当前代码只有：
- `GET /api/v1/config/trend-templates`
- `POST /api/v1/config/trend-refresh`

因此存在两个偏差：
- 内部接口没有真正独立到 `/internal/*`
- `trend-summary/{platform}` 能力缺失

---

## 3. 本轮目标

本轮目标是最小代价对齐 PRD：

1. 新增 `/internal/trend-refresh`
2. 新增 `/internal/trend-summary/{platform}`
3. 内部接口继续沿用现有 `X-Internal-Api-Key` 约束
4. 不删除现有 `/config/trend-refresh`，先保留兼容入口

---

## 4. 接入边界

本轮只做胶水对齐：
- 新增内部路由
- 抽取通用内部鉴权依赖
- 基于现有 `trend_strategy_service` 提供平台摘要查询

本轮不做：
- 趋势采集核心逻辑重写
- 趋势模板存储结构改造
- 管理后台页面开发

---

## 5. 技术方案

### 5.1 路由层

新增 `backend/app/api/routes/internal.py`：
- `POST /internal/trend-refresh`
- `GET /internal/trend-summary/{platform}`

### 5.2 鉴权层

在 `api/deps.py` 中新增内部鉴权依赖：
- 检查 `settings.internal_api_key`
- 校验 `X-Internal-Api-Key`

### 5.3 服务层

在 `trend_strategy_service` 中新增平台级摘要读取方法：
- 支持按平台读取最新趋势摘要
- 可选按 `content_type` 进一步筛选
- 若该平台无数据，则返回 404

---

## 6. 验证口径

本轮完成后至少需要满足：

1. 内部鉴权依赖有专项测试
2. `trend-summary/{platform}` 的服务层/路由层有专项测试
3. 不影响已有 `config/trend-refresh` 兼容入口

建议验证命令：
- `python3 -m py_compile backend/app/api/routes/internal.py backend/app/api/deps.py backend/app/services/trend_strategy/service.py`
- `pytest -q backend/tests/test_m41_internal_trend_api.py`

---

## 7. 完成标准

本轮完成标准定义为：
- PRD 中两条内部趋势接口均已存在
- 内部接口已独立成 `/internal/*` 命名空间
- tests 通过
- `docs/changelog.md` 已追加记录
- 有独立 Git 提交与本批变更对应
