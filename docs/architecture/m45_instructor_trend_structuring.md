# M45 趋势链结构化归纳深化

## 1. 目标

在不改动当前趋势采集入口白名单与 `Crawl4AI` 抓取边界的前提下，把 `trend_collector` 从“抓取后只拼接 72 字摘要”的轻量模式，升级为：

- `Crawl4AI` 负责页面抓取与 Markdown 清洗
- `Instructor + LiteLLM + Pydantic schema` 负责趋势文档结构化归纳
- 本仓只负责平台模板真值的最小合并、回退与落库胶水

本轮的目标不是新增更多平台规则，而是让现有趋势链具备更接近 PRD 预期的“外部状态趋势追踪 + 结构化可复用结果”。

---

## 2. 当前问题

当前 `backend/app/services/trend_collector/service.py` 已经具备：

- 白名单平台来源
- `Crawl4AI` 抓取能力
- 文档质量闸门
- 全局 fallback 保护

但抓取后的归纳仍主要依赖：

- 从 Markdown 中截取前 72 个字符
- 将截断摘要直接拼接到 `summary`
- 仅额外附加一个来源标题

这会导致：

- 抓到了页面，但没有真正抽出“平台钩子 / 节奏 / 封面风格 / 避免模式 / 热点话题”
- 趋势模板仍主要靠仓内 seed 与 appendix，而不是外部文档驱动
- 趋势链虽然“可刷新”，但“结构化外部趋势追踪”能力偏弱

---

## 3. 本轮方案

### 3.1 主路径

新增趋势结构化 schema，由 `Instructor` 直接输出：

- `summary`
- `hook_patterns`
- `rhythm_patterns`
- `title_cover_style`
- `audience_preference_summary`
- `avoid_patterns`
- `hot_topics_summary`

执行顺序：

1. `Crawl4AI` 抓取页面并输出 Markdown
2. `TrendCollectorService` 对文档做最小清洗
3. `Instructor` 基于平台、默认模板上下文和采集文档输出结构化趋势归纳
4. 本仓将结构化结果与默认模板做去重合并
5. 仅当结构化归纳不可用时，才回退到原有 excerpt 拼接逻辑

### 3.2 本仓允许保留的胶水内容

- 白名单来源定义
- 文档质量闸门
- prompt 组装
- 结构化结果与模板真值的合并规则
- 失败回退与 `manual_refresh_*` 语义保持

### 3.3 本轮明确不做

- 不直接并入 `RSSHub` 或 GPL/AGPL 风险仓库代码
- 不新增第二套趋势规则词典
- 不自己发明新的通用 crawler / feed parser
- 不把趋势归纳重新做成仓内长模板系统

---

## 4. 验收标准

- `trend_collector` 主路径优先走 `Instructor` 结构化归纳，而不是 excerpt 拼接
- 结构化归纳失败时，现有 fallback 仍可保活
- 至少有单测覆盖：
  - 结构化主路径成功
  - `Instructor` 不可用时回退 excerpt
  - 部分来源质量不足时不触发全局 fallback

---

## 5. 影响范围

- `backend/app/services/trend_collector/service.py`
- `backend/app/schemas/trend_template.py`
- `backend/tests/test_m27_trend_collection.py`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
- `docs/changelog.md`
