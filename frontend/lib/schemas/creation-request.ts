import { z } from "zod";

export const creationRequestSchema = z.object({
  theme_text: z.string().trim().min(1, "请先输入主题").max(500, "主题内容过长"),
  content_type: z.enum(["science_popularization", "story", "mixed", "auto"]),
  target_platform: z.enum(["douyin", "kuaishou", "xiaohongshu", "bilibili", "wechat_video"]),
  target_audience_text: z.string().trim().min(1, "请先输入目标受众").max(500, "受众描述过长"),
  style_tone: z.enum([
    "suspense",
    "healing",
    "passionate",
    "serious",
    "light",
    "twist",
    "high_emotion",
    "calm",
    "inspirational",
    "mysterious",
  ]),
  custom_style_text: z.string().trim().max(300, "自定义补充过长").optional().or(z.literal("")),
});

export type CreationRequestInput = z.infer<typeof creationRequestSchema>;
