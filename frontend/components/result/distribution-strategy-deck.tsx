"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";

import styles from "./distribution-strategy-deck.module.css";

type DistributionStrategyDeckProps = {
  titleAlternatives: string[];
  hookAlternatives: string[];
  coverCopyAlternatives: string[];
  distributionAngles: string[];
};

const groups = [
  { key: "titles", tag: "Titles", title: "标题备选", accent: "Title Angles" },
  { key: "hooks", tag: "Hooks", title: "开场钩子", accent: "First-Three-Seconds" },
  { key: "covers", tag: "Covers", title: "封面文案", accent: "Cover Copy" },
  { key: "distribution", tag: "Distribution", title: "传播角度", accent: "Distribution Angles" },
] as const;

export function DistributionStrategyDeck({
  titleAlternatives,
  hookAlternatives,
  coverCopyAlternatives,
  distributionAngles,
}: DistributionStrategyDeckProps) {
  const contentMap = {
    titles: titleAlternatives,
    hooks: hookAlternatives,
    covers: coverCopyAlternatives,
    distribution: distributionAngles,
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>备选方案</span>
        <h4 className={styles.title}>这里把标题、开场、封面和发布角度拆开，方便你快速比较不同方向。</h4>
        <p className={styles.lead}>如果你还没决定最终版本，可以先在这里对比几种写法，再挑最适合的一组继续用。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={336} height={248} cardDistance={30} verticalDistance={24} delay={3600} pauseOnHover>
          {groups.map((group) => (
            <SwapCard className={styles.swapCard} key={group.key}>
              <div className={styles.cardInner}>
                <span className={styles.cardTag}>{group.tag}</span>
                <h5 className={styles.cardTitle}>{group.title}</h5>
                <div className={styles.cardList}>
                  {contentMap[group.key].slice(0, 4).map((item) => (
                    <div className={styles.cardItem} key={item}>
                      <span className={styles.cardDot} />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
                <span className={styles.cardAccent}>{group.accent}</span>
              </div>
            </SwapCard>
          ))}
        </CardSwap>
      </div>
    </div>
  );
}
