# M31 后端阶段 F：验证与回归封口

## 目标

对后端阶段 A 到 E 已完成的真实胶水链做一次更高层的自动化验证封口，确保数据库真值层、趋势刷新、模型优先叙事生成、持久化状态链和导出链在组合运行时保持稳定。

本阶段目标：
- 在不新增业务能力的前提下，补齐高价值集成回归。
- 验证趋势刷新不仅返回成功，而且真正写回数据库真值层。
- 验证 `generate -> status -> result -> export -> video payload` 在持久化状态层切换后仍保持稳定。
- 将阶段 F 的验证策略、边界和材料来源落入 docs 真值层。

## 原材料来源

本阶段直接参考：
- `/home/admin2/smy/multi-media/backend/tests/test_m26_trend_repository_bootstrap.py`
- `/home/admin2/smy/multi-media/backend/tests/test_m27_trend_collection.py`
- `/home/admin2/smy/multi-media/backend/tests/test_m28_model_gateway.py`
- `/home/admin2/smy/multi-media/backend/tests/test_m29_model_first_narrative.py`
- `/home/admin2/smy/multi-media/backend/tests/test_m30_generation_store_persistence.py`

## 为什么这样做

- 现有测试已经覆盖了阶段 A 到 E 的模块边界，但还缺“跨模块组合运行”的封口层。
- 当前后端的主要风险已经从“单点能力缺失”转为“能力接上后是否仍稳定”，所以阶段 F 的重点应当是组合验证，而不是继续堆单个 service 的孤立测试。
- 这类集成回归可以最大化利用当前已落地的胶水原材料，不需要自造新的模拟框架。

## 验证重点

### 1. 趋势刷新写回数据库真值
- 通过 monkeypatch 固定趋势采集结果。
- 调用真实 `trend_strategy_service.refresh_templates()`。
- 再通过 repository 读取同一模板，确认刷新结果已经进入数据库真值层，而不是只停留在返回值。

### 2. 主链路在持久化状态层下仍然稳定
- 通过真实 API 触发 `generate`。
- 通过受控阶段推进使任务先进入 `PACKAGE_ASSEMBLING`，再由真实结果读取链完成最终物化并收口到 `DONE`。
- 使用新的 `GenerationPipelineStore` 实例读取状态，确认结果不依赖单例内存态。
- 串行验证 `status / result / export/json / export/md / video-payload` 的稳定性。

## 边界条件

- 不依赖真实外部网络。
- 不依赖真实模型供应商。
- 趋势刷新仍使用受控 fixture / monkeypatch，不把测试变成实时抓取测试。
- 该阶段只补验证，不在此阶段追加新的业务字段或新接口。

## 验证要求

- `python3 -m py_compile` 通过。
- 后端测试通过，新增阶段 F 测试并与既有阶段 A-E 回归一起执行。
- 同步更新 `docs/changelog.md`。
- 以同一批次 Git 提交收口。
