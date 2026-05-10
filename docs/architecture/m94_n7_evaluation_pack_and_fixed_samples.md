# M94 N7 固定评测包与交付入口

## 1. 背景

`N4` 已把统一回归顺序和 `Playwright` 页面级验证入口接上主链。

`N7` 不再新造评测系统，而是把现有入口收口成一套评测团队可直接执行的固定材料：

- 固定样例输入
- 固定观察点
- 固定执行入口
- 固定操作顺序

## 2. 本轮目标

本轮锁定四件事：

1. 固定一组评测输入样例
2. 固定一组核心观察点
3. 固定一组标准执行入口
4. 让评测团队不依赖口头说明即可开始执行

## 3. 固定入口

### 3.1 统一回归入口

- `./scripts/demo_regression.sh`
  - 用于统一验证：
    - 后端关键回归
    - 前端生产构建
    - `Playwright` 页面级 E2E

### 3.2 固定样例入口

- `./scripts/evaluation_sample_pack.sh`
  - 复用既有 `smoke_test.sh`
  - 串行执行固定样例输入
  - 验证：
    - `health`
    - `input-options`
    - `generate`
    - `status`
    - `result`
    - `export/json`
    - `export/md`
    - `video-payload`

## 4. 固定样例

样例文件位于：

- `docs/testing/evaluation_samples/`

当前固定三组：

1. `science_bilibili_time_travel.json`
2. `history_rednote_reform_story.json`
3. `workplace_wechat_efficiency.json`

这些样例分别用于观察：

- 科普/脑洞内容链
- 历史/叙事内容链
- 职场/实用内容链

## 5. 固定观察点

观察点文档位于：

- `docs/testing/n7_evaluation_sample_matrix.md`

当前要求至少核对四个核心目标：

1. 内部内容设计一致性
2. 外部趋势增强
3. 超重型结构化内容
4. 简单上手

## 6. Langfuse 当前结论

`Langfuse` 在本轮仍保持候选状态，不进入正式主链。

原因：

- 当前 `N7` 的最小完成标准是“固定评测入口与材料可直接执行”
- 现有 `demo_regression.sh`、`smoke_test.sh`、`Playwright` 与评测文档已经足以完成这一目标
- 若此时为了观测再接一条 tracing 主链，会扩大实现面，不符合本轮“胶水收口优先”的原则

## 7. 完成判定

满足以下条件即可视为 `N7` 当前范围完成：

1. 已有固定评测样例文件
2. 已有固定观察点矩阵
3. 已有固定执行入口
4. README 与评测交接文档都能指向这套固定材料
