"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";
import type { TrendTemplateSummary } from "@/lib/api-client/backend";

import styles from "./trend-strategy-deck.module.css";

type TrendStrategyDeckProps = {
  item: TrendTemplateSummary;
};

export function TrendStrategyDeck({ item }: TrendStrategyDeckProps) {
  const cards = [
    {
      key: "hooks",
      tag: "Hooks",
      title: "近期起手模式",
      items: item.hook_patterns,
      accent: "Openers",
    },
    {
      key: "rhythm",
      tag: "Rhythm",
      title: "近期节奏偏好",
      items: item.rhythm_patterns,
      accent: "Rhythm Patterns",
    },
    {
      key: "title",
      tag: "Covers",
      title: "标题 / 封面风格",
      items: item.title_cover_style,
      accent: "Title + Cover",
    },
    {
      key: "avoid",
      tag: "Avoid",
      title: "近期规避点",
      items: item.avoid_patterns,
      accent: "Avoid Patterns",
    },
  ];

  return (
    <div className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>参考拆解</span>
        <h4 className={styles.title}>这些提示不只是一句摘要，而是已经拆成了更容易直接使用的几类方向。</h4>
        <p className={styles.lead}>{item.audience_preference_summary}</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={332} height={236} cardDistance={28} verticalDistance={22} delay={3600} pauseOnHover>
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
