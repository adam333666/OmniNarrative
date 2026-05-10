import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { InternalConsoleHub } from "@/components/internal/internal-console-hub";
import { SiteShell } from "@/components/layout/site-shell";
import { CardSwap, SwapCard } from "@/components/upstream/card-swap";
import { SpotlightCard } from "@/components/ui/spotlight-card";

import styles from "./page.module.css";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";
const INTERNAL_API_KEY = process.env.INTERNAL_API_KEY ?? "";

const PLATFORM_LABELS: Record<string, string> = {
  bilibili: "B站",
  douyin: "抖音",
  kuaishou: "快手",
  xiaohongshu: "小红书",
  wechat_video: "视频号",
};

type TrendSummaryItem = {
  platform: string;
  content_type: string;
  summary: string;
  source_type: string;
  updated_at: string | null;
  hot_topics_summary: string[];
  source_trace: Array<{
    title: string;
    link: string | null;
    excerpt: string;
    source_name: string;
  }>;
  configured_sources: Array<{
    source_kind: string;
    display_name: string;
    target: string;
    enabled: boolean;
    status: string;
    rationale: string;
  }>;
};

type PlatformTrendSummary = {
  platform: string;
  items: TrendSummaryItem[];
  total: number;
  generated_at: string;
};

type FetchState<T> = {
  data: T | null;
  error: string | null;
};

