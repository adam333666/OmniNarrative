"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";

import styles from "./consistency-preview-deck.module.css";

type ConsistencyPreviewDeckProps = {
  themeText: string;
  audienceText: string;
  platformLabel: string;
  styleLabel: string;
};

export function ConsistencyPreviewDeck({
  themeText,
  audienceText,
  platformLabel,
  styleLabel,
}: ConsistencyPreviewDeckProps) {
  const cards = [
    {
      key: "theme",
      tag: "Theme",
      title: "中心主题",
      body: themeText || "当你填入主题后，后面的内容会尽量围绕这个核心方向展开。",
      accent: "Single Center",
    },
    {
      key: "audience",
      tag: "Audience",
      title: "受众理解",
      body: audienceText || "目标受众不是附属信息，后面的标题、脚本、镜头和语气都会参考这层判断。",
      accent: "Audience Fit",
    },
    {
      key: "platform",
      tag: "Platform",
      title: "平台适配",
      body: `${platformLabel} 会影响开场方式、节奏、标题封面和整体表达。`,
      accent: "Platform Adaptation",
    },
    {
      key: "style",
      tag: "Style",
      title: "风格统一",
      body: `${styleLabel} 不只是一个标签，后面的内容会尽量保持这条风格方向。`,
      accent: "Style Cohesion",
    },
  ];

  return (
    <section className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>填写预览</span>
        <h3 className={styles.title}>这里填的每一项，都会影响最后这份方案的方向。</h3>
        <p className={styles.lead}>主题、受众、平台和风格会先在这里对齐，后面的脚本、镜头和发布建议都会围绕它展开。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={340} height={244} cardDistance={30} verticalDistance={24} delay={3600} pauseOnHover>
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
