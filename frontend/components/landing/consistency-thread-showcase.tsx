"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";

import styles from "./consistency-thread-showcase.module.css";

const cards = [
  {
    key: "theme",
    tag: "Theme",
    title: "一句主题先定中心",
    body: "你写下的主题不会被拆得七零八落，后面的内容会尽量围绕这一个核心方向展开。",
    accent: "Single Center",
  },
  {
    key: "audience",
    tag: "Audience",
    title: "受众决定表达角度",
    body: "后面的标题、叙事、镜头与发布动作都会围绕目标受众重新取舍，而不是按统一模板硬套。",
    accent: "Audience Fit",
  },
  {
    key: "style",
    tag: "Style",
    title: "风格会前后一致",
    body: "风格不会只停留在一句描述里，后面的脚本、视觉和开场方式都会尽量保持同样的语气。",
    accent: "Style Cohesion",
  },
  {
    key: "trend",
    tag: "Trend",
    title: "趋势只做增强，不打散中心",
    body: "参考信息会帮助内容更贴合平台，但不会把你的原始方向带偏。",
    accent: "Trend Adaptation",
  },
  {
    key: "result",
    tag: "Result",
    title: "最后形成一份前后一致的方案",
    body: "从总览到脚本，再到发布和制作建议，整体会尽量保持同一条思路，不会明显割裂。",
    accent: "Unified Package",
  },
];

export function ConsistencyThreadShowcase() {
  return (
    <section className={styles.wrapper} id="consistency-thread-home">
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>方案一致性</span>
        <h2 className={styles.title}>更重要的不是生成得多，而是让整份方案前后一致、方向清楚。</h2>
        <p className={styles.lead}>这样你在查看结果时，会更容易判断这份方案是不是围绕同一个目标稳定展开，而不是东拼西凑。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={344} height={248} cardDistance={32} verticalDistance={24} delay={3600} pauseOnHover>
          {cards.map((card) => (
            <SwapCard className={styles.swapCard} key={card.key}>
              <div className={styles.cardInner}>
                <span className={styles.cardTag}>{card.tag}</span>
                <h3 className={styles.cardTitle}>{card.title}</h3>
                <p className={styles.cardBody}>{card.body}</p>
                <span className={styles.cardAccent}>{card.accent}</span>
              </div>
            </SwapCard>
          ))}
        </CardSwap>
      </div>
    </section>
  );
}
