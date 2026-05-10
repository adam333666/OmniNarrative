# M26 后端阶段 A：数据库真值层接入

## 目标

把趋势模板真值从文件仓迁移到数据库默认读写路径，同时保持现有 `trend_strategy_service` 对外行为不变。

本阶段目标：
- 建立 SQLAlchemy session / model / repository 基础设施。
- 让 `platform_trend_templates` 进入数据库默认真值路径。
- 让现有 JSON 文件只承担 seed 输入角色，不再承担主运行真值。
- 保持 `GET /config/trend-templates` 与 `POST /config/trend-refresh` 的契约稳定。

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/upstream-materials/sqlalchemy`
- `/home/admin2/smy/upstream-materials/alembic`
- `/home/admin2/smy/upstream-materials/full-stack-fastapi-template/backend/app/core/db.py`
- `/home/admin2/smy/upstream-materials/full-stack-fastapi-template/backend/app/alembic/env.py`

## 适配原则

- 现阶段先把数据库真值层和 seed/bootstrap 走通，不同时展开完整 migration 体系的所有细节。
- repository 对外继续返回 `PlatformTrendTemplate` schema，不把 ORM 模型泄漏到 service 层。
- 文件 seed 只在数据库空仓时生效，不再作为运行期主读路径。
- 当前阶段允许 `create_all` 作为过渡 bootstrap 手段，但目录和模型组织必须按后续 Alembic 演进方式设计。

## 变更范围

### 后端基础设施
- 新增 `db/base.py`、`db/session.py`、`db/bootstrap.py`。
- 新增趋势模板 ORM 模型与数据库仓储。
- 调整趋势策略 repository，使其默认使用数据库真值层。

### 配置与启动
- 调整配置项，显式区分 `database_url` 与 `trend_templates_seed_path`。
- 在应用启动时执行最小数据库 bootstrap 和 seed。

### 测试
- 新增数据库 seed/bootstrap 基础测试。
- 让现有趋势模板与导出测试在 sqlite 测试数据库上继续通过。

## 当前阶段明确不做

- 不在本阶段引入完整 Alembic revision 文件集合。
- 不改动前端接口。
- 不改动趋势抓取和模型接入逻辑。

## 验证要求

- `python3 -m py_compile` 通过。
- 后端测试通过，至少包含现有趋势模板回归测试和新增数据库 bootstrap 测试。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口。
