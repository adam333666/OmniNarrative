import Link from "next/link";

import { GlassSurface } from "@/components/upstream/glass-surface";

import styles from "./flow-stage-banner.module.css";

export type FlowStageBannerAction = {
  label: string;
  href: string;
};

export type FlowStageBannerProps = {
  stage: string;
  summary: string;
  nextStep: string;
  highlights: string[];
  actions: FlowStageBannerAction[];
};

export function FlowStageBanner({ stage, summary, nextStep, highlights, actions }: FlowStageBannerProps) {
  return (
    <div className={styles.banner}>
      <GlassSurface backgroundOpacity={0.08} blur={12} borderRadius={28} className={styles.heroCard}>
        <div className={styles.heroInner}>
          <span className={styles.stageBadge}>{stage}</span>
          <p className={styles.summary}>{summary}</p>
          <p className={styles.nextStep}>
            接下来：<strong>{nextStep}</strong>
          </p>
        </div>
      </GlassSurface>

      <div className={styles.sideGrid}>
        <GlassSurface backgroundOpacity={0.1} blur={10} borderRadius={24} className={styles.panelCard}>
          <div className={styles.panelInner}>
            <span className={styles.panelLabel}>重点</span>
            <div className={styles.highlightWrap}>
              {highlights.map((item) => (
                <span className={styles.highlightChip} key={item}>
                  {item}
                </span>
              ))}
            </div>
          </div>
        </GlassSurface>

        <GlassSurface backgroundOpacity={0.1} blur={10} borderRadius={24} className={styles.panelCard}>
          <div className={styles.panelInner}>
            <span className={styles.panelLabel}>常用操作</span>
            <div className={styles.actionWrap}>
              {actions.map((action) => (
                <Link className={styles.actionLink} href={action.href} key={action.label}>
                  {action.label}
                </Link>
              ))}
            </div>
          </div>
        </GlassSurface>
      </div>
    </div>
  );
}
