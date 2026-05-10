# M48 结构化输出 Gateway 统一收口

## 1. 目标

把当前分散在多个 service 内部的 `Instructor + LiteLLM` 客户端创建、provider 判断、模型配置判断、重试参数传递与失败回退入口，统一收口到一个共享的结构化输出 gateway。

---

## 2. 当前问题

在 `M38 / M39 / M45 / M46` 之后，当前以下模块都已经直接接入 `Instructor`：

- `profile_parser`
- `narrative_generator`
- `trend_collector`
- `package_assembler`

但它们当前各自都在做一遍：

- `Instructor.from_litellm()` 初始化
- `provider_name / model_name / max_retries / temperature` 读取
- 失败时的 fallback 判断

这会导致：

- 结构化输出虽然已经走成熟库，但模型调用边界再次分散
- 与此前 `model_gateway` 统一 provider 边界的原则产生漂移
- 后续若继续深化 provider 治理，会在多个 service 中重复修改

---

## 3. 本轮方案

新增共享 `structured_output_gateway`：

- 统一负责 `Instructor + LiteLLM` 客户端初始化
- 统一负责 provider/model 可用性判断
- 统一执行结构化 `response_model` 调用
- 统一做日志与 `model_validate` 兜底

各业务 service 保留：

- prompt 组装
- fallback 内容构建
- 结果真值合并

也就是说：

- 结构化输出“怎么调模型”由 gateway 负责
- 结构化输出“业务上要抽什么”仍由各 service 自己负责

---

## 4. 验收标准

- `profile_parser / narrative_generator / trend_collector / package_assembler` 不再各自直接 `from_litellm()`
- 结构化输出调用统一走共享 gateway
- 现有主路径与 fallback 行为保持不变
- 至少补共享 gateway 单测和关键回归单测
