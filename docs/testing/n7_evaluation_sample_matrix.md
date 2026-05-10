# N7 固定评测样例与观察点矩阵

## 1. 建议执行顺序

1. `./scripts/demo_regression.sh`
2. `./scripts/evaluation_sample_pack.sh`
3. 需要人工回看时，再进入：
   - 首页
   - 创建页
   - 生成页
   - 结果页
   - `internal/trends`
   - `internal/checkpoints/{generation_id}`

## 2. 样例矩阵

| 样例 | 文件 | 重点观察 |
| --- | --- | --- |
| 科普脑洞 | `docs/testing/evaluation_samples/science_bilibili_time_travel.json` | 趋势影响、解释链完整度、结果包执行字段 |
| 历史叙事 | `docs/testing/evaluation_samples/history_rednote_reform_story.json` | 受众适配、平台表达风格、标题封面方向 |
| 职场实用 | `docs/testing/evaluation_samples/workplace_wechat_efficiency.json` | 低门槛上手、结构化结果可用性、导出链一致性 |

## 3. 四个核心目标的观察口径

### 3.1 内部内容设计一致性

- 首页、创建页、结果页是否都围绕同一个用户任务
- 主题、受众、风格、趋势、执行是否围绕同一中心
- `result / export/json / export/md / video-payload` 是否保持同源

### 3.2 外部趋势增强

- 结果是否能看出趋势对标题、钩子、分发角度有影响
- 结果页和内部趋势页是否能回看趋势依据
- 不同样例下的趋势摘要和来源轨迹是否仍可追踪

### 3.3 超重型结构化内容

- 结果页是否仍保有多层结构
- 执行级字段是否可直接支撑下游消费
- Video payload 是否包含关键执行字段而不是简化文本

### 3.4 简单上手

- 第一次使用者是否知道该先做什么
- 创建页每一步是否知道要填什么
- 生成页和结果页是否都能回答“下一步做什么”

## 4. 快速判定规则

- 若 `demo_regression.sh` 失败，则先判定当前版本不满足连续评测入口要求。
- 若 `evaluation_sample_pack.sh` 中任一固定样例失败，则先判定 API 主链对固定样例不稳定。
- 若自动化通过，但四个核心目标中有任意一项无法在页面或导出物中快速观察到，则判定为“可运行但交付说明不足”。
