import Link from "next/link";

import { BorderGlow } from "@/components/upstream/border-glow";

import styles from "./first-run-guide.module.css";

const steps = [
  {
    index: "01",
    title: "先进入创作向导",
    copy: "从预设或五步输入开始，把主题、平台、受众和风格先锁清楚。",
    href: "/create",
    cta: "打开创建页",
  },
  {
    index: "02",
    title: "等待生成过程展开",
    copy: "生成页会持续刷新当前进度，并在完成后自动进入结果页。",
    href: "/create",
    cta: "了解主流程",
  },
  {
    index: "03",
    title: "在结果页导出或重开",
    copy: "结果页不是终点，你可以继续导出、回看参考依据，或立刻开始新一轮创作。",
    href: "/create",
    cta: "直接开始",
  },
];

export function FirstRunGuide() {
  return (
    <section className={styles.section} id="first-run-home">
      <div className={styles.copy}>
        <span className={styles.eyebrow}>新手指引</span>
        <h2 className={styles.title}>第一次来，也能很快知道接下来该怎么走。</h2>
        <p className={styles.lead}>这里把首页、创建页、生成页和结果页串成三步，方便你快速理解完整使用路径。</p>
      </div>

      <div className={styles.grid}>
        {steps.map((step) => (
          <BorderGlow
            backgroundColor="rgba(255, 252, 246, 0.96)"
            className={styles.cardShell}
            colors={["rgba(239, 124, 72, 0.88)", "rgba(63, 140, 126, 0.82)", "rgba(255, 211, 157, 0.8)"]}
            key={step.index}
          >
            <article className={styles.card}>
              <span className={styles.stepIndex}>{step.index}</span>
              <h3 className={styles.cardTitle}>{step.title}</h3>
              <p className={styles.cardCopy}>{step.copy}</p>
              <Link className={styles.cardLink} href={step.href}>
                {step.cta}
              </Link>
            </article>
          </BorderGlow>
        ))}
      </div>
    </section>
  );
}
