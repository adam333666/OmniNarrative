import { SiteShell } from "@/components/layout/site-shell";
import { CreativeHero } from "@/components/landing/creative-hero";

export default function HomePage() {
  return (
    <SiteShell
      eyebrow="从一句想法开始"
      title="把一个想法整理成能直接开工的内容方案"
      description="先说清主题，再补一点平台、受众和风格线索，系统会把它整理成可查看、可导出、可继续制作的结果。"
    >
      <CreativeHero />
    </SiteShell>
  );
}
