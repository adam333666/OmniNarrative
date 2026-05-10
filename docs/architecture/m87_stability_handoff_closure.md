# M87 演示与交接稳定复现收口

## 本轮目标

完成最后一个未闭环里程碑 `M-P5-A`，把“可演示、可运行”进一步收成“可复现、可交接”。

这轮不再扩写新功能，而是把关键验证入口、启动说明与文档真值统一起来，避免后续接手时出现“功能已经完成，但不知道该怎么验证”的状态。

## 修改范围

- `scripts/demo_regression.sh`
- `README.md`
- `backend/README.md`
- `frontend/README.md`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`

## 实现说明

### 1. 新增统一演示回归入口

新增 `scripts/demo_regression.sh`，串起：

- 后端关键回归集合
- 前端生产构建

这样演示前或交接时，不再需要人工记忆多个分散命令。

### 2. 启动与验证说明统一到 README

根目录、后端、前端 README 都统一指向：

- `scripts/dev_bootstrap.sh`
- `scripts/backend_test.sh`
- `scripts/demo_regression.sh`
- `scripts/smoke_test.sh`

并明确各自用途，避免入口漂移。

### 3. 总计划里程碑闭环

同步更新总计划文档：

- `M-P5-A` 从未完成推进为已完成
- “下一步直接执行建议”改为反映当前真实状态，而不是历史阶段顺序

## 对应里程碑

- `M-P5-A 演示和交接稳定可复现`

## 收口判断

本轮完成后，最后一个收口条件具备：

- 关键测试入口可跑
- 本地启动说明可用
- 文档真值与实际状态一致
- 明显的文档入口漂移已收口
