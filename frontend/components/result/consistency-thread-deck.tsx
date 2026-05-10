"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";

import styles from "./consistency-thread-deck.module.css";

type ConsistencyThreadDeckProps = {
  themeText: string;
  audienceText: string;
  styleSummary: string;
  trendSummary: string;
  platformStrategy: string;
};

export function ConsistencyThreadDeck({
  themeText,
  audienceText,
  styleSummary,
  trendSummary,
  platformStrategy,
}: ConsistencyThreadDeckProps) {
  const cards = [
    {
      key: "theme",
      tag: "Theme",
      title: "中心主题",
      body: themeText,
      accent: "Single Center",
    },
    {
      key: "audience",
      tag: "Audience",
      title: "受众理解",
      body: audienceText,
      accent: "Audience Fit",
    },
    {
      key: "style",
      tag: "Style",
      title: "风格表达",
      body: styleSummary,
      accent: "Style Cohesion",
    },
    {
      key: "trend",
      tag: "Trend",
      title: "趋势改造",
      body: trendSummary,
      accent: "Trend Adaptation",
    },
    {
      key: "execution",
      tag: "Execution",
      title: "执行落点",
      body: platformStrategy,
      accent: "Platform Strategy",
    },
  ];

  return (
    <div className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>方案主线</span>
        <h4 className={styles.title}>这份方案不是很多块内容拼起来的，而是围绕同一个目标一路展开的。</h4>
        <p className={styles.lead}>把主题、受众、风格、参考信息和落地方式拆开看，是为了让你更容易判断整份方案是否前后一致。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={340} height={246} cardDistance={30} verticalDistance={24} delay={3600} pauseOnHover>
          {cards.map((card) => (
            <SwapCard className={styles.swapCard} key={card.key}>
              <div className={styles.cardInner}>
                <span className={styles.cardTag}>{card.tag}</span>
                <h5 className={styles.cardTitle}>{card.title}</h5>
                <p className={styles.cardBody}>{card.body}</p>
                <span className={styles.cardAccent}>{card.accent}</span>
              </div>
            </SwapCard>
          ))}
        </CardSwap>
      </div>
    </div>
  );
}
