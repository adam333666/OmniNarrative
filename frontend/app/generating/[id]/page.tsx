import { SiteShell } from "@/components/layout/site-shell";
import { GenerationStatusClient } from "@/components/generation/generation-status-client";

export default async function GeneratingPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  return (
    <SiteShell
      eyebrow="第 2 步 / 生成中"
      title="你的方案正在生成"
      description="这一页会持续刷新真实进度。你不用反复返回查看，完成后会自动跳到结果页。"
      banner={{
        stage: "生成进度",
        summary: "这一步你只需要关注两件事：现在进行到哪里了，以及什么时候可以直接查看结果。",
        nextStep: "完成后会自动进入结果页，你可以马上浏览方案、导出内容，或者继续开始下一轮。",
        highlights: ["实时刷新当前进度", "完成后自动进入结果页", "失败时会显示当前卡在哪一步"],
        actions: [
          { label: "回到创建页", href: "/create" },
          { label: "回到首页", href: "/" },
        ],
      }}
    >
      <GenerationStatusClient generationId={id} />
    </SiteShell>
  );
}
