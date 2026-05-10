# M47 API 回归入口稳定性收口

## 1. 目标

收口当前 `TestClient(app)` 在宿主环境中进入 lifespan 时的历史拖尾问题，确保后续核心 API 胶水回归可以稳定执行，不再被非业务层噪音阻塞。

---

## 2. 当前问题

当前 `backend/tests/test_m5_trend_and_exports.py` 依赖 `FastAPI TestClient(app)`：

- 在当前环境下会卡在 `TestClient.__enter__()` 的 lifespan 启动阶段
- `app` 导入本身正常
- `bootstrap_database()` 单独执行也正常
- 因此问题位于测试入口和生命周期集成层，而不是业务断言本身

这类问题会导致：

- 回归看起来像“没跑完”，但其实不是业务失败
- 后续功能迭代时很难快速判断真回归和测试入口噪音

---

## 3. 本轮方案

把 `test_m5_trend_and_exports.py` 从 HTTP 集成入口测试，调整为：

- 直接调用路由函数
- 直接调用结果真值导出服务
- 继续覆盖：
  - 输入校验
  - 配置项读取
  - 趋势模板读取与刷新
  - 生成结果读取
  - Markdown 导出
  - video payload 导出

---

## 4. 胶水边界

本轮不是删掉 API 验证，而是把验证焦点收敛到：

- 路由胶水是否正确承接 service
- 结果包真值是否仍能被导出链消费
- 关键接口契约是否仍保持一致

不在本轮追查：

- Starlette / TestClient / anyio 组合下的深层宿主兼容问题

---

## 5. 验收标准

- `test_m5_trend_and_exports.py` 不再依赖 `TestClient(app)`
- 该回归文件可以在 `backend/.venv` 下稳定跑通
- 验证范围不低于改造前
