"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { GradientText } from "@/components/ui/gradient-text";
import { SpotlightCard } from "@/components/ui/spotlight-card";
import {
  fetchGenerationResult,
  getJsonExportUrl,
  getMarkdownExportUrl,
  getVideoPayloadUrl,
  type ResultResponse,
} from "@/lib/api-client/backend";

import { AnalysisSummary } from "./analysis-summary";
import { ExportActionPanel } from "./export-action-panel";
import { AnimatedDecisionList } from "./animated-decision-list";
import { ExportJsonPreview } from "./export-json-preview";
import { DistributionStrategyDeck } from "./distribution-strategy-deck";
import { MarkdownPreview } from "./markdown-preview";
import { ResultSectionNav } from "./result-section-nav";
import { ScriptSegmentNav } from "./script-segment-nav";
import { ScriptSummaryStrip } from "./script-summary-strip";
import { MachinePayloadSummary } from "./machine-payload-summary";
import { MultimodalSummary } from "./multimodal-summary";
import { PayloadFoldoutHeader } from "./payload-foldout-header";
import { PlatformLayerSummary } from "./platform-layer-summary";
import { PlatformRiskPanel } from "./platform-risk-panel";
import { OverviewSummary } from "./overview-summary";
import { ResultHeroSummary } from "./result-hero-summary";
import { TrendInfluenceDeck } from "./trend-influence-deck";
import { ResultNextStepGuide } from "./result-next-step-guide";
import { TrendSourceTracePanel } from "./trend-source-trace-panel";
import { ConsistencyThreadDeck } from "./consistency-thread-deck";
import styles from "./result-view-client.module.css";

