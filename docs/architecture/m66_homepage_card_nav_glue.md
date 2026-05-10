# M66 首页 CardNav 胶水接入

## 1. 背景

当前首页已经完成第一轮品牌化升级，但还缺少一个更像“产品入口”的顶部能力导航层。  
在不新增一套自写导航系统的前提下，本轮继续优先复用 `/home/admin2/smy/upstream-materials/react-bits-main/src/ts-default/Components/CardNav/` 的成熟组件语义。

## 2. 本轮目标

- 让首页顶部具备更强的品牌入口感和能力总览感
- 继续优先复用上游前端组件，不手写新的展开式导航系统
- 让首页更适合演示四个核心能力和主流程入口

## 3. 方案

- 直接参考上游 `CardNav.tsx` 与 `CardNav.css`
- 在本仓新增 `frontend/components/upstream/card-nav.tsx`
- 使用已有依赖 `gsap` 保留上游展开动画
- 用当前项目已存在的 `lucide-react` 替代上游 `react-icons/go`
- 把图片 Logo 改成文本品牌位，避免为本轮额外引入图像资产
- 在首页 `CreativeHero` 顶部接入 `CardNav`

## 4. 变更范围

- `frontend/components/upstream/card-nav.tsx`
- `frontend/components/upstream/card-nav.module.css`
- `frontend/components/landing/creative-hero.tsx`
- `frontend/components/landing/creative-hero.module.css`

## 5. 预期结果

- 首页顶部增加一个可展开的能力导航带
- 用户可从首页更快进入创作向导、内部趋势控制台与 checkpoint 入口
- 首页品牌感继续增强，同时保持“薄胶水 + 上游复用”的开发边界
