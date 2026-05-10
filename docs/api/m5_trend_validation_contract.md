# M5 趋势分析与验证契约

## 1. 文档目标

本文件用于锁定一期 M5 的趋势模板读取、手动刷新与自动化验证边界。

本阶段覆盖：
- GET /api/v1/config/trend-templates
- POST /api/v1/config/trend-refresh
- scripts/trend_refresh.py
- 后端最小自动化测试集
- 主链路验证记录

---

## 2. 顶层原则

- 趋势模板必须从统一仓储读取，不允许继续把平台模板长期写死在业务服务常量里。
- 手动刷新能力必须复用同一套模板仓储与刷新服务，不允许 CLI 和内部 API 各写一套逻辑。
- 趋势模板读取接口只暴露当前系统真值，不额外拼装第二套展示结构。
- 自动化测试至少覆盖输入校验、趋势模板读取、结果包结构、导出 payload 四类关键能力。

---

## 3. 接口定义

### 3.1 GET /api/v1/config/trend-templates

用途：读取当前系统中的平台趋势模板摘要。

行为约束：
- 支持 platform 可选过滤。
- 支持 content_type 可选过滤。
- 返回字段至少包含 platform、content_type、summary、source_type、updated_at、hot_topics_summary。
- 若未命中过滤条件，返回空列表而不是伪造默认结果。

### 3.2 POST /api/v1/config/trend-refresh

用途：手动刷新一期趋势模板仓储。

行为约束：
- 必须通过内部 API Key 保护。
- 必须复用统一刷新服务。
- 返回 refreshed_count、updated_at 与刷新后的模板摘要。
- 一期允许使用种子模板和规则化刷新结果，不要求实时联网抓取。

---

## 4. CLI 约束

scripts/trend_refresh.py 的要求：
- 必须直接调用统一刷新服务。
- 输出本次刷新数量、更新时间与模板摘要。
- 不允许在脚本里复制另一套模板数据。

---

## 5. 测试与验证约束

最小自动化测试集至少包含：
- 非法输入被拒绝。
- 趋势模板可读取且刷新后仍满足契约。
- 结果包接口返回统一结构。
- Markdown 导出与 Video payload 接口返回关键字段。

当前阶段允许的简化：
- 趋势模板仓储可以先采用文件仓储，而不是直接接 PostgreSQL。
- 刷新结果可以基于本地种子模板和规则化附加信息生成。
- 验证记录可以先以文档形式保存在 docs/testing。
