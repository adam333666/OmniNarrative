import styles from "./payload-foldout-header.module.css";

export function PayloadFoldoutHeader({
  eyebrow,
  title,
  description,
  entryCount,
  sourceLabel,
}: {
  eyebrow: string;
  title: string;
  description: string;
  entryCount: number;
  sourceLabel: string;
}) {
  return (
    <div className={styles.shell}>
      <div className={styles.copy}>
        <p className={styles.eyebrow}>{eyebrow}</p>
        <h4 className={styles.title}>{title}</h4>
        <p className={styles.description}>{description}</p>
      </div>

      <div className={styles.metaGrid}>
        <div className={styles.metaCard}>
          <span className={styles.metaLabel}>内容项</span>
          <span className={styles.metaValue}>{entryCount} 项</span>
        </div>
        <div className={styles.metaCard}>
          <span className={styles.metaLabel}>数据来源</span>
          <span className={styles.metaValue}>{sourceLabel}</span>
        </div>
        <div className={styles.metaCard}>
          <span className={styles.metaLabel}>查看方式</span>
          <span className={styles.metaValue}>展开查看摘要与原始内容</span>
        </div>
      </div>
    </div>
  );
}
