# M27 后端阶段 B：趋势采集链落地

## 目标

把当前“模板重写式刷新”升级成可插入真实抓取器的趋势采集链，同时在当前环境缺少 `crawl4ai` 运行包时保留显式回退路径。

本阶段目标：
- 建立白名单来源配置、抓取器适配层、归纳器与刷新编排服务。
- 让 `trend_refresh` 不再直接调用 `build_refreshed_templates()`，而是优先走采集链。
- 当前环境若缺少 `crawl4ai` 运行依赖，必须明确进入 fallback，而不是伪装成真实抓取成功。
- 保持 `GET /config/trend-templates` 与 `POST /config/trend-refresh` 外部契约稳定。

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/upstream-materials/crawl4ai/tests/test_prefetch_regression.py`
- `/home/admin2/smy/upstream-materials/crawl4ai`
- `/home/admin2/smy/upstream-materials/httpx`

## 适配原则

- 当前阶段重点是把“真实采集链的工程接入点”落地，而不是在没有依赖和网络保证的情况下伪造外网抓取能力。
- `Crawl4AI` 适配层只放在 `integrations/crawler/`，业务 service 不直接 import 第三方包。
- 采集失败或依赖缺失时，必须通过回退模板继续返回可用结果，并记录来源类型。
- 白名单来源和归纳规则先小而硬，不做开放式深爬。

## 变更范围

### 后端服务
- 新增趋势来源白名单。
- 新增 `crawl4ai` 适配层。
- 新增趋势采集与归纳服务。
- 调整趋势刷新逻辑，优先走采集链。

### 测试
- 新增采集链的回退测试。
- 新增使用 fake collector 的刷新测试。

## 当前阶段明确不做

- 不要求当前环境已经安装好 `crawl4ai`。
- 不做实时趋势参与每次生成。
- 不做开放式站点发现。

## 2026-03-27 采集治理补充

当前采集链已补入两条关键保护：
- 文档质量闸门：过短、不可用或异常来源文档不会被视为成功采集结果。
- fallback 不写库：当本轮刷新整体落入 `manual_refresh_fallback` 时，接口仍返回现有数据库真值，不会被默认模板覆盖。

当前仍保持的边界：
- 允许“部分来源成功、部分来源失败”，只把通过质量闸门的平台写入刷新结果。
- 未通过质量闸门的平台继续保留原有模板级摘要。

## 验证要求

- `python3 -m py_compile` 通过。
- 后端测试通过，至少覆盖：现有趋势刷新回归、fake collector 刷新、依赖缺失 fallback、部分来源成功、fallback 不污染数据库旧真值。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口。
