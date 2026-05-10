# M58 RSSHub 趋势入口层接入

## 1. 背景

当前系统的趋势链已经具备：

- 数据库真值层
- 手动刷新入口
- `Crawl4AI + Instructor` 结构化归纳链

但趋势入口层仍偏轻，主要依赖现有页面入口抓取。根据当前总计划，下一步必须把趋势链推进到“成熟 feed 入口 + 现有归纳链”的组合。

## 2. 本轮目标

本轮目标是把 `RSSHub` 真正接入趋势刷新主链，作为可配置的成熟 feed 入口层：

- 当配置了 `RSSHub` 时，刷新主链优先消费 RSS feed
- 将 feed 内容整合成可供现有结构化归纳链消费的文档
- 在未配置或不可用时，继续回退到现有 `Crawl4AI` 页面入口

## 3. 具体实现

### 3.1 新增 RSSHub adapter

新增：

- `backend/app/integrations/rss/rsshub_adapter.py`

能力包括：

- 基于 `httpx` 拉取 RSSHub feed
- 解析 XML RSS payload
- 提取 feed item 的 `title / link / description`

### 3.2 接入趋势刷新主链

`TrendCollectorService` 增加：

- `rsshub_base_url`
- `rsshub_platform_routes`
- `rsshub_item_limit`

刷新顺序改为：

1. 先尝试从 RSSHub 采集已配置平台的 feed
2. 将 feed item 组装成结构化文档
3. 交给现有 `Instructor` 结构化归纳链
4. RSSHub 未配置或不可用时，再回退到现有 `Crawl4AI` 页面入口

### 3.3 配置入口

新增环境变量：

- `TREND_RSSHUB_BASE_URL`
- `TREND_RSSHUB_PLATFORM_ROUTES`
- `TREND_RSSHUB_ITEM_LIMIT`

当前示例默认先接入：

- `bilibili -> /bilibili/popular/all`

## 4. 验证

验证方式：

- `python3 -m py_compile ...`
- `./scripts/backend_test.sh tests/test_m27_trend_collection.py tests/test_m58_rsshub_trend_ingestion.py tests/test_m41_internal_trend_api.py`

本轮新增回归：

- `tests/test_m58_rsshub_trend_ingestion.py`

该测试覆盖：

- `RSSHub` 已配置时，即使 `Crawl4AI` 不可用，仍可通过 feed 完成趋势归纳

## 5. 阶段意义

这轮对应总计划中的：

- `P1` 趋势入口真正成熟化

它的意义不是单纯多一个 adapter 文件，而是把“外部趋势导入与传播增强”真正推进到成熟订阅源入口层，开始符合：

- `RSSHub + Crawl4AI + Instructor`

这条目标路线。