export function ResultViewClient({ generationId }: { generationId: string }) {
  const [result, setResult] = useState<ResultResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [retryNonce, setRetryNonce] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const response = await fetchGenerationResult(generationId);
        if (cancelled) {
          return;
        }
        setResult(response);
        setError(null);
      } catch (requestError) {
        if (cancelled) {
          return;
        }
        setError(requestError instanceof Error ? requestError.message : "这次方案暂时还没能成功加载。");
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [generationId, retryNonce]);

  if (error) {
    return (
      <div className={styles.layout}>
        <section className={styles.card}>
          <div className={styles.detailInner}>
            <h3 className={styles.sectionTitle}>这次方案暂时还没打开成功</h3>
            <p className={styles.error}>{error}</p>
            <p className={styles.sectionLead}>generation_id: {generationId}</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 12 }}>
              <button
                onClick={() => {
                  setError(null);
                  setRetryNonce((value) => value + 1);
                }}
                style={{
                  border: "1px solid var(--border)",
                  borderRadius: 999,
                  padding: "10px 16px",
                  background: "var(--foreground)",
                  color: "var(--background)",
                  fontWeight: 700,
                  cursor: "pointer",
                }}
              >
                重新打开这次结果
              </button>
              <Link href={`/generating/${generationId}`} style={{ color: "var(--accent)", fontWeight: 700, alignSelf: "center" }}>
                回到生成进度页
              </Link>
              <Link href="/create" style={{ color: "var(--accent)", fontWeight: 700, alignSelf: "center" }}>
                重新开一轮
              </Link>
            </div>
          </div>
        </section>
      </div>
    );
  }

  if (result === null) {
    return <p className={styles.loading}>正在打开这次生成好的方案...</p>;
  }

  const { request_summary, analysis, result_package } = result;
  const multimodalLayer = result_package.multimodal_layer as Record<string, unknown>;
  const machinePayloadLayer = result_package.machine_payload_layer as Record<string, unknown>;
  const sceneProgression = Array.isArray(multimodalLayer.scene_progression) ? (multimodalLayer.scene_progression as string[]) : [];
  const motionCues = Array.isArray(multimodalLayer.motion_cues) ? (multimodalLayer.motion_cues as string[]) : [];
  const assetProps = Array.isArray(multimodalLayer.asset_props) ? (multimodalLayer.asset_props as string[]) : [];
  const visualReferences = Array.isArray(multimodalLayer.visual_references) ? (multimodalLayer.visual_references as string[]) : [];
  const commentGuidance = Array.isArray(result_package.platform_layer.comment_guidance)
    ? result_package.platform_layer.comment_guidance
    : [];
  const publishTimingSuggestions = Array.isArray(result_package.platform_layer.publish_timing_suggestions)
    ? result_package.platform_layer.publish_timing_suggestions
    : [];
  const distributionAngles = Array.isArray(result_package.platform_layer.distribution_angles)
    ? result_package.platform_layer.distribution_angles
    : [];
  const thumbnailCopyCandidates = Array.isArray(result_package.platform_layer.thumbnail_copy_candidates)
    ? result_package.platform_layer.thumbnail_copy_candidates
    : [];
  const assetChecklist = Array.isArray(machinePayloadLayer.asset_checklist) ? (machinePayloadLayer.asset_checklist as string[]) : [];
  const editingChecklist = Array.isArray(machinePayloadLayer.editing_checklist) ? (machinePayloadLayer.editing_checklist as string[]) : [];
  const ctaVariants = Array.isArray(machinePayloadLayer.cta_variants) ? (machinePayloadLayer.cta_variants as string[]) : [];
  const storyboardBeats = Array.isArray(machinePayloadLayer.storyboard_beats) ? (machinePayloadLayer.storyboard_beats as string[]) : [];
  const storyboardFrames = Array.isArray(machinePayloadLayer.storyboard_frames)
    ? (machinePayloadLayer.storyboard_frames as Array<Record<string, unknown>>)
    : [];
  const assetPreparationNotes = Array.isArray(machinePayloadLayer.asset_preparation_notes)
    ? (machinePayloadLayer.asset_preparation_notes as Array<Record<string, unknown>>)
    : [];
  const voiceoverSubtitleAlignment = Array.isArray(machinePayloadLayer.voiceover_subtitle_alignment)
    ? (machinePayloadLayer.voiceover_subtitle_alignment as Array<Record<string, unknown>>)
    : [];
  const runtimePacingNotes = Array.isArray(machinePayloadLayer.runtime_pacing_notes)
    ? (machinePayloadLayer.runtime_pacing_notes as string[])
    : [];
  const estimatedTotalDurationSeconds =
    typeof machinePayloadLayer.estimated_total_duration_seconds === "number"
      ? machinePayloadLayer.estimated_total_duration_seconds
      : 0;
  const thumbnailPrompt = typeof machinePayloadLayer.thumbnail_prompt_block === "string" ? machinePayloadLayer.thumbnail_prompt_block : "";
  const voiceoverPrompt = typeof machinePayloadLayer.voiceover_prompt_block === "string" ? machinePayloadLayer.voiceover_prompt_block : "";
  const titleCandidates = Array.isArray(result_package.script_layer.title_candidates) ? result_package.script_layer.title_candidates : [];
  const hookCandidates = Array.isArray(result_package.script_layer.hook_candidates) ? result_package.script_layer.hook_candidates : [];
  const coverCandidates = Array.isArray(result_package.platform_layer.cover_candidates) ? result_package.platform_layer.cover_candidates : [];
  const distributionAngleCandidates = Array.isArray(result_package.platform_layer.distribution_angle_candidates)
    ? result_package.platform_layer.distribution_angle_candidates
    : [];

  return (
    <div className={styles.layout}>
      <aside className={styles.sidebar}>
        <section className={styles.heroCard}>
          <div className={styles.heroInner}>
            <span className={styles.eyebrow}>本次结果</span>
            <h2 className={styles.heroTitle}>{result_package.overview.main_title}</h2>
            <p className={styles.heroSummary}>{result_package.overview.one_sentence_summary}</p>

            <ResultHeroSummary
              themeText={request_summary.theme_text}
              targetPlatform={request_summary.target_platform}
              contentPositioning={result_package.overview.content_positioning}
              styleSummary={result_package.overview.style_summary}
            />
          </div>
        </section>

        <section className={styles.card}>
          <div className={styles.cardInner}>
            <h3 className={styles.sectionTitle}>参考信息</h3>
            <AnalysisSummary
              trendSummary={analysis.trend_summary.summary}
              audienceRawText={analysis.audience_profile.raw_text}
              ageGroupGuess={analysis.audience_profile.age_group_guess}
              interestTags={analysis.audience_profile.interest_tags}
            />
            <TrendInfluenceDeck
              hookPatterns={analysis.trend_summary.hook_patterns}
              rhythmPatterns={analysis.trend_summary.rhythm_patterns}
              titleCoverStyle={analysis.trend_summary.title_cover_style}
              avoidPatterns={analysis.trend_summary.avoid_patterns}
              hotTopics={analysis.trend_summary.hot_topics_summary}
              interactionPatterns={analysis.trend_summary.interaction_patterns}
              emotionalEntryPoints={analysis.trend_summary.emotional_entry_points}
              creatorAngleSummary={analysis.trend_summary.creator_angle_summary}
            />
            <TrendSourceTracePanel items={analysis.trend_summary.source_trace ?? []} />
            <AnimatedDecisionList items={analysis.key_design_decisions} />
          </div>
        </section>

        <section className={styles.card}>
          <div className={styles.cardInner}>
            <h3 className={styles.sectionTitle}>导出和下一步</h3>
            <ExportActionPanel
              jsonUrl={getJsonExportUrl(generationId)}
              markdownUrl={getMarkdownExportUrl(generationId)}
              videoPayloadUrl={getVideoPayloadUrl(generationId)}
            />
            <div className={styles.internalLinkGroup}>
              <Link className={styles.internalLink} href={`/internal/checkpoints/${generationId}`}>
                查看进度排查页
              </Link>
              <Link className={styles.internalLink} href="/internal/trends">
                查看参考页
              </Link>
            </div>
            <ResultNextStepGuide generationId={generationId} />
          </div>
        </section>
      </aside>

      <section className={styles.content}>
        <ResultSectionNav />

        <div id="overview-layer">
          <SpotlightCard className={styles.heroCard} spotlightColor="rgba(255, 244, 230, 0.36)">
            <div className={styles.detailInner}>
              <h3 className={styles.sectionTitle}>
                <GradientText>整体方向</GradientText>
              </h3>
              <p className={styles.sectionLead}>{result_package.overview.design_summary}</p>
              <ConsistencyThreadDeck
                themeText={request_summary.theme_text}
                audienceText={analysis.audience_profile.raw_text}
                styleSummary={result_package.overview.style_summary}
                trendSummary={analysis.trend_summary.summary}
                platformStrategy={result_package.platform_layer.platform_strategy}
              />
              <OverviewSummary overview={result_package.overview as Record<string, unknown>} />
            </div>
          </SpotlightCard>
        </div>

        <div id="markdown-preview">
          <SpotlightCard className={styles.card} spotlightColor="rgba(255, 244, 230, 0.32)">
            <div className={styles.detailInner}>
              <MarkdownPreview generationId={generationId} />
            </div>
          </SpotlightCard>
        </div>

        <div className={styles.exportPreviewGrid}>
          <SpotlightCard className={styles.card} spotlightColor="rgba(255, 244, 230, 0.32)">
            <div className={styles.detailInner}>
              <ExportJsonPreview generationId={generationId} mode="json" />
            </div>
          </SpotlightCard>

          <SpotlightCard className={styles.card} spotlightColor="rgba(232, 246, 242, 0.34)">
            <div className={styles.detailInner}>
              <ExportJsonPreview generationId={generationId} mode="video" />
            </div>
          </SpotlightCard>
        </div>

        <article className={styles.card} id="script-layer">
          <div className={styles.detailInner}>
            <h3 className={styles.sectionTitle}>脚本内容</h3>
            <ScriptSegmentNav
              segments={result_package.script_layer.segments.map((segment) => ({
                segment_number: segment.segment_number,
                segment_title: segment.segment_title,
              }))}
            />
            <ScriptSummaryStrip
              segments={result_package.script_layer.segments.map((segment) => ({
                segment_number: segment.segment_number,
                segment_title: segment.segment_title,
                segment_goal: segment.segment_goal,
                emotion: segment.emotion,
                rhythm: segment.rhythm,
              }))}
            />
            <p className={styles.sectionLead}>每一段都保留了目标、旁白、字幕、画面和节奏，方便你继续修改和制作。</p>
            <div className={styles.segmentList}>
              {result_package.script_layer.segments.map((segment) => (
                <div className={styles.segmentCard} id={"script-segment-" + segment.segment_number} key={segment.segment_number}>
                  <div className={styles.segmentHeader}>
                    <span className={styles.segmentIndex}>段落 {segment.segment_number}</span>
                    <span className={styles.segmentTitle}>{segment.segment_title}</span>
                  </div>
                  <div className={styles.segmentGrid}>
                    <div className={styles.segmentMeta}><strong>目标：</strong>{segment.segment_goal}</div>
                    <div className={styles.segmentMeta}><strong>旁白：</strong>{segment.narration}</div>
                    <div className={styles.segmentMeta}><strong>字幕：</strong>{segment.subtitle_text}</div>
                    <div className={styles.segmentMeta}><strong>画面：</strong>{segment.visual_description}</div>
                    <div className={styles.segmentMeta}><strong>情绪 / 节奏：</strong>{segment.emotion} / {segment.rhythm}</div>
                  </div>
                </div>
              ))}
            </div>

            <div className={styles.shotSection}>
              <div className={styles.subsectionHeader}>
                <h4 className={styles.subsectionTitle}>关键镜头建议</h4>
                <p className={styles.subsectionLead}>这里先把最关键的镜头定下来，方便后续继续做分镜和制作安排。</p>
              </div>
              <div className={styles.shotGrid}>
                {result_package.script_layer.key_shots.map((shot, index) => (
                  <div className={styles.shotCard} key={shot.shot_title + index}>
                    <div className={styles.shotBadge}>镜头 {index + 1}</div>
                    <h5 className={styles.shotTitle}>{shot.shot_title}</h5>
                    <p className={styles.shotLead}>{shot.shot_focus}</p>
                    <div className={styles.shotMetaList}>
                      <span className={styles.shotMetaItem}>时长 {shot.shot_duration_seconds}s</span>
                      <span className={styles.shotMetaItem}>{shot.transition_hint}</span>
                    </div>
                    <div className={styles.shotDetailList}>
                      <span className={styles.shotDetailItem}><strong>运动：</strong>{shot.camera_movement || "待补充"}</span>
                      <span className={styles.shotDetailItem}><strong>转场：</strong>{shot.transition_style || shot.transition_hint}</span>
                      <span className={styles.shotDetailItem}><strong>素材依赖：</strong>{shot.asset_dependency || "待补充"}</span>
                      <span className={styles.shotDetailItem}><strong>配音落点：</strong>{shot.voiceover_cue || "待补充"}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className={styles.shotSection}>
              <div className={styles.subsectionHeader}>
                <h4 className={styles.subsectionTitle}>备选写法</h4>
                <p className={styles.subsectionLead}>把标题和开场方式整理成多组备选，方便你比较和挑选。</p>
              </div>
              <div className={styles.candidateGrid}>
                <section className={styles.candidateCardGroup}>
                  <h5 className={styles.candidateGroupTitle}>标题候选</h5>
                  {titleCandidates.map((candidate, index) => (
                    <article className={styles.candidateCard} key={candidate.candidate_text + index}>
                      <span className={styles.candidateIndex}>Title {index + 1}</span>
                      <p className={styles.candidateText}>{candidate.candidate_text}</p>
                      <p className={styles.candidateMeta}><strong>场景：</strong>{candidate.usage_scenario}</p>
                      <p className={styles.candidateMeta}><strong>原因：</strong>{candidate.design_reason}</p>
                    </article>
                  ))}
                </section>
                <section className={styles.candidateCardGroup}>
                  <h5 className={styles.candidateGroupTitle}>钩子候选</h5>
                  {hookCandidates.map((candidate, index) => (
                    <article className={styles.candidateCard} key={candidate.candidate_text + index}>
                      <span className={styles.candidateIndex}>Hook {index + 1}</span>
                      <p className={styles.candidateText}>{candidate.candidate_text}</p>
                      <p className={styles.candidateMeta}><strong>场景：</strong>{candidate.usage_scenario}</p>
                      <p className={styles.candidateMeta}><strong>原因：</strong>{candidate.design_reason}</p>
                    </article>
                  ))}
                </section>
              </div>
            </div>
          </div>
        </article>

        <article className={styles.card} id="platform-layer">
          <div className={styles.detailInner}>
            <h3 className={styles.sectionTitle}>发布建议</h3>
            <PlatformLayerSummary platformLayer={result_package.platform_layer as Record<string, unknown>} />
            <PlatformRiskPanel avoidPatterns={result_package.platform_layer.avoid_patterns} />
            <div className={styles.platformCandidateGrid}>
              <section className={styles.candidateCardGroup}>
                <h4 className={styles.subsectionTitle}>封面备选</h4>
                {coverCandidates.map((candidate, index) => (
                  <article className={styles.candidateCard} key={candidate.candidate_text + index}>
                    <span className={styles.candidateIndex}>Cover {index + 1}</span>
                    <p className={styles.candidateText}>{candidate.candidate_text}</p>
                    <p className={styles.candidateMeta}><strong>场景：</strong>{candidate.usage_scenario}</p>
                    <p className={styles.candidateMeta}><strong>原因：</strong>{candidate.design_reason}</p>
                  </article>
                ))}
              </section>
              <section className={styles.candidateCardGroup}>
                <h4 className={styles.subsectionTitle}>发布角度备选</h4>
                {distributionAngleCandidates.map((candidate, index) => (
                  <article className={styles.candidateCard} key={candidate.candidate_text + index}>
                    <span className={styles.candidateIndex}>Angle {index + 1}</span>
                    <p className={styles.candidateText}>{candidate.candidate_text}</p>
                    <p className={styles.candidateMeta}><strong>场景：</strong>{candidate.usage_scenario}</p>
                    <p className={styles.candidateMeta}><strong>原因：</strong>{candidate.design_reason}</p>
                  </article>
                ))}
              </section>
            </div>
          </div>
        </article>

        <article className={styles.card}>
          <div className={styles.detailInner}>
            <h3 className={styles.sectionTitle}>制作参考</h3>
            <p className={styles.sectionLead}>这里把场景推进、镜头提示、发布时间和素材清单都整理出来，方便你继续制作。</p>
            <div className={styles.optionGrid}>
              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Scene Progression</span>
                <h4 className={styles.optionTitle}>场景推进</h4>
                <ul className={styles.optionList}>
                  {sceneProgression.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Motion Cues</span>
                <h4 className={styles.optionTitle}>镜头运动提示</h4>
                <ul className={styles.optionList}>
                  {motionCues.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Publishing Windows</span>
                <h4 className={styles.optionTitle}>发布时间建议</h4>
                <ul className={styles.optionList}>
                  {publishTimingSuggestions.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Comment Guidance</span>
                <h4 className={styles.optionTitle}>评论区引导</h4>
                <ul className={styles.optionList}>
                  {commentGuidance.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Asset Props</span>
                <h4 className={styles.optionTitle}>素材与道具</h4>
                <ul className={styles.optionList}>
                  {assetProps.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Visual References</span>
                <h4 className={styles.optionTitle}>视觉参考</h4>
                <ul className={styles.optionList}>
                  {visualReferences.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Execution Prompts</span>
                <h4 className={styles.optionTitle}>执行提示</h4>
                <p className={styles.optionLead}><strong>缩略图：</strong>{thumbnailPrompt}</p>
                <p className={styles.optionLead}><strong>配音：</strong>{voiceoverPrompt}</p>
                <div className={styles.optionMetaWrap}>
                  {assetChecklist.map((item) => (
                    <span className={styles.optionMetaChip} key={item}>
                      {item}
                    </span>
                  ))}
                </div>
                <ul className={styles.optionList}>
                  {editingChecklist.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Storyboard Beats</span>
                <h4 className={styles.optionTitle}>分镜节拍拆分</h4>
                <ul className={styles.optionList}>
                  {storyboardBeats.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Storyboard Frames</span>
                <h4 className={styles.optionTitle}>结构化分镜帧</h4>
                <div className={styles.storyboardFrameList}>
                  {storyboardFrames.map((frame, index) => (
                    <article className={styles.storyboardFrameCard} key={`${frame.beat_number ?? index}-${frame.beat_title ?? index}`}>
                      <span className={styles.storyboardFrameIndex}>Beat {String(frame.beat_number ?? index + 1)}</span>
                      <p className={styles.storyboardFrameTitle}>{String(frame.beat_title ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>对应段落：</strong>{String(frame.linked_segment_number ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>对应关键镜头：</strong>{String(frame.linked_key_shot_title ?? "无")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>画面：</strong>{String(frame.visual_focus ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>旁白：</strong>{String(frame.narration_focus ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>时长：</strong>{String(frame.estimated_duration_seconds ?? 0)} 秒</p>
                      <p className={styles.storyboardFrameMeta}><strong>素材：</strong>{String(frame.asset_requirement ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>剪辑：</strong>{String(frame.editing_note ?? "")}</p>
                    </article>
                  ))}
                </div>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Asset Prep</span>
                <h4 className={styles.optionTitle}>素材准备说明</h4>
                <div className={styles.storyboardFrameList}>
                  {assetPreparationNotes.map((item, index) => (
                    <article className={styles.storyboardFrameCard} key={`${item.item_name ?? index}-${item.linked_beat_number ?? index}`}>
                      <p className={styles.storyboardFrameTitle}>{String(item.item_name ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>对应分镜：</strong>{String(item.linked_beat_number ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>要求：</strong>{String(item.requirement_detail ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>准备阶段：</strong>{String(item.ready_stage ?? "")}</p>
                    </article>
                  ))}
                </div>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>VO / Subtitle</span>
                <h4 className={styles.optionTitle}>配音字幕对齐</h4>
                <div className={styles.storyboardFrameList}>
                  {voiceoverSubtitleAlignment.map((item, index) => (
                    <article className={styles.storyboardFrameCard} key={`${item.linked_beat_number ?? index}-${item.voiceover_line ?? index}`}>
                      <p className={styles.storyboardFrameMeta}><strong>对应分镜：</strong>{String(item.linked_beat_number ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>配音：</strong>{String(item.voiceover_line ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>字幕：</strong>{String(item.subtitle_line ?? "")}</p>
                      <p className={styles.storyboardFrameMeta}><strong>时序：</strong>{String(item.timing_note ?? "")}</p>
                    </article>
                  ))}
                </div>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Runtime</span>
                <h4 className={styles.optionTitle}>总时长与节奏说明</h4>
                <p className={styles.optionLead}><strong>预计总时长：</strong>{estimatedTotalDurationSeconds} 秒</p>
                <ul className={styles.optionList}>
                  {runtimePacingNotes.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>
            </div>
          </div>
        </article>

        <article className={styles.card}>
          <div className={styles.detailInner}>
            <h3 className={styles.sectionTitle}>发布备选</h3>
            <p className={styles.sectionLead}>把标题、开场、封面和发布建议一起展开，方便你快速比较不同方向。</p>
            <DistributionStrategyDeck
              titleAlternatives={result_package.script_layer.title_alternatives}
              hookAlternatives={result_package.script_layer.hook_alternatives}
              coverCopyAlternatives={[...result_package.platform_layer.cover_copy_alternatives, ...thumbnailCopyCandidates]}
              distributionAngles={distributionAngles}
            />
            <div className={styles.optionGrid}>
              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Title Alternatives</span>
                <h4 className={styles.optionTitle}>标题备选</h4>
                <ul className={styles.optionList}>
                  {result_package.script_layer.title_alternatives.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Hook Alternatives</span>
                <h4 className={styles.optionTitle}>开场钩子备选</h4>
                <ul className={styles.optionList}>
                  {result_package.script_layer.hook_alternatives.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Cover Copy</span>
                <h4 className={styles.optionTitle}>封面文案备选</h4>
                <ul className={styles.optionList}>
                  {[...result_package.platform_layer.cover_copy_alternatives, ...thumbnailCopyCandidates].map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>

              <section className={styles.optionCard}>
                <span className={styles.optionEyebrow}>Publishing Copy</span>
                <h4 className={styles.optionTitle}>发布建议</h4>
                <p className={styles.optionLead}>{result_package.platform_layer.publishing_copy_suggestion}</p>
                <div className={styles.optionMetaWrap}>
                  {result_package.platform_layer.title_cover_style.map((item) => (
                    <span className={styles.optionMetaChip} key={item}>
                      {item}
                    </span>
                  ))}
                </div>
                <ul className={styles.optionList}>
                  {distributionAngles.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
                <ul className={styles.optionList}>
                  {ctaVariants.map((item) => (
                    <li className={styles.optionItem} key={item}>
                      {item}
                    </li>
                  ))}
                </ul>
              </section>
            </div>
          </div>
        </article>

        <details className={styles.detailCard} id="multimodal-layer">
          <summary>
            <PayloadFoldoutHeader
              eyebrow="制作信息"
              title="画面与镜头信息"
              description="这里汇总了与画面、镜头和制作相关的结构化内容。"
              entryCount={Object.keys(result_package.multimodal_layer).length}
              sourceLabel="当前结果中的制作信息"
            />
          </summary>
          <MultimodalSummary payload={result_package.multimodal_layer as Record<string, unknown>} />
          <div className={styles.codeContent}>
            <pre className={styles.codeBlock}>{JSON.stringify(result_package.multimodal_layer, null, 2)}</pre>
          </div>
        </details>

        <details className={styles.codeCard} id="machine-layer">
          <summary>
            <PayloadFoldoutHeader
              eyebrow="结构化导出"
              title="完整字段内容"
              description="这里保留了更完整的字段内容，方便继续交给其他工具或流程使用。"
              entryCount={Object.keys(result_package.machine_payload_layer).length}
              sourceLabel="当前结果中的完整字段"
            />
          </summary>
          <MachinePayloadSummary payload={result_package.machine_payload_layer as Record<string, unknown>} />
          <div className={styles.codeContent}>
            <pre className={styles.codeBlock}>{JSON.stringify(result_package.machine_payload_layer, null, 2)}</pre>
          </div>
        </details>
      </section>
    </div>
  );
}
