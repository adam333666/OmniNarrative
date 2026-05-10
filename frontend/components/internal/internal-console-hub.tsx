import Link from "next/link";

import { SpotlightCard } from "@/components/ui/spotlight-card";

import styles from "./internal-console-hub.module.css";

type InternalConsoleHubProps = {
  current: "trends" | "checkpoints";
  generationId?: string;
};

const consoleItems = [
  {
    key: "trends" as const,
    badge: "Reference Page",
    title: "参考页",
    copy: "查看当前参考摘要、来源链接和最近刷新时间，方便回看这些提示从哪里来。",
    href: "/internal/trends",
    cta: "打开参考页",
  },
  {
    key: "checkpoints" as const,
    badge: "Progress Debug",
    title: "进度排查页",
    copy: "查看当前任务最近停在哪一步、发生过哪些变化，以及能否继续恢复。",
    href: "",
    cta: "打开当前进度排查页",
  },
];

export function InternalConsoleHub({ current, generationId }: InternalConsoleHubProps) {
  const resolvedItems = consoleItems.map((item) => ({
    ...item,
    href: item.key === "checkpoints" ? `/internal/checkpoints/${generationId ?? "demo"}` : item.href,
  }));

  return (
    <section className={styles.section}>
      <div className={styles.copy}>
        <span className={styles.eyebrow}>辅助页面</span>
        <h3 className={styles.title}>这里放了两个辅助页面，方便你查看参考信息或排查进度。</h3>
        <p className={styles.lead}>正常使用主流程时通常不用进入，只有需要更多细节时再打开就好。</p>
      </div>

      <div className={styles.grid}>
        {resolvedItems.map((item) => {
          const isActive = item.key === current;
          return (
            <SpotlightCard
              className={`${styles.card} ${isActive ? styles.cardActive : ""}`}
              key={item.key}
              spotlightColor={isActive ? "rgba(232, 246, 242, 0.45)" : "rgba(255, 244, 230, 0.4)"}
            >
              <div className={styles.cardInner}>
                <span className={styles.badge}>{item.badge}</span>
                <h4 className={styles.cardTitle}>{item.title}</h4>
                <p className={styles.cardCopy}>{item.copy}</p>
                <div className={styles.metaRow}>
                  <span className={styles.metaChip}>{isActive ? "当前页" : "可跳转"}</span>
                  {item.key === "checkpoints" && generationId ? (
                    <span className={styles.metaChip}>任务编号 {generationId}</span>
                  ) : null}
                </div>
                <Link className={styles.cardLink} href={item.href}>
                  {item.cta}
                </Link>
              </div>
            </SpotlightCard>
          );
        })}
      </div>
    </section>
  );
}
