"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";

import { DotGrid } from "@/components/upstream/dot-grid";
import { TextType } from "@/components/upstream/text-type";
import { fetchGenerationStatus, type StatusResponse } from "@/lib/api-client/backend";
import { GenerationOutputDeck } from "./generation-output-deck";
import styles from "./generation-status-client.module.css";

const orderedStages = [
  "THEME_PARSING",
  "PROFILE_PARSING",
  "TREND_ADAPTING",
  "NARRATIVE_GENERATING",
  "PACKAGE_ASSEMBLING",
  "DONE",
] as const;

const stageLabels: Record<string, string> = {
  THEME_PARSING: "正在整理主题",
  PROFILE_PARSING: "正在补充受众和风格",
  TREND_ADAPTING: "正在参考平台内容",
  NARRATIVE_GENERATING: "正在生成叙事骨架",
  PACKAGE_ASSEMBLING: "正在整理完整方案",
  DONE: "完整方案已生成",
};

export function GenerationStatusClient({ generationId }: { generationId: string }) {
  const router = useRouter();
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [retryNonce, setRetryNonce] = useState(0);
  const currentIndex = orderedStages.findIndex((item) => item === (status?.current_stage ?? "THEME_PARSING"));
  const typedPhrases = useMemo(
    () => [
      "系统正在把你的主题和要求整理成一份完整方案。",
      "你只需要看进度，完成后会自动进入结果页。",
      "如果中途出问题，这里也会告诉你卡在哪一步。",
    ],
    [],
  );

  useEffect(() => {
    let cancelled = false;
    let timerId: number | null = null;

    async function poll() {
      try {
        const response = await fetchGenerationStatus(generationId);
        if (cancelled) {
          return;
        }
        setStatus(response);
        setError(null);

        if (response.status === "DONE") {
          timerId = window.setTimeout(() => {
            router.push(`/result/${generationId}`);
          }, 800);
          return;
        }

        if (response.status === "FAILED" || response.status === "TIMEOUT") {
          setError(response.error_message ?? "生成未能完成。");
          return;
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(requestError instanceof Error ? requestError.message : "状态轮询失败。");
        }
        return;
      }

      if (!cancelled) {
        timerId = window.setTimeout(poll, 1200);
      }
    }

    poll();
    return () => {
      cancelled = true;
      if (timerId !== null) {
        window.clearTimeout(timerId);
      }
    };
  }, [generationId, retryNonce, router]);

  return (
    <div className={styles.layout}>
      <section className={styles.hero}>
        <div className={styles.gridLayer}>
          <DotGrid
            baseColor="#ffb48c"
            activeColor="#fff3eb"
            dotSize={8}
            gap={22}
            proximity={120}
            shockRadius={180}
            shockStrength={3}
            speedTrigger={60}
          />
        </div>
        <div className={styles.heroInner}>
          <span className={styles.eyebrow}>生成进度</span>
          <div>
            <h2 className={styles.heroTitle}>内容方案正在成形</h2>
            <p className={styles.heroLead}>现在不用做额外操作。等进度完成后，会自动进入结果页。</p>
          </div>
          <div className={styles.typedLine}>
            <TextType
              as="p"
              text={typedPhrases}
              typingSpeed={28}
              deletingSpeed={18}
              pauseDuration={1100}
              initialDelay={120}
              cursorBlinkDuration={0.4}
              textColors={["#ffd7c4", "#fff0e8", "#ffc39c"]}
            />
          </div>
          <div className={styles.metaGrid}>
            <article className={styles.metaCard}>
              <p className={styles.metaLabel}>任务编号</p>
              <p className={styles.metaValue}>{generationId}</p>
            </article>
            <article className={styles.metaCard}>
              <p className={styles.metaLabel}>当前阶段</p>
              <p className={styles.metaValue}>{stageLabels[status?.current_stage ?? "THEME_PARSING"]}</p>
            </article>
            <article className={styles.metaCard}>
              <p className={styles.metaLabel}>累计耗时</p>
              <p className={styles.metaValue}>
                {status?.total_elapsed_seconds != null ? `${status.total_elapsed_seconds}s` : "正在计算中"}
              </p>
            </article>
          </div>
          <div className={styles.toolLinks}>
            <Link className={styles.toolLink} href={`/internal/checkpoints/${generationId}`}>
              查看进度排查页
            </Link>
            <Link className={styles.toolLink} href="/internal/trends">
              查看参考页
            </Link>
          </div>
        </div>
      </section>

      <section className={styles.card}>
        <div className={styles.cardInner}>
          <h3 className={styles.sectionTitle}>阶段轨道</h3>
          <p className={styles.sectionLead}>五个阶段会依次推进。你可以把它理解成“系统正在补哪一部分内容”。</p>
          <div className={styles.progressRail}>
            <ol className={styles.stageList}>
          {orderedStages.slice(0, 5).map((stage, index) => {
            const isActive = stage === status?.current_stage;
            const isDone = currentIndex > index || status?.status === "DONE";
            return (
              <li
                className={`${styles.stageItem} ${isActive ? styles.stageActive : ""} ${isDone ? styles.stageDone : ""}`}
                key={stage}
              >
                <div className={styles.stageHeader}>
                  <h4 className={styles.stageTitle}>{stageLabels[stage]}</h4>
                  <span className={styles.stageBadge}>{isActive ? "进行中" : isDone ? "已完成" : "待进入"}</span>
                </div>
                <p className={styles.stageCopy}>
                  {stage === "THEME_PARSING"
                    ? "先把主题整理清楚，作为后面内容的共同起点。"
                    : stage === "PROFILE_PARSING"
                      ? "把受众和风格补清楚，避免后面只靠感觉往下写。"
                      : stage === "TREND_ADAPTING"
                        ? "加入平台参考信息，提前修正开场方式和表达重点。"
                        : stage === "NARRATIVE_GENERATING"
                          ? "开始生成标题、梗概、脚本段落和镜头建议。"
                          : "把标题、脚本、发布和制作建议整理成完整结果。"}
                </p>
              </li>
            );
          })}
            </ol>
          </div>
          <GenerationOutputDeck />
        </div>
      </section>

      <section className={styles.card}>
        <div className={styles.cardInner}>
          <h3 className={styles.sectionTitle}>当前状态</h3>
          <p className={styles.sectionLead}>这里会持续刷新最新状态。完成后不需要手动刷新页面。</p>
          <div className={styles.statusBody}>
            <div className={styles.statusChipRow}>
              <span className={styles.statusChip}>状态: {status?.status ?? "POLLING"}</span>
              {status?.stage_elapsed_seconds != null ? (
                <span className={styles.statusChip}>阶段耗时: {status.stage_elapsed_seconds}s</span>
              ) : null}
              {status?.completed_at ? <span className={styles.statusChip}>已完成</span> : null}
            </div>
            <div className={styles.currentMessage}>{status?.stage_message ?? "正在连接进度服务..."}</div>
            {status?.status === "DONE" ? <p className={styles.success}>方案已生成，正在跳转结果页。</p> : null}
          </div>
        </div>
      </section>

      {error ? (
        <div className={styles.errorCard}>
          <p className={styles.errorText}>{error}</p>
          {status?.current_stage ? (
            <p className={styles.recentStage}>
              最近阶段：{stageLabels[status.current_stage] ?? status.current_stage}
            </p>
          ) : null}
          <div className={styles.actionRow}>
            <button
              onClick={() => {
                setError(null);
                setRetryNonce((value) => value + 1);
              }}
              className={styles.retryButton}
            >
              立即重试状态拉取
            </button>
            <Link href="/create" className={styles.linkAction}>
              返回重新开始
            </Link>
          </div>
        </div>
      ) : null}
    </div>
  );
}
