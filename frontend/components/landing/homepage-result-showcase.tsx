import Link from "next/link";

import { ChromaGrid, type ChromaGridItem } from "@/components/upstream/chroma-grid";

import styles from "./homepage-result-showcase.module.css";

const showcaseItems: ChromaGridItem[] = [
  {
    title: "总览定位卡",
    subtitle: "一句话主题、平台定位、受众摘要和风格总结会先收在同一页，方便你快速判断方向。",
    handle: "Overview",
    location: "结果总览层",
    borderColor: "rgba(239, 124, 72, 0.62)",
    gradient: "linear-gradient(145deg, rgba(29, 20, 17, 0.98), rgba(89, 43, 29, 0.94))",
    preview: "主标题\n一句话总结\n内容定位\n风格摘要",
    url: "/create",
  },
  {
    title: "叙事脚本卡",
    subtitle: "段落目标、旁白、字幕、画面和节奏会被整理出来，不只是给你一句笼统概述。",
    handle: "Script",
    location: "脚本层",
    borderColor: "rgba(76, 144, 128, 0.62)",
    gradient: "linear-gradient(145deg, rgba(17, 33, 33, 0.98), rgba(28, 77, 69, 0.95))",
    preview: "段落 1\n目标\n旁白\n字幕\n画面提示",
    url: "/create",
  },
  {
    title: "传播策略卡",
    subtitle: "标题封面、评论引导、发布时间和发布角度会继续补齐，方便你直接拿去用。",
    handle: "Distribution",
    location: "平台层",
    borderColor: "rgba(235, 203, 126, 0.68)",
    gradient: "linear-gradient(145deg, rgba(36, 27, 16, 0.98), rgba(97, 76, 27, 0.94))",
    preview: "标题备选\n封面文案\n评论引导\n发布时间\n分发角度",
    url: "/create",
  },
  {
    title: "导出方式卡",
    subtitle: "结果不会只停留在页面里，你还可以按不同格式导出，方便协作和继续制作。",
    handle: "Export",
    location: "导出层",
    borderColor: "rgba(182, 160, 255, 0.62)",
    gradient: "linear-gradient(145deg, rgba(24, 22, 36, 0.98), rgba(66, 51, 112, 0.94))",
    preview: "Markdown\nJSON\n视频制作内容\n完整结果",
    url: "/create",
  },
];

export function HomepageResultShowcase() {
  return (
    <section className={styles.section} id="result-showcase-home">
      <div className={styles.copy}>
        <span className={styles.eyebrow}>结果预览</span>
        <h2 className={styles.title}>开始之前，先看看一轮完成后大概会得到什么。</h2>
        <p className={styles.lead}>这样你在进入创建页前，就能先知道结果会覆盖哪些信息，以及哪些内容可以直接带走继续用。</p>
        <div className={styles.actions}>
          <Link className={styles.primaryCta} href="/create">
            进入创作并生成样例
          </Link>
          <Link className={styles.secondaryCta} href="/internal/trends">
            查看参考页
          </Link>
        </div>
      </div>

      <div className={styles.gridShell}>
        <ChromaGrid items={showcaseItems} columns={2} radius={260} />
      </div>
    </section>
  );
}
