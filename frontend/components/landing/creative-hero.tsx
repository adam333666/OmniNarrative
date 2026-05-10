import Link from "next/link";

import { WorkflowStepper, type WorkflowStep } from "@/components/landing/workflow-stepper";
import { ConsistencyThreadShowcase } from "@/components/landing/consistency-thread-showcase";
import { FirstRunGuide } from "@/components/landing/first-run-guide";
import { HomepageResultShowcase } from "@/components/landing/homepage-result-showcase";
import { HomepageSignalNav } from "@/components/landing/homepage-signal-nav";
import { QuickstartLaunchpad } from "@/components/landing/quickstart-launchpad";
import { TrendDemoScript } from "@/components/landing/trend-demo-script";
import { TrendAmplifierShowcase } from "@/components/landing/trend-amplifier-showcase";
import { CardNav, type CardNavItem } from "@/components/upstream/card-nav";
import { CardSwap, SwapCard } from "@/components/upstream/card-swap";
import { DotGrid } from "@/components/upstream/dot-grid";
import { TextType } from "@/components/upstream/text-type";
import { GradientText } from "@/components/ui/gradient-text";
import { ShinyText } from "@/components/ui/shiny-text";
import { SpotlightCard } from "@/components/ui/spotlight-card";
import { CountUp } from "@/components/ui/count-up";

import styles from "./creative-hero.module.css";

const stats = [
  { to: 5, suffix: " 步", label: "把模糊想法整理成清晰需求" },
  { to: 5, suffix: " 部分", label: "方案覆盖标题、脚本、发布建议和制作信息" },
  { to: 3, suffix: " 种", label: "支持不同格式导出，方便继续协作和制作" },
];

const featureColumns = [
  {
    tag: "Start",
    title: "先把一句想法变成可以开工的起点",
    copy: "你不需要先准备完整提纲，只要把想做的内容说出来，就能顺着引导一步步往下走。",
    items: ["先给出清晰起点", "直接进入创作", "第一次使用也能轻松上手"],
    wide: false,
  },
  {
    tag: "Narrative",
    title: "把零散想法收成一份能继续推进的方案",
    copy: "结果会从整体方向到具体脚本逐步展开，方便你先判断方向，再决定是否继续修改或导出。",
    items: ["先看总方向", "再看脚本和镜头", "需要时再导出带走"],
    wide: true,
  },
  {
    tag: "Glue",
    title: "把复杂过程留给系统，把判断重点留给你",
    copy: "页面会尽量用直白的话说明这一步该做什么、下一步会发生什么，而不是让你去理解一套专业术语。",
    items: ["页面语言更直白", "重点信息更靠前", "先回答你最关心的问题"],
    wide: false,
  },
];

const workflowSteps: WorkflowStep[] = [
  {
    key: "input",
    label: "Input",
    title: "先把这次要做的内容讲清楚",
    description: "只要补齐主题、平台、受众和风格，后面的分析和叙事就会一直围绕这次任务展开。",
  },
  {
    key: "analysis",
    label: "Analysis",
    title: "先看参考方向，再决定怎么写",
    description: "会先整理与你这次任务相关的参考信息，避免后面只凭感觉往下写。",
  },
  {
    key: "narrative",
    label: "Narrative",
    title: "系统开始帮你长出标题、脚本和镜头",
    description: "主标题、梗概、段落脚本和关键镜头会一起成形，减少前后不一致的问题。",
  },
  {
    key: "result",
    label: "Result",
    title: "最后拿到一份能继续使用的完整方案",
    description: "你会拿到一份适合继续阅读、修改、导出和推进制作的完整方案。",
  },
  {
    key: "export",
    label: "Export",
    title: "需要带走时，直接导出就好",
    description: "需要分享、协作或继续制作时，可以直接导出，不必再手动整理。",
  },
];

const capabilityCards = [
  {
    tag: "Consistency",
    title: "整套方案会围绕同一个中心展开",
    copy: "标题、开场、脚本、镜头、封面和发布建议会尽量围绕同一个目标展开，不会各说各话。",
    accent: "线索统一",
  },
  {
    tag: "Trend",
    title: "趋势会真的影响最后写法",
    copy: "参考信息会在生成前就参与判断，不是等写完了再临时补上几句热门表达。",
    accent: "趋势导入",
  },
  {
    tag: "Heavy Result",
    title: "你拿到的不只是几句文案",
    copy: "结果会是一整套可以浏览、导出、继续制作的完整方案，而不是零散几句话。",
    accent: "结果加厚",
  },
  {
    tag: "Ease",
    title: "第一次上手也能直接开始",
    copy: "五步输入会把复杂创作拆成容易回答的小问题，让你不用准备完整大纲也能开工。",
    accent: "低门槛",
  },
];

const navItems: CardNavItem[] = [
  {
    label: "Core Flow",
    bgColor: "#1f2742",
    textColor: "#fff3ea",
    links: [
      { label: "进入创作向导", href: "/create", ariaLabel: "进入创作向导" },
      { label: "查看生成过程", href: "/create", ariaLabel: "查看生成过程" },
    ],
  },
  {
    label: "结果示例",
    bgColor: "#ef7c48",
    textColor: "#1b1920",
    links: [
      { label: "结果会包含什么", href: "/create", ariaLabel: "了解结果会包含什么" },
      { label: "查看导出方式", href: "/create", ariaLabel: "查看导出方式" },
    ],
  },
  {
    label: "辅助页面",
    bgColor: "#d8e7df",
    textColor: "#17322a",
    links: [
      { label: "参考页", href: "/internal/trends", ariaLabel: "打开参考页" },
      { label: "进度排查页", href: "/internal/checkpoints/demo", ariaLabel: "打开进度排查页" },
    ],
  },
];

