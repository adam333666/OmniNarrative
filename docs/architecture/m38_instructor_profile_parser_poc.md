# M38 Instructor 化 Profile Parser PoC 方案

## 1. 文档定位

本文档用于锁定 `P1` 第一项具体实施内容：

> 用成熟仓库 `instructor-ai/instructor` 替换当前仓内自写的 `profile_parser` 主路径，
> 让 `AudienceProfile / StyleProfile` 的抽取优先走成熟结构化输出链，
> 当前仓库只保留 schema、最小 prompt glue、失败回退与编排接入。

本文档受以下事实源约束：
- `docs/PRD.md`
- `docs/stage_records/stage_01_project_handoff_summary_v1.md`
- `docs/stage_records/stage_02_project_handoff_summary_v2.md`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
- `docs/research/p0_strict_glue_repo_selection_v1.md`
- `docs/changelog.md`

---

## 2. 当前问题

当前 `backend/app/services/profile_parser/service.py` 仍主要依赖仓内关键词规则：
- 受众画像由手写年龄、兴趣、痛点规则推断
- 风格画像由手写情绪映射和强度映射推断

这与当前项目已确认的强胶水编程原则不一致：
- 关键业务能力不应继续以仓内规则作为主实现
- 应优先复用成熟开源仓库的结构化输出能力
- 本仓应仅保留输入组织、结果映射、失败回退与编排接入

---

## 3. 上游仓库与准入结论

### 3.1 主仓库

- 仓库：`instructor-ai/instructor`
- 本地路径：`/home/admin2/smy/upstream-materials/instructor`
- 固定版本：`41f050c7`
- 许可证：MIT

### 3.2 选择原因

该仓库已经直接提供：
- 基于 Pydantic 的结构化输出
- 自动校验
- 自动重试
- 对 `LiteLLM` 的直接支持

这意味着当前项目可以直接复用其核心能力，而不是继续自写：
- JSON 解析
- schema 校验
- 回填重试逻辑
- provider 差异适配

### 3.3 本轮明确不做的事

本轮不引入新的仓内“智能解析规则增强”。
如果 `Instructor` 主路径不可用，只允许保留最小回退逻辑用于系统可用性兜底，不允许把回退逻辑继续发展成新的主实现。

---

## 4. 本轮目标

本轮目标是把 `profile_parser` 从“规则主路径”改为“成熟库主路径”：

1. `parse_audience_profile()` 优先通过 `Instructor + LiteLLM + AudienceProfile` 提取
2. `parse_style_profile()` 优先通过 `Instructor + LiteLLM + StyleProfile` 提取
3. 失败时保留最小 fallback，防止主链不可用
4. 生成编排层调用方式保持不变，避免一次性扩大改动面

---

## 5. 接入边界

### 5.1 本仓允许保留的内容

- `AudienceProfile / StyleProfile` schema
- 针对当前输入结构的 prompt 组织
- `Instructor` 客户端初始化
- 失败时的最小 fallback
- 与 orchestrator 的现有调用对接

### 5.2 本仓不允许继续扩大的内容

- 不继续手写更多关键词规则
- 不继续扩写更多风格映射表
- 不继续自写结构化 JSON 解析与验证重试

---

## 6. 技术方案

### 6.1 主路径

`ProfileParserService` 将优先：

1. 使用上游 `Instructor`
2. 通过 `from_litellm()` 复用当前项目已有的 `LiteLLM` 体系
3. 直接以 `AudienceProfile / StyleProfile` 作为 `response_model`
4. 让上游仓库负责结构化输出约束、校验与重试

这样做的原因是：
- 当前仓库已经使用 `litellm`
- `Instructor` 上游原生支持 `LiteLLM`
- 这能避免为接入 `Instructor` 再额外自造一层 OpenAI 风格客户端适配器

### 6.2 Prompt 设计

Prompt 只负责：
- 提供当前请求上下文
- 强调字段含义和约束
- 要求输出严格匹配 schema

Prompt 不负责：
- 用仓内规则硬编码答案
- 手工模拟外部结构化输出框架

### 6.3 回退策略

以下情况允许回退到最小规则逻辑：
- `instructor` 依赖当前环境不可用
- `litellm` 运行不可用
- 模型调用失败
- 模型返回无法通过 schema 校验

回退原则：
- 仅用于保活
- 保持当前最小可运行水平
- 后续阶段仍应继续压缩其存在感

---

## 7. 验证口径

本轮完成后至少需要满足：

1. 新增针对 `ProfileParserService` 的专项测试
2. 能验证主路径会调用 `Instructor` 客户端
3. 能验证主路径异常时会回退到最小规则逻辑
4. 现有 orchestrator 相关测试不被破坏

建议验证命令：
- `python3 -m py_compile backend/app/services/profile_parser/service.py backend/tests/test_m38_instructor_profile_parser.py`
- `pytest -q backend/tests/test_m38_instructor_profile_parser.py backend/tests/test_m35_generation_orchestrator.py`

---

## 8. 完成标准

本轮完成标准定义为：
- `profile_parser` 主路径已经切换到 `Instructor`
- 当前仓库未新增大块自写解析逻辑
- tests 通过
- `docs/changelog.md` 已追加记录
- 有独立 Git 提交与本批变更对应
