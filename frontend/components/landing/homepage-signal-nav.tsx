"use client";

import { GooeyNav } from "@/components/upstream/gooey-nav";

import styles from "./homepage-signal-nav.module.css";

const items = [
  { label: "方案如何保持统一", href: "#consistency-thread-home" },
  { label: "参考信息怎么帮助创作", href: "#trend-amplifier-home" },
  { label: "一轮使用怎么走", href: "#trend-demo-home" },
  { label: "结果会包含什么", href: "#workflow-home" },
  { label: "立即开始", href: "#hero-top" },
];

export function HomepageSignalNav() {
  return (
    <section className={styles.wrapper}>
      <div className={styles.copyBlock}>
        <span className={styles.eyebrow}>页面导航</span>
        <p className={styles.lead}>如果你想先快速浏览重点，可以直接从这里跳到自己最关心的部分。</p>
      </div>
      <div className={styles.shell}>
        <GooeyNav items={items} />
      </div>
    </section>
  );
}
