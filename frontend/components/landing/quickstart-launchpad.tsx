import Link from "next/link";

import { BorderGlow } from "@/components/upstream/border-glow";
import { creationPresets } from "@/lib/constants/creation-presets";

import styles from "./quickstart-launchpad.module.css";

export function QuickstartLaunchpad() {
  return (
    <section className={styles.section} id="quickstart-launchpad">
      <div className={styles.copy}>
        <span className={styles.eyebrow}>快速开始</span>
        <h2 className={styles.title}>如果你想先看一个完整结果，可以直接从预设开始。</h2>
        <p className={styles.lead}>这些预设会先帮你填好平台、内容类型、受众和风格，让你先跑通一轮，再回头细调。</p>
      </div>

      <div className={styles.grid}>
        {creationPresets.map((preset) => (
          <BorderGlow
            backgroundColor="rgba(255, 252, 246, 0.94)"
            borderRadius={26}
            className={styles.cardShell}
            colors={["rgba(239, 124, 72, 0.88)", "rgba(63, 140, 126, 0.82)", "rgba(255, 211, 157, 0.8)"]}
            key={preset.key}
          >
            <article className={styles.card}>
              <div className={styles.header}>
                <span className={styles.tag}>{preset.tag}</span>
                <span className={styles.platform}>{preset.payload.target_platform}</span>
              </div>
              <h3 className={styles.cardTitle}>{preset.title}</h3>
              <p className={styles.cardCopy}>{preset.summary}</p>
              <div className={styles.metaRow}>
                <span className={styles.metaChip}>{preset.payload.content_type}</span>
                <span className={styles.metaChip}>{preset.payload.style_tone}</span>
              </div>
              <Link className={styles.cardLink} href={`/create?preset=${preset.key}`}>
                直接用这组预设开始
              </Link>
            </article>
          </BorderGlow>
        ))}
      </div>
    </section>
  );
}
