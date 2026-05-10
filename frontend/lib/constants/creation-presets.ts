import type { CreationRequestInput } from "@/lib/schemas/creation-request";

export type CreationPreset = {
  key: string;
  tag: string;
  title: string;
  summary: string;
  accent: string;
  payload: CreationRequestInput;
};

export const creationPresets: CreationPreset[] = [
  {
    key: "bilibili-science",
    tag: "Science",
    title: "B站科普拆解",
    summary: "适合把一个信息密度高的主题整理成更容易看懂、也更容易继续展开讨论的科普内容。",
    accent: "Knowledge-first launch",
    payload: {
      theme_text: "我想做一个关于时间旅行悖论为什么总让人越想越上头的内容",
      content_type: "science_popularization",
      target_platform: "bilibili",
      target_audience_text: "对科幻、知识拆解和世界观讨论感兴趣的18到30岁用户",
      style_tone: "mysterious",
      custom_style_text: "保持设问感和完整解释链，避免过度中二化。",
    },
  },
  {
    key: "xiaohongshu-healing",
    tag: "Healing",
    title: "小红书治愈陪伴",
    summary: "适合把一个生活议题整理成更有共鸣、也更适合收藏和分享的陪伴型内容。",
    accent: "Soft emotional resonance",
    payload: {
      theme_text: "我想做一个关于为什么长大后越来越难交到真朋友的内容",
      content_type: "story",
      target_platform: "xiaohongshu",
      target_audience_text: "刚工作不久、在大城市生活、对情绪共鸣和关系议题敏感的年轻用户",
      style_tone: "healing",
      custom_style_text: "语气要温柔但不鸡汤，更像一个很懂你的陪伴型表达。",
    },
  },
  {
    key: "douyin-high-emotion",
    tag: "Impact",
    title: "抖音高情绪开场",
    summary: "适合把一个冲突感强的话题整理成开场更抓人、后续节奏推进更快的短内容。",
    accent: "High-speed attention hook",
    payload: {
      theme_text: "我想做一个关于为什么越努力的人有时候反而越焦虑的内容",
      content_type: "mixed",
      target_platform: "douyin",
      target_audience_text: "节奏快、容易共鸣于自我要求和压力议题的年轻用户",
      style_tone: "high_emotion",
      custom_style_text: "开场要有冲击力，但中段要给出能被带走的判断和方法。",
    },
  },
];

export const creationPresetMap = Object.fromEntries(creationPresets.map((preset) => [preset.key, preset] as const));
