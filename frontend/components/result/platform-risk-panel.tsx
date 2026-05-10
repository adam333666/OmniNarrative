import styles from "./platform-risk-panel.module.css";

export function PlatformRiskPanel({
  avoidPatterns,
}: {
  avoidPatterns: string[];
}) {
  return (
    <div className={styles.shell}>
      <div className={styles.header}>
        <p className={styles.eyebrow}>Risk Focus</p>
        <h4 className={styles.title}>平台风险提示</h4>
      </div>

      <div className={styles.grid}>
        {avoidPatterns.map((item, index) => (
          <article className={styles.card} key={item}>
            <span className={styles.index}>注意事项 {index + 1}</span>
            <p className={styles.value}>{item}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