export function CreativeHero() {
  return (
    <div className={styles.page}>
      <section className={styles.hero} id="hero-top">
        <div aria-hidden="true" className={styles.glowA} />
        <div aria-hidden="true" className={styles.glowB} />
        <DotGrid
          className={styles.heroGridBackdrop}
          dotSize={2}
          gap={18}
          baseColor="rgba(72, 91, 133, 0.20)"
          activeColor="#ef7c48"
          proximity={120}
          shockRadius={160}
          shockStrength={5}
          resistance={820}
          returnDuration={1.3}
        />
        <CardNav
          brand="Content Planner"
          items={navItems}
          className={styles.navBand}
          baseColor="rgba(255, 250, 243, 0.86)"
          menuColor="#1a2035"
          buttonBgColor="#1a2035"
          buttonTextColor="#fff7ef"
        />
        <div className={styles.heroLayout}>
          <div className={styles.heroInner}>
            <div className={styles.badgeRow}>
              <span className={styles.badge}>
                <span className={styles.badgeDot} />
                Start With One Idea
              </span>
              <span className={styles.badgeText}>从一句想法到一份可继续制作的方案</span>
            </div>

            <h1 className={styles.title}>
              先把你的创意
              <span className={styles.titleAccent}>
                <ShinyText pauseOnHover>讲清楚</ShinyText>
              </span>
            </h1>

            <div className={styles.typedWrap}>
              <TextType
                as="p"
                className={styles.typedLine}
                text={[
                  "先把一句想法整理成清晰方向",
                  "先看参考提示，再决定标题和开场",
                  "把结果变成可以直接带走的完整方案",
                ]}
                typingSpeed={38}
                pauseDuration={1600}
                deletingSpeed={22}
                loop
                showCursor
                cursorCharacter="_"
              />
            </div>

            <p className={styles.subtitle}>
              你先给出一个主题，系统再把平台、受众、表达重点和内容结构慢慢补齐，最后交给你一份可以直接浏览、导出和继续推进的内容方案。
            </p>

            <div className={styles.ctaRow}>
              <Link className={styles.primaryCta} href="/create">
                从一句想法开始
              </Link>
              <Link className={styles.secondaryCta} href="/create">
                直接打开五步向导
              </Link>
            </div>
          </div>

          <div className={styles.deckWrap}>
            <div className={styles.deckCaption}>
              <span className={styles.deckEyebrow}>你会得到什么</span>
              <p className={styles.deckLead}>先不用研究流程细节，这里先告诉你完成一轮后会实际拿到什么。</p>
            </div>
            <CardSwap width={340} height={238} cardDistance={34} verticalDistance={28} delay={3800} pauseOnHover>
              {capabilityCards.map((item) => (
                <SwapCard className={styles.swapCard} key={item.title}>
                  <div className={styles.swapCardInner}>
                    <span className={styles.swapTag}>{item.tag}</span>
                    <h3 className={styles.swapTitle}>{item.title}</h3>
                    <p className={styles.swapCopy}>{item.copy}</p>
                    <span className={styles.swapAccent}>{item.accent}</span>
                  </div>
                </SwapCard>
              ))}
            </CardSwap>
          </div>
        </div>
      </section>

      <section className={styles.statsGrid}>
        {stats.map((item) => (
          <article className={styles.statCard} key={item.label}>
            <p className={styles.statValue}>
              <CountUp separator="," suffix={item.suffix} to={item.to} />
            </p>
            <p className={styles.statLabel}>{item.label}</p>
          </article>
        ))}
      </section>

      <HomepageSignalNav />

      <FirstRunGuide />

      <QuickstartLaunchpad />

      <section className={styles.workflowSection} id="workflow-home">
        <WorkflowStepper steps={workflowSteps} />
      </section>

      <ConsistencyThreadShowcase />

      <TrendAmplifierShowcase />

      <TrendDemoScript />

      <HomepageResultShowcase />

      <section>
        <h2 className={styles.sectionTitle}><GradientText>Built For Structured Storytelling</GradientText></h2>
        <p className={styles.sectionLead}>
          这一版首页继续复用现有上游组件，但文案重点改成帮用户判断“我要不要从这里开始”，而不是先介绍系统自己有多完整。
        </p>
      </section>

      <section className={styles.bento}>
        {featureColumns.map((item) => (
          <SpotlightCard
            className={item.wide ? `${styles.featureCard} ${styles.featureCardWide}` : styles.featureCard}
            key={item.title}
            spotlightColor="rgba(255, 244, 230, 0.42)"
          >
            <span className={styles.featureTag}>{item.tag}</span>
            <h3 className={styles.featureTitle}>{item.title}</h3>
            <p className={styles.featureCopy}>{item.copy}</p>
            <div className={styles.featureList}>
              {item.items.map((entry) => (
                <div className={styles.featureListItem} key={entry}>
                  <span className={styles.featureListDot} />
                  <span>{entry}</span>
                </div>
              ))}
            </div>
          </SpotlightCard>
        ))}
      </section>
    </div>
  );
}
