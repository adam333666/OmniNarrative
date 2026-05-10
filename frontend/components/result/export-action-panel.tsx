import styles from "./export-action-panel.module.css";

const exportItems = [
  {
    key: "json",
    eyebrow: "Structured",
    title: "导出 JSON",
    description: "保留完整字段，适合继续给工具、流程或脚本使用。",
    cta: "打开 JSON",
    tone: "primary",
  },
  {
    key: "markdown",
    eyebrow: "Readable",
    title: "导出 Markdown",
    description: "生成更适合阅读和讨论的文本版本，便于内容评审、分享与内部协作。",
    cta: "打开 Markdown",
    tone: "secondary",
  },
  {
    key: "video",
    eyebrow: "Executable",
    title: "查看 Video Payload",
    description: "查看更适合继续进入视频制作流程的结构化内容。",
    cta: "打开内容",
    tone: "secondary",
  },
] as const;

export function ExportActionPanel({
  jsonUrl,
  markdownUrl,
  videoPayloadUrl,
}: {
  jsonUrl: string;
  markdownUrl: string;
  videoPayloadUrl: string;
}) {
  const hrefMap = {
    json: jsonUrl,
    markdown: markdownUrl,
    video: videoPayloadUrl,
  } as const;

  return (
    <div className={styles.stack}>
      {exportItems.map((item) => (
        <article className={styles.card} data-tone={item.tone} key={item.key}>
          <div className={styles.copy}>
            <span className={styles.eyebrow}>{item.eyebrow}</span>
            <h4 className={styles.title}>{item.title}</h4>
            <p className={styles.description}>{item.description}</p>
          </div>
          <a className={styles.cta} href={hrefMap[item.key]} rel="noreferrer" target="_blank">
            {item.cta}
          </a>
        </article>
      ))}
    </div>
  );
}
