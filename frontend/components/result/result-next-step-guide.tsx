import Link from "next/link";

import { BorderGlow } from "@/components/upstream/border-glow";

import styles from "./result-next-step-guide.module.css";

type ResultNextStepGuideProps = {
  generationId: string;
};

export function ResultNextStepGuide({ generationId }: ResultNextStepGuideProps) {
  const items = [
    {
      index: "A",
      title: "导出当前方案",
      copy: "如果这轮方向对了，就先把结果带走，继续发给同事、拿去评审，或直接进入后续制作。",
      href: `#markdown-preview`,
      cta: "查看导出预览",
    },
    {
      index: "B",
      title: "回看参考依据",
      copy: "如果你还在犹豫这轮为什么这样写，可以先回看参考来源和影响点，再决定要不要重开。",
      href: "/internal/trends",
      cta: "查看参考页",
    },
    {
      index: "C",
      title: "发起下一轮创作",
      copy: "如果这轮方向还差一点，就带着当前理解回到创建页，直接开下一轮，不用从零重新想。",
      href: "/create",
      cta: "重新开始",
    },
  ];

  return (
    <section className={styles.section}>
      <div className={styles.copy}>
        <span className={styles.eyebrow}>下一步</span>
        <h3 className={styles.title}>看到结果后，下一步通常只剩这三种动作。</h3>
        <p className={styles.lead}>先判断这轮方案是不是已经够用；够用就导出，不够就回看依据或直接开始下一轮。</p>
        <p className={styles.meta}>任务编号: {generationId}</p>
      </div>

      <div className={styles.grid}>
        {items.map((item) => (
          <BorderGlow
            backgroundColor="rgba(255, 251, 245, 0.95)"
            className={styles.cardShell}
            colors={["rgba(239, 124, 72, 0.88)", "rgba(63, 140, 126, 0.82)", "rgba(255, 215, 173, 0.8)"]}
            key={item.index}
          >
            <article className={styles.card}>
              <span className={styles.stepIndex}>{item.index}</span>
              <h4 className={styles.cardTitle}>{item.title}</h4>
              <p className={styles.cardCopy}>{item.copy}</p>
              <Link className={styles.cardLink} href={item.href}>
                {item.cta}
              </Link>
            </article>
          </BorderGlow>
        ))}
      </div>
    </section>
  );
}
