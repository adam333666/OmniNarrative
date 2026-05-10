import styles from "./analysis-summary.module.css";

export function AnalysisSummary({
  trendSummary,
  audienceRawText,
  ageGroupGuess,
  interestTags,
}: {
  trendSummary: string;
  audienceRawText: string;
  ageGroupGuess: string;
  interestTags: string[];
}) {
  return (
    <div className={styles.stack}>
      <article className={styles.featureCard}>
        <span className={styles.label}>参考摘要</span>
        <p className={styles.featureValue}>{trendSummary}</p>
      </article>

      <div className={styles.grid}>
        <article className={styles.card}>
          <span className={styles.label}>你填写的受众</span>
          <p className={styles.value}>{audienceRawText}</p>
        </article>

        <article className={styles.card}>
          <span className={styles.label}>大致年龄</span>
          <p className={styles.value}>{ageGroupGuess}</p>
        </article>
      </div>

      <div className={styles.tagSection}>
        <span className={styles.label}>兴趣点</span>
        <div className={styles.tagWrap}>
          {interestTags.map((item) => (
            <span className={styles.tag} key={item}>
              {item}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
