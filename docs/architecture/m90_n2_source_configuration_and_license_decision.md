# M90 N2 来源配置显式化与许可证结论

## 1. 背景

`N2` 第一批已经把趋势链推进到：

- 同平台可合流 `RSSHub + Crawl4AI`
- 趋势模板新增互动模式、情绪切口、创作者角度

但当前仍有两个缺口：

1. 来源配置结构仍主要藏在后端常量和环境变量里，前台与内部控制台只能看到“用了哪些来源”，看不到“本来配置了哪些来源”
2. `bilibili-api-python` 仍停留在“研究候选”表述，没有在 `N2` 中形成正式去留结论

## 2. 本轮目标

本轮作为 `N2` 的第二批闭环，锁定两件事：

1. 把平台来源配置提升为可透传、可展示的结构化真值
2. 给 `bilibili-api-python` 输出正式许可证结论

## 3. 新增真值字段

在 `TrendTemplateSummary` 中新增：

- `configured_sources`

其中每个来源项至少包含：

- `source_kind`
- `display_name`
- `target`
- `enabled`
- `status`
- `rationale`

## 4. 来源配置约束

### 4.1 显式化展示

内部趋势控制台和趋势摘要接口不只展示“最终采集轨迹”，还必须展示：

- 当前平台有哪些已配置来源
- 这些来源是否启用
- 它们属于 feed / crawl / research candidate 的哪一类
- 若未启用，原因是什么

### 4.2 RSSHub 多 route 约束

`RSSHub` 配置不再限制为：

- `platform -> single route`

而应允许：

- `platform -> one or more routes`

若同平台配置了多个 route，则刷新时允许把多个 route 的 feed 文档合并进入同一平台趋势归纳链。

## 5. `bilibili-api-python` 结论

根据当前 docs 真值中的仓库准入规则与既有研究结论：

- `bilibili-api-python` 许可证为 `GPL-3.0`
- 当前主仓未建立与该许可证兼容的直接接入策略

因此在 `N2` 阶段给出明确结论：

- 保留研究价值
- 正式退出主实现路径
- 不再作为“待定主链候选”

这项结论必须在来源配置说明里对 `bilibili` 平台显式可见，而不是只埋在研究文档里。

## 6. 完成判定

满足以下条件即可视为 `N2` 第二批完成：

1. 趋势摘要接口能返回结构化 `configured_sources`
2. 内部趋势控制台能同时展示：
   - 已消费来源轨迹
   - 已配置来源结构
3. 同平台可配置多个 RSSHub route 并合并进入同一次趋势归纳
4. `bilibili-api-python` 已被明确标为因许可证原因退出主实现路径
