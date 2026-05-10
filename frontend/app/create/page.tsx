import { SiteShell } from "@/components/layout/site-shell";
import { CreateWizard } from "@/components/wizard/create-wizard";

type CreatePageProps = {
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
};

export default async function CreatePage({ searchParams }: CreatePageProps) {
  const resolvedParams = searchParams ? await searchParams : undefined;
  const presetValue = resolvedParams?.preset;
  const presetKey = Array.isArray(presetValue) ? presetValue[0] : presetValue;

  return (
    <SiteShell
      eyebrow="第 1 步 / 填写需求"
      title="先把这次要做的内容说清楚"
      description="按顺序补齐主题、内容类型、平台、受众和风格。每一步都只需要回答当前最关键的问题，不用一次想完所有细节。"
      banner={{
        stage: "需求填写",
        summary: "如果你现在只有一个大概方向，也可以直接开始。这一页会把它拆成五个容易回答的小问题，帮你快速进入状态。",
        nextStep: "填完后就会开始生成，你只需要等待结果出来，不必再补交额外信息。",
        highlights: ["每一步只回答一个重点", "先看参考方向再下笔", "也可以直接套用预设开始"],
        actions: [
          { label: "查看参考页", href: "/internal/trends" },
          { label: "回到首页", href: "/" },
        ],
      }}
    >
      <CreateWizard initialPresetKey={presetKey} />
    </SiteShell>
  );
}
