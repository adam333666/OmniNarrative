import type { CreationRequestInput } from "@/lib/schemas/creation-request";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

export const getMarkdownExportUrl = (generationId: string) => `${API_BASE_URL}/creations/${generationId}/export/md`;
export const getJsonExportUrl = (generationId: string) => `${API_BASE_URL}/creations/${generationId}/export/json`;
export const getVideoPayloadUrl = (generationId: string) => `${API_BASE_URL}/creations/${generationId}/video-payload`;

async function readErrorMessage(response: Response, fallbackMessage: string): Promise<string> {
  const contentType = response.headers.get("content-type") ?? "";

  if (contentType.includes("application/json")) {
    try {
      const payload = (await response.json()) as { detail?: unknown; error_message?: unknown };
      if (typeof payload.detail === "string" && payload.detail.trim()) {
        return payload.detail;
      }
      if (typeof payload.error_message === "string" && payload.error_message.trim()) {
        return payload.error_message;
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

async function assertOk(response: Response, fallbackMessage: string): Promise<void> {
  if (response.ok) {
    return;
  }

  throw new Error(await readErrorMessage(response, fallbackMessage));
}

export type InputOptionItem = {
  value: string;
  label: string;
};

export type InputOptionsResponse = {
  content_types: InputOptionItem[];
  platforms: InputOptionItem[];
  style_tones: InputOptionItem[];
  example_prompts: string[];
};

export type TrendTemplateSummary = {
  platform: string;
  content_type: string;
  summary: string;
  source_type: string;
  updated_at: string | null;
  hook_patterns: string[];
  rhythm_patterns: string[];
  title_cover_style: string[];
  audience_preference_summary: string;
  avoid_patterns: string[];
  hot_topics_summary: string[];
  interaction_patterns: string[];
  emotional_entry_points: string[];
  creator_angle_summary: string;
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

export type TrendTemplateListResponse = {
  items: TrendTemplateSummary[];
  total: number;
  generated_at: string;
};

export type GenerateResponse = {
  generation_id: string;
  current_status: string;
  created_at: string;
};

export type StatusResponse = {
  generation_id: string;
  status: string;
  current_stage: string;
  stage_message: string;
  error_message: string | null;
  created_at: string;
  updated_at: string | null;
  completed_at: string | null;
  total_elapsed_seconds: number | null;
  stage_elapsed_seconds: number | null;
};

export type StructuredCandidate = {
  candidate_text: string;
  usage_scenario: string;
  design_reason: string;
};

export type ResultResponse = {
  request_summary: {
    theme_text: string;
    content_type: string;
    target_platform: string;
    target_audience_text: string;
    style_tone: string;
    custom_style_text: string | null;
  };
  analysis: {
    audience_profile: {
      raw_text: string;
      age_group_guess: string;
      interest_tags: string[];
      pain_points: string[];
      content_preference: string[];
      emotion_preference: string[];
    };
    style_profile: {
      style_label: string;
      emotion_label: string;
      intensity_level: string;
      custom_notes: string | null;
    };
    trend_summary: {
      platform: string;
      summary: string;
      hook_patterns: string[];
      rhythm_patterns: string[];
      title_cover_style: string[];
      audience_preference_summary: string;
      avoid_patterns: string[];
      hot_topics_summary: string[];
      interaction_patterns: string[];
      emotional_entry_points: string[];
      creator_angle_summary: string;
      source_trace: Array<{
        title: string;
        link: string | null;
        excerpt: string;
        source_name: string;
      }>;
    };
    key_design_decisions: string[];
  };
  result_package: {
    overview: Record<string, string>;
    script_layer: {
      segments: Array<{
        segment_number: number;
        segment_title: string;
        segment_goal: string;
        narration: string;
        subtitle_text: string;
        visual_description: string;
        emotion: string;
        rhythm: string;
      }>;
      key_shots: Array<{
        shot_title: string;
        shot_focus: string;
        shot_duration_seconds: number;
        transition_hint: string;
        camera_movement: string;
        transition_style: string;
        asset_dependency: string;
        voiceover_cue: string;
      }>;
      script_note: string;
      title_alternatives: string[];
      hook_alternatives: string[];
      title_candidates: StructuredCandidate[];
      hook_candidates: StructuredCandidate[];
    };
    multimodal_layer: Record<string, unknown>;
    platform_layer: {
      platform_strategy: string;
      trend_summary: Record<string, unknown>;
      audience_adaptation: string;
      hook_design_reason: string;
      rhythm_structure_reason: string;
      title_cover_style: string[];
      publishing_copy_suggestion: string;
      avoid_patterns: string[];
      cover_copy_alternatives: string[];
      comment_guidance: string[];
      publish_timing_suggestions: string[];
      distribution_angles: string[];
      thumbnail_copy_candidates: string[];
      cover_candidates: StructuredCandidate[];
      distribution_angle_candidates: StructuredCandidate[];
    };
    machine_payload_layer: Record<string, unknown> & {
      storyboard_frames?: Array<{
        beat_number: number;
        beat_title: string;
        linked_segment_number: number;
        linked_key_shot_title: string;
        visual_focus: string;
        narration_focus: string;
        estimated_duration_seconds: number;
        asset_requirement: string;
        editing_note: string;
      }>;
      asset_preparation_notes?: Array<{
        item_name: string;
        linked_beat_number: number;
        requirement_detail: string;
        ready_stage: string;
      }>;
      voiceover_subtitle_alignment?: Array<{
        linked_beat_number: number;
        voiceover_line: string;
        subtitle_line: string;
        timing_note: string;
      }>;
      estimated_total_duration_seconds?: number;
      runtime_pacing_notes?: string[];
    };
  };
  export_meta: {
    schema_version: string;
    generation_id: string;
    generated_at: string;
  };
};

export async function submitCreationRequest(payload: CreationRequestInput): Promise<GenerateResponse> {
  const response = await fetch(`${API_BASE_URL}/creations/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  await assertOk(response, "创建请求失败，请检查输入后重试。");

  return response.json() as Promise<GenerateResponse>;
}

export async function fetchInputOptions(): Promise<InputOptionsResponse> {
  const response = await fetch(`${API_BASE_URL}/config/input-options`, {
    cache: "no-store",
  });

  await assertOk(response, "获取输入选项失败。");

  return response.json() as Promise<InputOptionsResponse>;
}

export async function fetchGenerationStatus(generationId: string): Promise<StatusResponse> {
  const response = await fetch(`${API_BASE_URL}/creations/${generationId}/status`, {
    cache: "no-store",
  });

  await assertOk(response, "获取生成状态失败。");

  return response.json() as Promise<StatusResponse>;
}

export async function fetchGenerationResult(generationId: string): Promise<ResultResponse> {
  const response = await fetch(`${API_BASE_URL}/creations/${generationId}/result`, {
    cache: "no-store",
  });

  await assertOk(response, "获取结果失败。");

  return response.json() as Promise<ResultResponse>;
}

export async function fetchTrendTemplates(
  platform?: string,
  contentType?: string,
): Promise<TrendTemplateListResponse> {
  const params = new URLSearchParams();
  if (platform) {
    params.set("platform", platform);
  }
  if (contentType) {
    params.set("content_type", contentType);
  }

  const query = params.toString();
  const response = await fetch(`${API_BASE_URL}/config/trend-templates${query ? `?${query}` : ""}`, {
    cache: "no-store",
  });

  await assertOk(response, "获取趋势模板失败。");

  return response.json() as Promise<TrendTemplateListResponse>;
}

export async function fetchMarkdownExport(generationId: string): Promise<string> {
  const response = await fetch(getMarkdownExportUrl(generationId), {
    cache: "no-store",
  });

  await assertOk(response, "获取 Markdown 导出失败。");

  return response.text();
}

export async function fetchJsonExport(generationId: string): Promise<Record<string, unknown>> {
  const response = await fetch(getJsonExportUrl(generationId), {
    cache: "no-store",
  });

  await assertOk(response, "获取 JSON 导出失败。");

  return response.json() as Promise<Record<string, unknown>>;
}

export async function fetchVideoPayload(generationId: string): Promise<Record<string, unknown>> {
  const response = await fetch(getVideoPayloadUrl(generationId), {
    cache: "no-store",
  });

  await assertOk(response, "获取 Video Payload 失败。");

  return response.json() as Promise<Record<string, unknown>>;
}
