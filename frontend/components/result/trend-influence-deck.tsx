"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";

import styles from "./trend-influence-deck.module.css";

type TrendInfluenceDeckProps = {
  hookPatterns: string[];
  rhythmPatterns: string[];
  titleCoverStyle: string[];
  avoidPatterns: string[];
  hotTopics: string[];
  interactionPatterns: string[];
  emotionalEntryPoints: string[];
  creatorAngleSummary: string;
};

export function TrendInfluenceDeck({
  hookPatterns,
  rhythmPatterns,
  titleCoverStyle,
  avoidPatterns,
  hotTopics,
  interactionPatterns,
  emotionalEntryPoints,
  creatorAngleSummary,
}: TrendInfluenceDeckProps) {
  const cards = [
    { key: "hooks", tag: "Hooks", title: "起手方式", items: hookPatterns, accent: "Trend Hooks" },
    { key: "rhythm", tag: "Rhythm", title: "节奏方式", items: rhythmPatterns, accent: "Trend Rhythm" },
    { key: "cover", tag: "Covers", title: "标题 / 封面风格", items: titleCoverStyle, accent: "Title + Cover" },
    { key: "avoid", tag: "Avoid", title: "规避方向", items: avoidPatterns, accent: "Avoid Patterns" },
    { key: "topics", tag: "Topics", title: "热点线索", items: hotTopics, accent: "Hot Topics" },
    { key: "interaction", tag: "Interact", title: "互动方式", items: interactionPatterns, accent: "Interaction" },
    { key: "emotion", tag: "Emotion", title: "情绪切口", items: emotionalEntryPoints, accent: "Emotion Entry" },
    { key: "angle", tag: "Angle", title: "创作者角度", items: [creatorAngleSummary], accent: "Creator Angle" },
  ];

  return (
    <div className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>参考影响</span>
        <h4 className={styles.title}>这次结果不是凭空展开的，而是结合了当前平台上更适合的表达方式。</h4>
        <p className={styles.lead}>这里把这些影响拆成开场、节奏、标题封面、规避点和互动方式，方便你快速看懂它们改动了哪里。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={336} height={242} cardDistance={28} verticalDistance={24} delay={3600} pauseOnHover>
          {cards.map((card) => (
            <SwapCard className={styles.swapCard} key={card.key}>
              <div className={styles.cardInner}>
                <span className={styles.cardTag}>{card.tag}</span>
                <h5 className={styles.cardTitle}>{card.title}</h5>
                <div className={styles.cardList}>
                  {card.items.slice(0, 4).map((entry) => (
                    <div className={styles.cardItem} key={entry}>
                      <span className={styles.cardDot} />
                      <span>{entry}</span>
                    </div>
                  ))}
                </div>
                <span className={styles.cardAccent}>{card.accent}</span>
              </div>
            </SwapCard>
          ))}
        </CardSwap>
      </div>
    </div>
  );
}
