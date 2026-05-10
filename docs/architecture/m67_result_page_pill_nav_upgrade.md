# M67 结果页 PillNav 导航升级

## 1. 背景

结果页已经具备较重的结构化内容，但顶部的分区导航仍是仓内轻量手写 `pill` 实现。  
这一层非常适合继续遵循强胶水编程原则，直接复用 `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/Components/PillNav/` 的成熟导航语义，而不是继续维持自写导航组件。

## 2. 本轮目标

- 把结果页分区导航从轻量手写实现升级成更适合展示的品牌导航条
- 继续优先复用上游源码与已有依赖 `gsap`
- 不新增新的结果页业务逻辑，只增强结果页导航与阅读体验

## 3. 方案

- 新增 `frontend/components/upstream/pill-nav.tsx`
- 参考上游 `PillNav.tsx` 与 `PillNav.css`
- 保留上游 hover 圆弧动画与移动端折叠菜单
- 去掉 `react-router-dom` 依赖，改成当前项目直接使用锚点 `a href="#..."` 跳转
- 将现有 `result-section-nav.tsx` 改造成对上游适配版 `PillNav` 的薄胶水包装

## 4. 变更范围

- `frontend/components/upstream/pill-nav.tsx`
- `frontend/components/upstream/pill-nav.module.css`
- `frontend/components/result/result-section-nav.tsx`
- `frontend/components/result/result-section-nav.module.css`（移除）

## 5. 预期结果

- 结果页总览层、Markdown、脚本层、平台层、多模态层、机器层的跳转入口更统一
- 结果页更像“重型结构化方案工作台”，不是一页普通内容堆叠
- 这轮继续以“复制上游源码 + 最小适配”的方式推进，不新增手写导航系统
