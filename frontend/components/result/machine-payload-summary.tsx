import styles from "./machine-payload-summary.module.css";

function describeValue(value: unknown) {
  if (Array.isArray(value)) {
    return {
      type: "array",
      preview: `共 ${value.length} 项`,
    };
  }

  if (value !== null && typeof value === "object") {
    const keys = Object.keys(value as Record<string, unknown>);
    return {
      type: "object",
      preview: keys.length > 0 ? `字段：${keys.slice(0, 3).join(" / ")}${keys.length > 3 ? " ..." : ""}` : "空对象",
    };
  }

  if (typeof value === "string") {
    return {
      type: "string",
      preview: value.length > 88 ? `${value.slice(0, 88)}...` : value,
    };
  }

  if (typeof value === "number") {
    return {
      type: "number",
      preview: String(value),
    };
  }

  if (typeof value === "boolean") {
    return {
      type: "boolean",
      preview: value ? "true" : "false",
    };
  }

  return {
    type: "unknown",
    preview: "无可用预览",
  };
}

export function MachinePayloadSummary({ payload }: { payload: Record<string, unknown> }) {
  const entries = Object.entries(payload);

  if (entries.length === 0) {
    return null;
  }

  return (
    <div className={styles.shell}>
      <div className={styles.header}>
        <p className={styles.eyebrow}>字段摘要</p>
        <h4 className={styles.title}>结构化内容摘要</h4>
      </div>

      <div className={styles.grid}>
        {entries.map(([key, value]) => {
          const meta = describeValue(value);
          return (
            <article className={styles.card} key={key}>
              <span className={styles.key}>{key}</span>
              <span className={styles.type}>{meta.type}</span>
              <p className={styles.preview}>{meta.preview}</p>
            </article>
          );
        })}
      </div>
    </div>
  );
}
