import { revalidatePath } from "next/cache";
import Link from "next/link";
import { redirect } from "next/navigation";

import { InternalConsoleHub } from "@/components/internal/internal-console-hub";
import { SiteShell } from "@/components/layout/site-shell";
import { SpotlightCard } from "@/components/ui/spotlight-card";

import styles from "./page.module.css";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";
const INTERNAL_API_KEY = process.env.INTERNAL_API_KEY ?? "";

type CheckpointItem = {
  checkpoint_id: string | null;
  checkpoint_ns: string;
  thread_id: string | null;
  created_at: string | null;
  channel_keys: string[];
  metadata: Record<string, unknown>;
  pending_write_count: number;
};

type CheckpointListResponse = {
  generation_id: string;
  total: number;
  items: CheckpointItem[];
};

type CheckpointStateResponse = {
  generation_id: string;
  checkpoint_id: string | null;
  checkpoint_ns: string;
  thread_id: string | null;
  created_at: string | null;
  channel_keys: string[];
  metadata: Record<string, unknown>;
  has_result: boolean;
  result_title: string | null;
  result_summary: string | null;
  script_segment_count: number;
  failure_attribution: {
    category: string;
    stage: string | null;
    stage_message: string | null;
    latest_event_type: string | null;
    latest_error_message: string | null;
    recovery_hint: string;
    can_restore_result_snapshot: boolean;
  };
};

