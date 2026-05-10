# M39 Instructor 化 Narrative Bundle PoC 方案

## 1. 文档定位

本文档用于锁定 `P1` 第二项具体实施内容：

> 用成熟仓库 `instructor-ai/instructor` 替换当前 `narrative_generator` 中以仓内模板为主的脚本骨架生成路径，
> 让标题、摘要、脚本段落、关键镜头、备选标题与钩子优先走结构化输出主路径，
> 当前仓库只保留 schema、prompt glue、回退与结果映射。

本文档受以下事实源约束：
- `docs/PRD.md`
- `docs/stage_records/stage_01_project_handoff_summary_v1.md`
- `docs/stage_records/stage_02_project_handoff_summary_v2.md`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
- `docs/architecture/m38_instructor_profile_parser_poc.md`
- `docs/research/p0_strict_glue_repo_selection_v1.md`
- `docs/changelog.md`

---

## 2. 当前问题

当前 `backend/app/services/narrative_generator/service.py` 的主要偏差是：
- `segments` 由仓内固定四段模板直接生成
- `key_shots` 由仓内固定三段模板直接生成
- 模型目前只影响标题和摘要

这意味着：
- 生成结果虽然有结构，但仍主要是本地拼装
- 关键叙事骨架并未真正站在成熟结构化输出仓库之上
- 与当前项目的强胶水编程路线仍不一致

---

## 3. 上游仓库与准入结论

### 3.1 主仓库

- 仓库：`instructor-ai/instructor`
- 本地路径：`/home/admin2/smy/upstream-materials/instructor`
- 固定版本：`41f050c7`
- 许可证：MIT

### 3.2 选择原因

本轮继续选择 `Instructor` 的原因是：
- 已在 M38 中完成本地准入验证
- 直接支持 `LiteLLM`
- 天然适配当前项目已存在的 Pydantic schema
- 能把“标题、摘要、脚本段落、关键镜头、备选项”统一成单次结构化输出，而不是再写本地拼装逻辑

---

## 4. 本轮目标

本轮目标是把 `narrative_generator` 从“模板主路径”改为“成熟结构化输出主路径”：

1. 以新的结构化 schema 承接 `narrative bundle`
2. 优先使用 `Instructor + LiteLLM` 生成：
   - `main_title`
   - `one_sentence_summary`
   - `segments`
   - `key_shots`
   - `title_alternatives`
   - `hook_alternatives`
3. 失败时保留当前最小模板回退，确保主链不失效
4. 现有 orchestrator 与 package assembler 调用方式尽量保持不变

---

## 5. 接入边界

### 5.1 本仓允许保留的内容

- `ScriptSegment / KeyShot` 以及新的结构化 bundle schema
- prompt 组织
- 上游客户端初始化
- 失败兜底回退
- 输出结果到 `package_assembler` 的最小映射

### 5.2 本仓不允许继续扩大的内容

- 不继续扩写更多固定四段脚本模板
- 不继续扩写更多固定镜头模板
- 不继续自写结构化 JSON 解析、字段校验与重试

---

## 6. 技术方案

### 6.1 主路径

`NarrativeGeneratorService` 将优先：

1. 使用 `Instructor.from_litellm()`
2. 以新的 `StructuredNarrativeBundle` schema 作为 `response_model`
3. 将 `request / audience_profile / style_profile / trend_summary` 全部作为 prompt 上下文
4. 直接让成熟库输出完整结构化脚本骨架

### 6.2 回退路径

以下情况允许回退到当前模板逻辑：
- `instructor` 当前环境不可用
- `litellm` 不可用
- 模型调用失败
- 结构化结果校验失败

回退原则：
- 仅保留系统可用性所需最小模板
- 不再继续扩展模板复杂度

---

## 7. 验证口径

本轮完成后至少需要满足：

1. 有专项测试覆盖 `Instructor` 主路径
2. 有专项测试覆盖主路径失败后的回退
3. 现有 `test_m29_model_first_narrative.py` 迁移或更新后仍能表达“主路径优先、回退兜底”
4. 现有 orchestrator 相关测试不被破坏

建议验证命令：
- `python3 -m py_compile backend/app/services/narrative_generator/service.py backend/app/schemas/narrative_generation.py backend/tests/test_m39_instructor_narrative_bundle.py`
- `pytest -q backend/tests/test_m39_instructor_narrative_bundle.py backend/tests/test_m35_generation_orchestrator.py`

---

## 8. 完成标准

本轮完成标准定义为：
- `narrative_generator` 主路径已经切换到 `Instructor`
- `segments / key_shots` 不再默认由仓内模板直接主导
- tests 通过
- `docs/changelog.md` 已追加记录
- 有独立 Git 提交与本批变更对应
