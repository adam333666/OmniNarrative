import Link from "next/link";

import { BorderGlow } from "@/components/upstream/border-glow";

import styles from "./trend-demo-script.module.css";

const steps = [
  {
    index: "01",
    title: "先看参考信息会怎么帮你判断",
    body: "首页会先说明这些参考信息会在哪些地方帮你做判断，让你知道结果不是只靠一句主题直接展开。",
    href: "#trend-amplifier-home",
    cta: "定位首页趋势链",
  },
  {
    index: "02",
    title: "再到创建页看看当前参考方向",
    body: "创建页会先给出与你所选平台相关的参考提示，帮助你决定标题、开场和表达重点。",
    href: "/create",
    cta: "打开创建页",
  },
  {
    index: "03",
    title: "结果页回看这些参考是怎么影响方案的",
    body: "结果页会继续告诉你，这些参考信息最终改变了哪些写法、节奏和发布建议。",
    href: "/create",
    cta: "进入主流程验证",
  },
  {
    index: "04",
    title: "需要时再打开参考页查看更多细节",
    body: "如果你想继续核对来源和更新时间，也可以打开参考页查看更详细的信息。",
    href: "/internal/trends",
    cta: "打开参考页",
  },
];

export function TrendDemoScript() {
  return (
    <section className={styles.section} id="trend-demo-home">
      <div className={styles.copy}>
        <span className={styles.eyebrow}>使用示例</span>
        <h2 className={styles.title}>如果你想看清一轮创作里参考信息是怎么参与进来的，可以按这四步走。</h2>
        <p className={styles.lead}>这样看会更容易理解，为什么最后拿到的方案会更贴近平台表达和用户阅读习惯。</p>
      </div>

      <div className={styles.grid}>
        {steps.map((step) => (
          <BorderGlow
            backgroundColor="rgba(255, 252, 246, 0.96)"
            className={styles.cardShell}
            colors={["rgba(239, 124, 72, 0.88)", "rgba(63, 140, 126, 0.82)", "rgba(255, 214, 173, 0.82)"]}
            key={step.index}
          >
            <article className={styles.card}>
              <span className={styles.index}>{step.index}</span>
              <h3 className={styles.cardTitle}>{step.title}</h3>
              <p className={styles.cardBody}>{step.body}</p>
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
