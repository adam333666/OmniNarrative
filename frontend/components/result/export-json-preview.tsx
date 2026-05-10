"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchJsonExport, fetchVideoPayload } from "@/lib/api-client/backend";

import { MachinePayloadSummary } from "./machine-payload-summary";
import { PayloadFoldoutHeader } from "./payload-foldout-header";
import styles from "./export-json-preview.module.css";

type Mode = "json" | "video";

function buildSummary(payload: Record<string, unknown>, mode: Mode): Record<string, unknown> {
  if (mode === "video") {
    return {
      video_meta: payload.video_meta ?? {},
      segments: payload.segments ?? [],
      shots: payload.shots ?? [],
      characters: payload.characters ?? [],
      scenes: payload.scenes ?? [],
      scene_progression: payload.scene_progression ?? [],
      motion_cues: payload.motion_cues ?? [],
      asset_props: payload.asset_props ?? [],
      visual_references: payload.visual_references ?? [],
      publish_timing_suggestions: payload.publish_timing_suggestions ?? [],
      distribution_angles: payload.distribution_angles ?? [],
      thumbnail_copy_candidates: payload.thumbnail_copy_candidates ?? [],
      comment_guidance: payload.comment_guidance ?? [],
      cover_copy_alternatives: payload.cover_copy_alternatives ?? [],
      title_alternatives: payload.title_alternatives ?? [],
      hook_alternatives: payload.hook_alternatives ?? [],
      title_candidates: payload.title_candidates ?? [],
      hook_candidates: payload.hook_candidates ?? [],
      cover_candidates: payload.cover_candidates ?? [],
      distribution_angle_candidates: payload.distribution_angle_candidates ?? [],
      editing_checklist: payload.editing_checklist ?? [],
      cta_variants: payload.cta_variants ?? [],
      storyboard_beats: payload.storyboard_beats ?? [],
      storyboard_frames: payload.storyboard_frames ?? [],
      asset_preparation_notes: payload.asset_preparation_notes ?? [],
      voiceover_subtitle_alignment: payload.voiceover_subtitle_alignment ?? [],
      estimated_total_duration_seconds: payload.estimated_total_duration_seconds ?? 0,
      runtime_pacing_notes: payload.runtime_pacing_notes ?? [],
      trend_source_trace: payload.trend_source_trace ?? [],
      negative_constraints: payload.negative_constraints ?? [],
    };
  }

  return {
    request_summary: payload.request_summary ?? {},
    analysis: payload.analysis ?? {},
    result_package: payload.result_package ?? {},
    export_meta: payload.export_meta ?? {},
  };
}

export function ExportJsonPreview({ generationId, mode }: { generationId: string; mode: Mode }) {
  const [payload, setPayload] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [retryNonce, setRetryNonce] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const response = mode === "json" ? await fetchJsonExport(generationId) : await fetchVideoPayload(generationId);
        if (!cancelled) {
          setPayload(response);
          setError(null);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(requestError instanceof Error ? requestError.message : "导出预览加载失败。");
        }
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [generationId, mode, retryNonce]);

  const summary = useMemo(() => {
    if (!payload) {
      return {};
    }

    return buildSummary(payload, mode);
  }, [payload, mode]);

  const title = mode === "json" ? "JSON 导出预览" : "视频制作内容预览";
  const eyebrow = mode === "json" ? "JSON 导出" : "视频制作内容";
  const description =
    mode === "json"
      ? "这里展示适合继续给工具、脚本或其他流程使用的完整字段内容。"
      : "这里展示更适合继续进入视频制作流程的结构化内容。";

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <h3 className={styles.title}>{title}</h3>
        <span className={styles.lead}>{description}</span>
      </div>

      {error ? (
        <div className={styles.errorPanel}>
          <p className={styles.error}>{error}</p>
          <button
            className={styles.retryButton}
            onClick={() => {
              setError(null);
              setRetryNonce((value) => value + 1);
            }}
            type="button"
          >
            重新加载内容
          </button>
        </div>
      ) : null}

      {!payload && !error ? <p className={styles.status}>正在加载内容预览...</p> : null}

      {payload ? (
        <details className={styles.foldout} open>
          <summary>
            <PayloadFoldoutHeader
              eyebrow={eyebrow}
              title={title}
              description={description}
              entryCount={Object.keys(payload).length}
              sourceLabel={mode === "json" ? "当前结果的 JSON 导出" : "当前结果的视频制作内容"}
            />
          </summary>
          <MachinePayloadSummary payload={summary} />
          <div className={styles.codeContent}>
            <pre className={styles.codeBlock}>{JSON.stringify(payload, null, 2)}</pre>
          </div>
        </details>
      ) : null}
    </div>
  );
}
