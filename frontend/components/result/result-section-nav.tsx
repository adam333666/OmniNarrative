import { PillNav, type PillNavItem } from "@/components/upstream/pill-nav";

const sections: PillNavItem[] = [
  { href: "#overview-layer", label: "整体方向" },
  { href: "#markdown-preview", label: "文本预览" },
  { href: "#script-layer", label: "脚本内容" },
  { href: "#platform-layer", label: "发布建议" },
  { href: "#multimodal-layer", label: "制作信息" },
  { href: "#machine-layer", label: "完整字段" },
];

export function ResultSectionNav() {
  return <PillNav brand="结果导航" items={sections} activeHref="#overview-layer" />;
}
