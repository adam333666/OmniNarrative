import styles from "./overview-summary.module.css";

const overviewFields = [
  { key: "target_platform", label: "平台目标" },
  { key: "content_positioning", label: "内容定位" },
  { key: "style_summary", label: "风格摘要" },
] as const;

export function OverviewSummary({
  overview,
}: {
  overview: Record<string, unknown>;
}) {
  return (
    <div className={styles.grid}>
      {overviewFields.map((field) => (
        <article className={styles.card} key={field.key}>
          <span className={styles.label}>{field.label}</span>
          <p className={styles.value}>{String(overview[field.key] ?? "")}</p>
        </article>
      ))}
    </div>
  );
}
