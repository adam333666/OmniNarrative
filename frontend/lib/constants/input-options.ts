export const contentTypes = [
  { value: "science_popularization", label: "科普型" },
  { value: "story", label: "故事型" },
  { value: "mixed", label: "混合型" },
  { value: "auto", label: "自动判断" },
] as const;

export const targetPlatforms = [
  { value: "douyin", label: "抖音" },
  { value: "kuaishou", label: "快手" },
  { value: "xiaohongshu", label: "小红书" },
  { value: "bilibili", label: "B站" },
  { value: "wechat_video", label: "视频号" },
] as const;

export const styleTones = [
  { value: "suspense", label: "悬疑" },
  { value: "healing", label: "治愈" },
  { value: "passionate", label: "热血" },
  { value: "serious", label: "严肃" },
  { value: "light", label: "轻松" },
  { value: "twist", label: "反转" },
  { value: "high_emotion", label: "高情绪" },
  { value: "calm", label: "冷静克制" },
  { value: "inspirational", label: "鼓舞" },
  { value: "mysterious", label: "神秘" },
] as const;

export const examplePrompts = [
  "我想做一个关于时间旅行悖论的内容",
  "我想做一个关于高三学生焦虑的内容",
  "我想做一个讲猫为什么会踩奶的内容",
] as const;