async function readErrorMessage(response: Response, fallbackMessage: string): Promise<string> {
  const contentType = response.headers.get("content-type") ?? "";

  if (contentType.includes("application/json")) {
    try {
      const payload = (await response.json()) as { detail?: unknown };
      if (typeof payload.detail === "string" && payload.detail.trim()) {
        return payload.detail;
      }
    } catch {
      return fallbackMessage;
    }
  }

  try {
    const text = await response.text();
    return text.trim() || fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}

async function fetchPlatformSummary(platform: string): Promise<FetchState<PlatformTrendSummary>> {
  if (!INTERNAL_API_KEY) {
    return { data: null, error: null };
  }

  const response = await fetch(`${API_BASE_URL}/internal/trend-summary/${platform}`, {
    cache: "no-store",
    headers: {
      "X-Internal-Api-Key": INTERNAL_API_KEY,
    },
  });

  if (response.status === 404) {
    return { data: null, error: null };
  }

  if (!response.ok) {
    return {
      data: null,
      error: await readErrorMessage(response, `趋势摘要加载失败: ${platform}`),
    };
  }

  return {
    data: (await response.json()) as PlatformTrendSummary,
    error: null,
  };
}

async function refreshTrendsAction() {
  "use server";

  if (!INTERNAL_API_KEY) {
    redirect("/internal/trends?action_error=INTERNAL_API_KEY%20is%20not%20configured%20for%20the%20internal%20trend%20console.");
  }

  const response = await fetch(`${API_BASE_URL}/internal/trend-refresh`, {
    method: "POST",
    cache: "no-store",
    headers: {
      "X-Internal-Api-Key": INTERNAL_API_KEY,
    },
  });

  if (!response.ok) {
    const errorMessage = await readErrorMessage(response, "趋势刷新失败。");
    redirect(`/internal/trends?action_error=${encodeURIComponent(errorMessage)}`);
  }

  revalidatePath("/internal/trends");
  redirect("/internal/trends?action_success=%E8%B6%8B%E5%8A%BF%E5%88%B7%E6%96%B0%E5%B7%B2%E5%AE%8C%E6%88%90%E3%80%82");
}

function formatDate(value: string | null): string {
  if (!value) {
    return "未记录";
  }

  try {
    return new Intl.DateTimeFormat("zh-CN", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(value));
  } catch {
    return value;
  }
}

export default async function InternalTrendConsolePage({
  searchParams,
}: {
  searchParams?: Promise<{ action_error?: string; action_success?: string }>;
}) {
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const actionError = resolvedSearchParams.action_error ?? null;
  const actionSuccess = resolvedSearchParams.action_success ?? null;
  const platforms = Object.keys(PLATFORM_LABELS);
  const summaries = await Promise.all(platforms.map((platform) => fetchPlatformSummary(platform)));
  const connectedPlatforms = summaries.filter((item) => item.data?.items?.[0]).length;
  const loadErrors = summaries.flatMap((item) => (item.error ? [item.error] : []));
  const sourceDeck = [
    {
      tag: "Entry",
      title: "订阅来源",
      copy: "优先从稳定来源读取近期内容，方便更快拿到当前平台的参考方向。",
      accent: `${connectedPlatforms} 个平台已接入摘要读取`,
    },
    {
      tag: "Collect",
      title: "补充采集",
      copy: "当现成来源不足时，会补充抓取公开内容，尽量保证参考信息不断档。",
      accent: "页面级内容采集兜底",
    },
    {
      tag: "Structure",
      title: "摘要整理",
      copy: "最后把外部内容整理成更容易直接使用的提示，方便进入后续创作。",
      accent: "整理后可直接参考",
    },
  ];

  return (
    <SiteShell
      eyebrow="辅助页面 / 参考页"
      title="参考页"
      description="这里会集中展示当前可参考的平台摘要、来源链接和最近更新时间，方便你继续核对。"
    >
      <div className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroCopy}>
            <span className={styles.heroBadge}>参考来源总览</span>
            <h2 className={styles.heroTitle}>把当前能参考的信息、来源和更新时间放到同一页里。</h2>
            <p className={styles.heroLead}>如果你想进一步确认这些提示从哪里来、最近有没有更新，可以在这里统一查看。</p>
          </div>

          <form action={refreshTrendsAction} className={styles.refreshForm}>
            <button className={styles.refreshButton} type="submit">
              手动刷新参考信息
            </button>
            <p className={styles.refreshHint}>刷新后会重新读取当前平台的摘要和来源信息。</p>
          </form>
        </section>

        <section className={styles.deckSection}>
          <div className={styles.deckCopy}>
            <span className={styles.deckBadge}>信息怎么来</span>
            <h3 className={styles.deckTitle}>这里简单说明参考信息是怎样被收集、补充和整理出来的。</h3>
            <p className={styles.deckLead}>你不需要记住实现方式，只要知道这些提示不是凭空出现的即可。</p>
          </div>

          <div className={styles.deckSurface}>
            <CardSwap width={320} height={220} cardDistance={28} verticalDistance={24} delay={3600} pauseOnHover>
              {sourceDeck.map((item) => (
                <SwapCard className={styles.swapCard} key={item.title}>
                  <div className={styles.swapCardInner}>
                    <span className={styles.swapTag}>{item.tag}</span>
                    <h4 className={styles.swapTitle}>{item.title}</h4>
                    <p className={styles.swapCopy}>{item.copy}</p>
                    <span className={styles.swapAccent}>{item.accent}</span>
                  </div>
                </SwapCard>
              ))}
            </CardSwap>
          </div>
        </section>

        {!INTERNAL_API_KEY ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(255, 224, 214, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>当前未配置内部 API Key</h3>
              <p className={styles.sectionLead}>当前环境还没有开启这页所需的内部访问权限，所以暂时无法读取更详细的参考信息。</p>
            </div>
          </SpotlightCard>
        ) : null}

        {loadErrors.length > 0 ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(255, 224, 214, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>参考页暂时不可用</h3>
              <p className={styles.sectionLead}>{loadErrors[0]}</p>
            </div>
          </SpotlightCard>
        ) : null}

        {actionError ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(255, 224, 214, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>刷新未完成</h3>
              <p className={styles.sectionLead}>{actionError}</p>
            </div>
          </SpotlightCard>
        ) : null}

        {actionSuccess ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(232, 246, 242, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>刷新已完成</h3>
              <p className={styles.sectionLead}>{actionSuccess}</p>
            </div>
          </SpotlightCard>
        ) : null}

        <InternalConsoleHub current="trends" />

        <section className={styles.summaryGrid}>
          {summaries.map((summary, index) => {
            const platform = platforms[index];
            const label = PLATFORM_LABELS[platform];
            const primaryItem = summary.data?.items[0];

            return (
              <SpotlightCard className={styles.summaryCard} key={platform} spotlightColor="rgba(255, 244, 230, 0.4)">
                <div className={styles.summaryInner}>
                  <div className={styles.summaryHeader}>
                    <div>
                      <span className={styles.platformBadge}>{label}</span>
                      <h3 className={styles.platformTitle}>{platform}</h3>
                    </div>
                      <span className={styles.metaChip}>{primaryItem?.source_type ?? "暂无来源"}</span>
                  </div>

                  <p className={styles.platformLead}>{primaryItem?.summary ?? "当前暂无可参考摘要。"}
                  </p>

                  <div className={styles.metaList}>
                    <span className={styles.metaItem}>摘要数 {summary.data?.total ?? 0}</span>
                    <span className={styles.metaItem}>更新时间 {formatDate(primaryItem?.updated_at ?? null)}</span>
                  </div>

                  <div className={styles.topicWrap}>
                    {(primaryItem?.hot_topics_summary ?? []).map((topic) => (
                      <span className={styles.topicChip} key={topic}>
                        {topic}
                      </span>
                    ))}
                  </div>

                  {(primaryItem?.configured_sources ?? []).length > 0 ? (
                    <div className={styles.configSection}>
                      <div className={styles.traceHeader}>
                        <h4 className={styles.traceTitle}>来源配置</h4>
                        <span className={styles.traceHint}>当前平台启用的参考来源</span>
                      </div>

                      <div className={styles.configList}>
                        {(primaryItem?.configured_sources ?? []).map((source) => (
                          <article className={styles.configItem} key={`${source.source_kind}-${source.display_name}-${source.target}`}>
                            <div className={styles.configHeader}>
                              <span className={styles.configKind}>{source.source_kind}</span>
                              <span className={source.enabled ? styles.configStatusActive : styles.configStatusBlocked}>
                                {source.status}
                              </span>
                            </div>
                            <h5 className={styles.configTitle}>{source.display_name}</h5>
                            <p className={styles.configTarget}>{source.target}</p>
                            <p className={styles.configRationale}>{source.rationale}</p>
                          </article>
                        ))}
                      </div>
                    </div>
                  ) : null}

                  {(primaryItem?.source_trace ?? []).length > 0 ? (
                    <div className={styles.traceSection}>
                      <div className={styles.traceHeader}>
                        <h4 className={styles.traceTitle}>来源列表</h4>
                        <span className={styles.traceHint}>这些摘要当前参考了以下内容</span>
                      </div>

                      <div className={styles.traceList}>
                        {(primaryItem?.source_trace ?? []).slice(0, 3).map((trace) => (
                          <article className={styles.traceItem} key={`${trace.source_name}-${trace.title}`}>
                            <span className={styles.traceSource}>{trace.source_name}</span>
                            <h5 className={styles.traceItemTitle}>
                              {trace.link ? (
                                <a className={styles.traceLink} href={trace.link} rel="noreferrer" target="_blank">
                                  {trace.title}
                                </a>
                              ) : (
                                trace.title
                              )}
                            </h5>
                            <p className={styles.traceExcerpt}>{trace.excerpt}</p>
                          </article>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              </SpotlightCard>
            );
          })}
        </section>
      </div>
    </SiteShell>
  );
}
