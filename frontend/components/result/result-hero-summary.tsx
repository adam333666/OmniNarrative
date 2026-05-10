import styles from "./result-hero-summary.module.css";

const heroSummaryFields = [
  { key: "themeText", label: "主题" },
  { key: "targetPlatform", label: "平台" },
  { key: "contentPositioning", label: "内容方向" },
  { key: "styleSummary", label: "风格" },
] as const;

export function ResultHeroSummary({
  themeText,
  targetPlatform,
  contentPositioning,
  styleSummary,
}: {
  themeText: string;
  targetPlatform: string;
  contentPositioning: string;
  styleSummary: string;
}) {
  const values = {
    themeText,
    targetPlatform,
    contentPositioning,
    styleSummary,
  } as const;

  return (
    <div className={styles.grid}>
      {heroSummaryFields.map((field) => (
        <article className={styles.card} key={field.key}>
          <span className={styles.label}>{field.label}</span>
          <p className={styles.value}>{values[field.key]}</p>
        </article>
      ))}
    </div>
  );
}