type DiagnosticsResponse = {
  generation_id: string;
  status_snapshot: {
    status: string;
    current_stage: string;
    stage_message: string;
    error_message: string | null;
    total_elapsed_seconds: number | null;
    stage_elapsed_seconds: number | null;
  };
  has_result_snapshot: boolean;
  event_count: number;
  events: Array<{
    generation_id: string;
    event_type: string;
    status: string;
    stage: string;
    stage_message: string;
    error_message: string | null;
    occurred_at: string;
  }>;
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

async function fetchCheckpointList(generationId: string): Promise<FetchState<CheckpointListResponse>> {
  if (!INTERNAL_API_KEY) {
    return { data: null, error: null };
  }

  const response = await fetch(`${API_BASE_URL}/internal/generation-checkpoints/${generationId}`, {
    cache: "no-store",
    headers: {
      "X-Internal-Api-Key": INTERNAL_API_KEY,
    },
  });

  if (response.status === 404) {
    const detail = await readErrorMessage(response, "Checkpoint 列表不存在。");
    if (detail.includes("Generation not found")) {
      return { data: null, error: detail };
    }
    return { data: null, error: null };
  }

  if (!response.ok) {
    return {
      data: null,
      error: await readErrorMessage(response, "Checkpoint 列表加载失败。"),
    };
  }

  return {
    data: (await response.json()) as CheckpointListResponse,
    error: null,
  };
}

async function fetchLatestState(generationId: string): Promise<FetchState<CheckpointStateResponse>> {
  if (!INTERNAL_API_KEY) {
    return { data: null, error: null };
  }

  const response = await fetch(`${API_BASE_URL}/internal/generation-checkpoints/${generationId}/latest-state`, {
    cache: "no-store",
    headers: {
      "X-Internal-Api-Key": INTERNAL_API_KEY,
    },
  });

  if (response.status === 404) {
    const detail = await readErrorMessage(response, "Checkpoint 状态不存在。");
    if (detail.includes("Generation not found")) {
      return { data: null, error: detail };
    }
    return { data: null, error: null };
  }

  if (!response.ok) {
    return {
      data: null,
      error: await readErrorMessage(response, "Checkpoint 状态加载失败。"),
    };
  }

  return {
    data: (await response.json()) as CheckpointStateResponse,
    error: null,
  };
}

async function fetchDiagnostics(generationId: string): Promise<FetchState<DiagnosticsResponse>> {
  if (!INTERNAL_API_KEY) {
    return { data: null, error: null };
  }

  const response = await fetch(`${API_BASE_URL}/creations/${generationId}/diagnostics?limit=12`, {
    cache: "no-store",
    headers: {
      "X-Internal-Api-Key": INTERNAL_API_KEY,
    },
  });

  if (response.status === 404) {
    const detail = await readErrorMessage(response, "执行诊断不存在。");
    if (detail.includes("Generation not found")) {
      return { data: null, error: detail };
    }
    return { data: null, error: null };
  }

  if (!response.ok) {
    return {
      data: null,
      error: await readErrorMessage(response, "执行诊断加载失败。"),
    };
  }

  return {
    data: (await response.json()) as DiagnosticsResponse,
    error: null,
  };
}

async function restoreLatestCheckpointAction(formData: FormData) {
  "use server";

  const generationId = String(formData.get("generation_id") ?? "").trim();
  const redirectGenerationId = generationId || "demo";

  if (!INTERNAL_API_KEY) {
    redirect(
      `/internal/checkpoints/${redirectGenerationId}?action_error=INTERNAL_API_KEY%20is%20not%20configured%20for%20the%20internal%20checkpoint%20console.`,
    );
  }

  if (!generationId) {
    redirect(`/internal/checkpoints/${redirectGenerationId}?action_error=generation_id%20is%20required.`);
  }

  const response = await fetch(`${API_BASE_URL}/internal/generation-checkpoints/${generationId}/restore-latest`, {
    method: "POST",
    cache: "no-store",
    headers: {
      "X-Internal-Api-Key": INTERNAL_API_KEY,
    },
  });

  if (!response.ok) {
    const errorMessage = await readErrorMessage(response, "Checkpoint 恢复失败。");
    redirect(`/internal/checkpoints/${generationId}?action_error=${encodeURIComponent(errorMessage)}`);
  }

  revalidatePath(`/internal/checkpoints/${generationId}`);
  redirect(`/internal/checkpoints/${generationId}?action_success=${encodeURIComponent("Checkpoint 恢复已完成。")}`);
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

export default async function InternalCheckpointPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams?: Promise<{ action_error?: string; action_success?: string }>;
}) {
  const { id } = await params;
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const actionError = resolvedSearchParams.action_error ?? null;
  const actionSuccess = resolvedSearchParams.action_success ?? null;
  const [list, latestState, diagnostics] = await Promise.all([fetchCheckpointList(id), fetchLatestState(id), fetchDiagnostics(id)]);
  const loadError = list.error ?? latestState.error ?? diagnostics.error;

  return (
    <SiteShell
      eyebrow="辅助页面 / 进度排查"
      title={`进度排查 · ${id}`}
      description="这里会展示当前任务最近的状态、关键事件和可恢复情况，方便你在结果异常时继续排查。"
    >
      <div className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroCopy}>
            <span className={styles.heroBadge}>任务恢复与排查</span>
            <h2 className={styles.heroTitle}>当结果没有正常出来时，可以先在这里看看最近发生了什么。</h2>
            <p className={styles.heroLead}>这页会集中展示最近状态、错误提示和恢复入口，帮助你判断是继续等待、重新打开，还是尝试恢复。</p>
          </div>

          <form action={restoreLatestCheckpointAction} className={styles.restoreForm}>
            <input name="generation_id" type="hidden" value={id} />
            <button className={styles.restoreButton} type="submit">
              尝试恢复最近一次结果
            </button>
            <p className={styles.restoreHint}>如果结果没有正常显示，但任务记录还在，可以尝试用这一步恢复。</p>
          </form>
        </section>

        {!INTERNAL_API_KEY ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(255, 224, 214, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>当前未配置内部 API Key</h3>
              <p className={styles.sectionLead}>当前环境还没有开启这页所需的内部访问权限，所以暂时无法读取详细排查信息。</p>
            </div>
          </SpotlightCard>
        ) : null}

        {loadError ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(255, 224, 214, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>进度排查页暂时不可用</h3>
              <p className={styles.sectionLead}>{loadError}</p>
            </div>
          </SpotlightCard>
        ) : null}

        {actionError ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(255, 224, 214, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>恢复未完成</h3>
              <p className={styles.sectionLead}>{actionError}</p>
            </div>
          </SpotlightCard>
        ) : null}

        {actionSuccess ? (
          <SpotlightCard className={styles.warningCard} spotlightColor="rgba(232, 246, 242, 0.42)">
            <div className={styles.warningInner}>
              <h3 className={styles.sectionTitle}>恢复已完成</h3>
              <p className={styles.sectionLead}>{actionSuccess}</p>
            </div>
          </SpotlightCard>
        ) : null}

        <InternalConsoleHub current="checkpoints" generationId={id} />

        <section className={styles.stateGrid}>
          <SpotlightCard className={styles.stateCard} spotlightColor="rgba(255, 244, 230, 0.4)">
            <div className={styles.stateInner}>
              <h3 className={styles.sectionTitle}>最近状态</h3>
              {latestState.data ? (
                <>
                  <p className={styles.sectionLead}>{latestState.data.result_summary ?? "当前最近一次记录里还没有结果摘要。"}</p>
                  <div className={styles.metaList}>
                    <span className={styles.metaChip}>记录 ID {latestState.data.checkpoint_id ?? "none"}</span>
                    <span className={styles.metaChip}>是否有结果 {String(latestState.data.has_result)}</span>
                    <span className={styles.metaChip}>脚本段数 {latestState.data.script_segment_count}</span>
                    <span className={styles.metaChip}>失败类型 {latestState.data.failure_attribution.category}</span>
                  </div>
                  <p className={styles.metaLine}>标题：{latestState.data.result_title ?? "未记录"}</p>
                  <p className={styles.metaLine}>更新时间：{formatDate(latestState.data.created_at)}</p>
                  <div className={styles.failureBlock}>
                    <p className={styles.metaLine}>失败阶段：{latestState.data.failure_attribution.stage_message ?? "未进入失败态"}</p>
                    <p className={styles.metaLine}>最近错误事件：{latestState.data.failure_attribution.latest_event_type ?? "none"}</p>
                    <p className={styles.metaLine}>恢复建议：{latestState.data.failure_attribution.recovery_hint}</p>
                    {latestState.data.failure_attribution.latest_error_message ? (
                      <p className={styles.failureMessage}>{latestState.data.failure_attribution.latest_error_message}</p>
                    ) : null}
                  </div>
                </>
              ) : (
                <p className={styles.sectionLead}>当前任务还没有可用的状态记录。</p>
              )}
            </div>
          </SpotlightCard>

          <SpotlightCard className={styles.stateCard} spotlightColor="rgba(232, 246, 242, 0.42)">
            <div className={styles.stateInner}>
              <h3 className={styles.sectionTitle}>当前进度与最近事件</h3>
              {diagnostics.data ? (
                <>
                  <p className={styles.sectionLead}>{diagnostics.data.status_snapshot.stage_message}</p>
                  <div className={styles.metaList}>
                    <span className={styles.metaChip}>status {diagnostics.data.status_snapshot.status}</span>
                    <span className={styles.metaChip}>阶段 {diagnostics.data.status_snapshot.current_stage}</span>
                    <span className={styles.metaChip}>事件数 {diagnostics.data.event_count}</span>
                    <span className={styles.metaChip}>已有结果 {String(diagnostics.data.has_result_snapshot)}</span>
                  </div>
                  <p className={styles.metaLine}>总耗时：{diagnostics.data.status_snapshot.total_elapsed_seconds ?? "未记录"} 秒</p>
                  <p className={styles.metaLine}>当前阶段耗时：{diagnostics.data.status_snapshot.stage_elapsed_seconds ?? "未记录"} 秒</p>
                  <p className={styles.metaLine}>状态错误：{diagnostics.data.status_snapshot.error_message ?? "none"}</p>

                  <div className={styles.eventBlock}>
                    {(diagnostics.data.events ?? []).slice(-6).reverse().map((event, index) => (
                      <article className={styles.eventItem} key={`${event.event_type}-${event.occurred_at}-${index}`}>
                        <div className={styles.eventHeader}>
                          <span className={styles.itemBadge}>{event.event_type}</span>
                          <span className={styles.itemMeta}>{formatDate(event.occurred_at)}</span>
                        </div>
                        <p className={styles.eventLine}>阶段：{event.stage}</p>
                        <p className={styles.eventLine}>说明：{event.stage_message}</p>
                        {event.error_message ? <p className={styles.eventError}>{event.error_message}</p> : null}
                      </article>
                    ))}
                  </div>
                </>
              ) : (
                <p className={styles.sectionLead}>当前任务还没有可用的进度诊断信息。</p>
              )}

              <div className={styles.linkList}>
                <Link className={styles.linkItem} href={`/generating/${id}`}>
                  打开生成状态页
                </Link>
                <Link className={styles.linkItem} href={`/result/${id}`}>
                  打开结果页
                </Link>
                <Link className={styles.linkItem} href="/internal/trends">
                  返回参考页
                </Link>
              </div>
            </div>
          </SpotlightCard>
        </section>

        <SpotlightCard className={styles.listCard} spotlightColor="rgba(255, 244, 230, 0.38)">
          <div className={styles.listInner}>
            <h3 className={styles.sectionTitle}>历史记录列表</h3>
            <p className={styles.sectionLead}>这里按时间展示当前任务保留下来的记录，方便你回看不同阶段发生过什么。</p>

            <div className={styles.checkpointGrid}>
              {(list.data?.items ?? []).map((item, index) => (
                <article className={styles.checkpointItem} key={`${item.checkpoint_id ?? "none"}-${index}`}>
                  <div className={styles.itemHeader}>
                    <span className={styles.itemBadge}>#{index + 1}</span>
                    <span className={styles.itemMeta}>{item.checkpoint_ns || "default"}</span>
                  </div>
                  <p className={styles.itemLine}>记录 ID: {item.checkpoint_id ?? "none"}</p>
                  <p className={styles.itemLine}>创建时间: {formatDate(item.created_at)}</p>
                  <p className={styles.itemLine}>待写入项: {item.pending_write_count}</p>
                  <div className={styles.channelWrap}>
                    {item.channel_keys.map((key) => (
                      <span className={styles.channelChip} key={key}>
                        {key}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          </div>
        </SpotlightCard>
      </div>
    </SiteShell>
  );
}
