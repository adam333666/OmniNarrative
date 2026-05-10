import { SiteShell } from "@/components/layout/site-shell";
import { ResultViewClient } from "@/components/result/result-view-client";

export default async function ResultPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <SiteShell
      eyebrow="第 3 步 / 查看结果"
      title="你的内容方案已经准备好了"
      description="先快速浏览主标题、脚本和平台建议；如果合适，就直接导出、继续制作，或者回头再开一轮新方案。"
      banner={{
        stage: "结果已生成",
        summary: "这不只是一个浏览页，而是一份你现在就能继续修改、分享、导出和推进制作的内容方案。",
        nextStep: "先判断这次方向是否合适，再决定导出、回看参考依据，还是继续开始下一轮。",
        highlights: ["先看主方案", "再看参考依据", "最后决定导出或重做"],
        actions: [
          { label: "重新开始创作", href: "/create" },
          { label: "查看参考页", href: "/internal/trends" },
        ],
      }}
    >
      <ResultViewClient generationId={id} />
    </SiteShell>
  );
}
