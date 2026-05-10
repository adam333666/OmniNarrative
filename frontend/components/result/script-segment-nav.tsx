import styles from "./script-segment-nav.module.css";

export function ScriptSegmentNav({
  segments,
}: {
  segments: Array<{ segment_number: number; segment_title: string }>;
}) {
  return (
    <div className={styles.shell}>
      <div className={styles.header}>
        <p className={styles.eyebrow}>Script Navigator</p>
        <h4 className={styles.title}>段落快速导航</h4>
      </div>

      <div className={styles.grid}>
        {segments.map((segment) => (
          <a className={styles.card} href={`#script-segment-${segment.segment_number}`} key={segment.segment_number}>
            <span className={styles.index}>段落 {segment.segment_number}</span>
            <span className={styles.cardTitle}>{segment.segment_title}</span>
            <span className={styles.linkText}>跳转查看</span>
          </a>
        ))}
      </div>
    </div>
  );
}
