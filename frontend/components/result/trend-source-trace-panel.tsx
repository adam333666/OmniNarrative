"use client";

import styles from "./trend-source-trace-panel.module.css";

type TrendSourceTracePanelProps = {
  items: Array<{
    title: string;
    link: string | null;
    excerpt: string;
    source_name: string;
  }>;
};

export function TrendSourceTracePanel({ items }: TrendSourceTracePanelProps) {
  if (items.length === 0) {
    return null;
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <div>
          <span className={styles.eyebrow}>参考来源</span>
          <h4 className={styles.title}>这次方案参考了哪些外部内容，你可以在这里继续回看。</h4>
        </div>
        <span className={styles.meta}>{items.length} 条来源</span>
      </div>

      <div className={styles.grid}>
        {items.slice(0, 3).map((item) => (
          <article className={styles.card} key={`${item.source_name}-${item.title}`}>
            <span className={styles.source}>{item.source_name}</span>
            <h5 className={styles.cardTitle}>
              {item.link ? (
                <a className={styles.link} href={item.link} rel="noreferrer" target="_blank">
                  {item.title}
                </a>
              ) : (
                item.title
              )}
            </h5>
            <p className={styles.excerpt}>{item.excerpt}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
