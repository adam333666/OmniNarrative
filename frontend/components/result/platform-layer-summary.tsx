import styles from "./platform-layer-summary.module.css";

const platformFields = [
  { key: "platform_strategy", label: "平台建议" },
  { key: "audience_adaptation", label: "受众建议" },
  { key: "hook_design_reason", label: "开场理由" },
  { key: "rhythm_structure_reason", label: "节奏理由" },
  { key: "publishing_copy_suggestion", label: "发布文案" },
] as const;

export function PlatformLayerSummary({
  platformLayer,
}: {
  platformLayer: Record<string, unknown>;
}) {
  return (
    <div className={styles.shell}>
      <div className={styles.grid}>
        {platformFields.map((field) => (
          <article className={styles.card} key={field.key}>
            <span className={styles.label}>{field.label}</span>
            <p className={styles.value}>{String(platformLayer[field.key] ?? "")}</p>
          </article>
        ))}
      </div>
    </div>
  );
}
