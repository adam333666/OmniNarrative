"use client";

import { CardSwap, SwapCard } from "@/components/upstream/card-swap";
import type { CreationPreset } from "@/lib/constants/creation-presets";

import styles from "./creation-preset-deck.module.css";

type CreationPresetDeckProps = {
  presets: CreationPreset[];
  onApply: (preset: CreationPreset) => void;
};

export function CreationPresetDeck({ presets, onApply }: CreationPresetDeckProps) {
  return (
    <section className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>预设起步</span>
        <h3 className={styles.title}>如果你还不确定怎么起手，可以先套用一组现成方向。</h3>
        <p className={styles.lead}>预设会连同平台、内容类型、受众和风格一起填好，让你先跑通一轮，再回头细调更省力。</p>
      </div>

      <div className={styles.deckShell}>
        <CardSwap width={342} height={254} cardDistance={30} verticalDistance={24} delay={3800} pauseOnHover>
          {presets.map((preset) => (
            <SwapCard className={styles.swapCard} key={preset.key}>
              <div className={styles.cardInner}>
                <span className={styles.cardTag}>{preset.tag}</span>
                <h4 className={styles.cardTitle}>{preset.title}</h4>
                <p className={styles.cardSummary}>{preset.summary}</p>
                <div className={styles.metaWrap}>
                  <span className={styles.metaChip}>{preset.payload.target_platform}</span>
                  <span className={styles.metaChip}>{preset.payload.content_type}</span>
                  <span className={styles.metaChip}>{preset.payload.style_tone}</span>
                </div>
                <button className={styles.applyButton} onClick={() => onApply(preset)} type="button">
                  应用这组预设
                </button>
                <span className={styles.cardAccent}>{preset.accent}</span>
              </div>
            </SwapCard>
          ))}
        </CardSwap>
      </div>
    </section>
  );
}
