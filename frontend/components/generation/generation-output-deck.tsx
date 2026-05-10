"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";

import styles from "./generation-output-deck.module.css";

const cards = [
  {
    key: "theme",
    tag: "Theme",
    title: "主题方向",
    body: "先把一句模糊想法整理清楚，避免后面每一步都各自理解一遍。",
    accent: "Theme Parsing",
  },
  {
    key: "profile",
    tag: "Profile",
    title: "受众与风格",
    body: "受众特点和风格方向会先被整理出来，后面的标题、脚本和镜头都会参考这一层。",
    accent: "Profile Parsing",
  },
  {
    key: "trend",
    tag: "Trend",
    title: "平台参考提示",
    body: "这些参考会直接影响开场方式、节奏、标题封面和规避方向。",
    accent: "Trend Adapting",
  },
  {
    key: "narrative",
    tag: "Narrative",
    title: "叙事骨架",
    body: "标题、梗概、段落脚本和关键镜头会一起成形，不是零散拼接。",
    accent: "Narrative",
  },
  {
    key: "package",
    tag: "Package",
    title: "完整结果",
    body: "整体方向、脚本、发布建议和制作信息会被整理成一份完整结果。",
    accent: "Package",
  },
];

export function GenerationOutputDeck() {
  return (
    <section className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>正在生成什么</span>
        <h3 className={styles.title}>等待不是空白期，系统正在一步步整理这份方案。</h3>
        <p className={styles.lead}>这组卡片会告诉你，每个阶段大概在补什么内容。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={340} height={248} cardDistance={30} verticalDistance={24} delay={3600} pauseOnHover>
          {cards.map((card) => (
            <SwapCard className={styles.swapCard} key={card.key}>
              <div className={styles.cardInner}>
                <span className={styles.cardTag}>{card.tag}</span>
                <h4 className={styles.cardTitle}>{card.title}</h4>
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
