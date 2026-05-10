# Backend

后端采用 FastAPI，负责：
- 输入归一化
- 标签抽取
- 趋势策略读取
- 叙事生成
- 结果包组装
- 导出与 payload 派生

## 当前阶段

当前已完成：
- 输入归一化与枚举校验
- `generate / status / result / export/json / export/md / video-payload` 主链路联通
- `profile_parser`、`trend_strategy`、`narrative_generator`、`package_assembler`、`export_payload` MVP 实现
- 趋势模板数据库真值层与趋势刷新入口
- LiteLLM 模型网关与模型失败回退
- `generation_jobs` 状态持久化与 `generation_results` 结果持久化
- Alembic 初始 migration、旧库补表兼容路径与启动阶段 migration/bootstrap 衔接
- 启动阶段数据库 bootstrap 重试与旧库补表回归

当前仍待深化：
- 多 revision 演进、团队级 migration 评审与治理规范
- 更完整的 provider 级错误分类、超时与重试治理
- 趋势采集从受控真实化走向可持续线上抓取

## 本地启动

1. 复制 `backend/.env.example` 为 `backend/.env`。
2. 创建虚拟环境并安装依赖：
   - `python3 -m venv backend/.venv`
   - `source backend/.venv/bin/activate`
   - `pip install -e backend[dev]`
3. 启动服务：
   - `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
4. 运行后端测试：
   - `./scripts/backend_test.sh`
   - 或 `./scripts/backend_test.sh tests/test_m41_internal_trend_api.py`
5. 运行演示回归主入口：
   - `./scripts/demo_regression.sh`
6. 若需要页面级闭环回归：
   - `cd frontend && npm run test:e2e`

补充说明：
- 应用启动时会自动执行 `bootstrap_database()`，优先走 Alembic migration，再做有限兼容修复与 seed。
- 默认示例配置已开启 `GENERATION_AUTO_START_ENABLED=true`，创建任务后会立即进入后台生成主链；若手动关闭，应预期 `/generate` 返回 `503`，而不是进入一个无法完成的假进度页。
- 若需要启用 diagnostics 或趋势刷新接口，需要在 `backend/.env` 中提供 `INTERNAL_API_KEY`。
- 若需要真实模型调用，需要额外提供对应 provider 所需环境变量，例如 `OPENAI_API_KEY`。
- 后端测试默认建议通过项目根目录的 `scripts/backend_test.sh` 运行，而不是直接使用宿主环境中的 `pytest`。
- 若要做演示前总体验证，优先运行项目根目录的 `scripts/demo_regression.sh`，它会串起后端关键回归、前端构建与 Playwright E2E。
- 若直接使用宿主 Python，可能遇到数据库驱动缺失、pytest 插件干扰或第三方依赖版本漂移问题；这类问题应优先视为环境隔离不足，而不是业务代码回归。
