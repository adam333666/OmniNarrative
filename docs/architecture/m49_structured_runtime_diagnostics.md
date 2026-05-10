# M49 结构化生成运行时诊断透出

## 1. 目标

把当前只存在于日志中的结构化生成主路径/回退路径信息，补充透出到结果真值的 `analysis` 中，便于前端展示、导出解释与后续 diagnostics 对齐。

---

## 2. 当前问题

当前系统虽然已经把画像抽取、叙事生成、趋势归纳、结果包组装切到结构化主路径，但：

- 用户最终拿到的 `result` 中并不知道叙事生成是否走了结构化主路径
- 也不知道结果包组装是否走了结构化主路径
- 这些事实大多只留在日志里，结果真值层缺少稳定可消费的解释

---

## 3. 本轮方案

### 3.1 先补最关键的两段

本轮先在 `analysis` 中增加：

- `runtime_diagnostics.narrative_generation`
- `runtime_diagnostics.package_assembly`

其中至少包含：

- `source_type`
- `fallback_reason`

### 3.2 不扩大本轮范围

本轮不改：

- diagnostics 数据库事件表结构
- 前端显示逻辑
- profile parser 的运行时元信息持久化

---

## 4. 验收标准

- `result.analysis` 中新增结构化运行时诊断信息
- 叙事生成走主路径与 fallback 路径时，都能在结果真值里区分
- 结果包组装走主路径与 fallback 路径时，都能在结果真值里区分
