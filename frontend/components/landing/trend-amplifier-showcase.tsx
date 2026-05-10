"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";

import styles from "./trend-amplifier-showcase.module.css";

const cards = [
  {
    key: "entry",
    tag: "Entry",
    title: "先看最近大家更容易接受什么",
    body: "不会只靠空想去猜用户偏好，而是先整理近期更容易被接受的表达方向。",
    accent: "RSSHub Entry",
  },
  {
    key: "structure",
    tag: "Structure",
    title: "再把参考信息整理成可用建议",
    body: "这些内容不会原样堆给你，而是会被整理成开场、节奏、标题和规避点等更好用的建议。",
    accent: "Structured Trend",
  },
  {
    key: "create",
    tag: "Create",
    title: "开始前就先让你看到重点",
    body: "在真正生成前，你就能先看到当前最值得参考的方向，不用等到结果出来后再回头理解。",
    accent: "Create Preview",
  },
  {
    key: "result",
    tag: "Result",
    title: "最后把这些建议带进方案里",
    body: "这些参考会真正影响脚本、开场、标题和发布建议，而不是只停留在说明文字里。",
    accent: "Result Influence",
  },
];

export function TrendAmplifierShowcase() {
  return (
    <section className={styles.wrapper} id="trend-amplifier-home">
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>参考信息</span>
        <h2 className={styles.title}>这些参考不是装饰，而是真的会影响最后的写法和发布建议。</h2>
        <p className={styles.lead}>你可以把它理解成一层提前给到的外部提醒，帮助这次内容更贴近平台语境和用户阅读习惯。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={344} height={246} cardDistance={32} verticalDistance={24} delay={3600} pauseOnHover>
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
