# M28 后端阶段 C：模型网关接入

## 目标

把 LiteLLM 接入为后端统一模型网关的真实入口，同时在当前环境缺少 `litellm` 运行包时保留显式回退路径。

本阶段目标：
- 建立 `integrations/llm/` 下的 LiteLLM 适配层。
- 建立 `services/model_gateway/` 下的统一业务 façade。
- 让模型调用的错误、依赖缺失与返回结构收敛在网关层，而不是散落在业务 service。
- 为下一阶段 `narrative_generator` 切换到模型主路径做好接入准备。

2026-03-27 补强后，当前阶段额外具备：
- provider 基础配置入口：`model_provider`、`model_name`、`model_timeout_seconds`、`model_max_retries`、`model_temperature`
- completion 超时、provider 异常、malformed response 的统一语义层
- fallback 原因与尝试次数透出，便于上游测试和诊断
- 网关内调用耗时与失败原因日志

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/upstream-materials/litellm/litellm/main.py`
- `/home/admin2/smy/upstream-materials/litellm/litellm/router.py`

## 适配原则

- 当前阶段重点是建立 LiteLLM 的业务接入边界，而不是立即让所有叙事生成都依赖外部模型。
- LiteLLM import 与调用只允许存在于 `integrations/llm/`，业务 service 只依赖 `model_gateway`。
- 当前环境若缺少 `litellm` 运行依赖，网关必须明确返回 fallback 信号，而不是抛出无上下文异常。
- 结果结构先以最小字段集为目标，不在本阶段直接替换现有叙事生成主路径。

## 变更范围

### 后端服务
- 新增 LiteLLM 适配层。
- 新增模型网关 service 与内部请求/响应 schema。
- 新增最小“叙事草案请求”与“模型回退”测试。

### 当前阶段明确不做
- 不在本阶段直接替换 `narrative_generator` 主路径。
- 不做复杂 provider router。
- 不引入真实外部模型依赖作为测试前提。

## 当前实现状态补充

当前 `model_gateway` 已满足：
- provider 未配置或配置不受支持时，直接返回 `provider_config_missing` fallback。
- LiteLLM 运行包缺失时，返回 `provider_unavailable` fallback。
- provider timeout 与一般 provider error 会在 `max_retries` 范围内重试。
- malformed response 视为不可恢复错误，只记录一次并直接 fallback。
- 成功与失败路径都带有 `attempt_count`，便于整链追踪。

## 验证要求

- `python3 -m py_compile` 通过。
- 后端测试通过，至少覆盖成功路径、依赖缺失 fallback、timeout retry、provider error、malformed response 与 provider config missing。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口。
