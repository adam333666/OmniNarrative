import styles from "./script-summary-strip.module.css";

export function ScriptSummaryStrip({
  segments,
}: {
  segments: Array<{
    segment_number: number;
    segment_title: string;
    segment_goal: string;
    emotion: string;
    rhythm: string;
  }>;
}) {
  return (
    <div className={styles.grid}>
      {segments.map((segment) => (
        <a className={styles.card} href={`#script-segment-${segment.segment_number}`} key={segment.segment_number}>
          <div className={styles.header}>
            <span className={styles.index}>段落 {segment.segment_number}</span>
            <span className={styles.tempo}>{segment.emotion} / {segment.rhythm}</span>
          </div>
          <h4 className={styles.title}>{segment.segment_title}</h4>
          <p className={styles.goal}>{segment.segment_goal}</p>
          <span className={styles.linkText}>查看完整段落</span>
        </a>
      ))}
    </div>
  );
}
