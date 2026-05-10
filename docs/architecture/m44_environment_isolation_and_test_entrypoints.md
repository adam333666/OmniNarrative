# M44 环境隔离与统一测试入口收口

## 1. 文档定位

本文档用于收口当前继续开发过程中暴露出的环境历史问题：

> 当前项目虽然已经具备 `backend/.venv` 启动路径，
> 但测试和临时调试仍容易误用宿主 Python 环境，
> 从而受到宿主已安装包、数据库驱动和 pytest 插件的干扰。

本文档目标是建立更清晰的项目级环境隔离说明和统一测试入口。

本文档受以下事实源约束：
- `docs/stage_records/stage_02_project_handoff_summary_v2.md`
- `docs/stage_records/stage_03_next_phase_deepening_plan_v1.md`
- `docs/changelog.md`

---

## 2. 当前问题

当前历史问题主要来自三点：

1. 宿主 Python 环境与项目虚拟环境并存  
容易出现：
- 宿主缺少 `psycopg` 方言驱动
- 宿主已有 `langchain*` / `pytest` / 插件版本与项目期望不一致

2. 测试命令入口不统一  
开发者可能直接在宿主环境执行：
- `pytest`
- `python3 -m ...`

从而绕过 `backend/.venv`。

3. 一期阶段更偏主链打通  
早期优先级是能力联通，不是环境治理，所以环境隔离说明尚未完全收口。

---

## 3. 本轮目标

1. 明确要求后端开发与测试优先使用 `backend/.venv`
2. 提供统一的后端测试入口脚本
3. 在 README 中明确区分“宿主环境问题”和“项目代码问题”

---

## 4. 技术方案

### 4.1 文档层

- 更新根 README
- 更新 backend README
- 明确：
  - 后端依赖安装到 `backend/.venv`
  - 后端测试优先通过统一脚本运行
  - 宿主 Python 仅用于引导，不作为长期运行入口

### 4.2 脚本层

新增统一脚本：
- `scripts/backend_test.sh`

用途：
- 自动检查 `backend/.venv`
- 自动注入 `PYTHONPATH`
- 默认使用 SQLite 测试库
- 将额外 pytest 参数透传

---

## 5. 验证口径

1. `bash -n scripts/backend_test.sh` 通过
2. 使用统一脚本跑至少一组后端测试通过

---

## 6. 完成标准

- 文档已明确环境隔离要求
- 统一测试入口已存在
- changelog 已更新
- 有独立 git 提交
