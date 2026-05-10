# M46 结果包组装结构化深化

## 1. 目标

把 `package_assembler` 从“仓内大量 dict 硬编码拼装”升级为：

- 上游 `narrative_generator` 继续产出脚本层真值
- `Instructor + LiteLLM + Pydantic schema` 负责组装其余结果包层
- 本仓只保留脚本层承接、提示词组装、fallback 与落库胶水

这样可以在不扰动当前脚本真值链的前提下，降低结果包其余层对仓内模板硬编码的依赖。

---

## 2. 当前问题

当前 `backend/app/services/package_assembler/service.py` 虽然能稳定输出五层结果包，但：

- `overview / multimodal_layer / platform_layer / machine_payload_layer` 主要由仓内 dict 直接拼装
- 关键设计决策说明也是本地固定文案
- 结果包结构虽然完整，但“解释性、平台适配性、下游可执行性”仍偏模板化

这与“关键业务能力优先站在成熟仓库之上”的目标不完全一致。

---

## 3. 本轮方案

### 3.1 主路径

新增结果包分层 schema，并用 `Instructor` 直接输出：

- `overview`
- `multimodal_layer`
- `platform_layer`
- `machine_payload_layer`
- `key_design_decisions`

`script_layer` 继续直接承接上游 `narrative_generator` 的真值，不在本轮重新生成。

### 3.2 胶水边界

本仓允许保留：

- 脚本层真值承接
- prompt 组装
- 结构化输出校验
- fallback 拼装
- 结果包落库与导出映射

### 3.3 本轮明确不做

- 不重新生成脚本层
- 不引入第二套手写结果包模板系统
- 不改变现有 `result / export / video-payload` 对结果包真值的消费边界

---

## 4. 验收标准

- `package_assembler` 主路径优先走 `Instructor` 结构化组装
- `script_layer` 仍以上游真值为准
- `Instructor` 不可用时仍能回退到现有最小结构化结果包
- 至少有单测覆盖结构化主路径与 fallback 路径
