"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";

import { fetchInputOptions, submitCreationRequest, type InputOptionItem } from "@/lib/api-client/backend";
import { creationPresetMap, creationPresets, type CreationPreset } from "@/lib/constants/creation-presets";
import { contentTypes, examplePrompts, styleTones, targetPlatforms } from "@/lib/constants/input-options";
import { creationRequestSchema, type CreationRequestInput } from "@/lib/schemas/creation-request";
import { ConsistencyPreviewDeck } from "@/components/wizard/consistency-preview-deck";
import { CreationPresetDeck } from "@/components/wizard/creation-preset-deck";
import { TrendSignalPanel } from "@/components/wizard/trend-signal-panel";
import styles from "./create-wizard.module.css";

const steps = [
  {
    title: "主题 / 核心想法",
    description: "先用一句话写清你这次想做什么。",
    field: "theme_text",
  },
  {
    title: "内容类型",
    description: "决定这次更偏解释、故事、混合，或者交给系统判断。",
    field: "content_type",
  },
  {
    title: "目标平台",
    description: "平台会影响开场、节奏、标题和封面建议。",
    field: "target_platform",
  },
  {
    title: "目标受众",
    description: "写清你想打动谁，后面的表达方式会围绕这群人调整。",
    field: "target_audience_text",
  },
  {
    title: "风格 / 情绪基调",
    description: "确定整体语气和情绪，也可以补充更细的要求。",
    field: "style_tone",
  },
] as const;

function cardStyle(selected: boolean) {
  return {
    background: selected ? "rgba(180, 79, 44, 0.12)" : "var(--surface)",
    border: selected ? "1px solid rgba(180, 79, 44, 0.55)" : "1px solid var(--border)",
    borderRadius: 20,
    cursor: "pointer",
    padding: 18,
    textAlign: "left" as const,
  };
}

type CreateWizardProps = {
  initialPresetKey?: string;
};

export function CreateWizard({ initialPresetKey }: CreateWizardProps) {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(0);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [remoteContentTypes, setRemoteContentTypes] = useState<InputOptionItem[] | null>(null);
  const [remotePlatforms, setRemotePlatforms] = useState<InputOptionItem[] | null>(null);
  const [remoteStyleTones, setRemoteStyleTones] = useState<InputOptionItem[] | null>(null);
  const [remoteExamplePrompts, setRemoteExamplePrompts] = useState<string[] | null>(null);

  const {
    register,
    handleSubmit,
    trigger,
    watch,
    setValue,
    formState: { errors },
  } = useForm<CreationRequestInput>({
    resolver: zodResolver(creationRequestSchema),
    defaultValues: {
      theme_text: "",
      content_type: "auto",
      target_platform: "bilibili",
      target_audience_text: "",
      style_tone: "mysterious",
      custom_style_text: "",
    },
    mode: "onChange",
  });

  const values = watch();
  const progressLabel = useMemo(() => `${currentStep + 1} / ${steps.length}`, [currentStep]);
  const resolvedContentTypes = remoteContentTypes ?? [...contentTypes];
  const resolvedPlatforms = remotePlatforms ?? [...targetPlatforms];
  const resolvedStyleTones = remoteStyleTones ?? [...styleTones];
  const resolvedExamplePrompts = remoteExamplePrompts ?? [...examplePrompts];
  const currentPlatformLabel = resolvedPlatforms.find((item) => item.value === values.target_platform)?.label ?? "待选择";
  const currentContentTypeLabel = resolvedContentTypes.find((item) => item.value === values.content_type)?.label ?? "待选择";

  useEffect(() => {
    let cancelled = false;

    async function loadInputOptions() {
      try {
        const response = await fetchInputOptions();
        if (cancelled) {
          return;
        }
        setRemoteContentTypes(response.content_types);
        setRemotePlatforms(response.platforms);
        setRemoteStyleTones(response.style_tones);
        setRemoteExamplePrompts(response.example_prompts);
      } catch {
        if (cancelled) {
          return;
        }
        setRemoteContentTypes(null);
        setRemotePlatforms(null);
        setRemoteStyleTones(null);
        setRemoteExamplePrompts(null);
      }
    }

    loadInputOptions();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const presetKey = initialPresetKey;
    if (!presetKey) {
      return;
    }
    const preset = creationPresetMap[presetKey];
    if (!preset) {
      return;
    }
    applyPreset(preset);
  }, [initialPresetKey]);

  async function goNext() {
    const field = steps[currentStep].field;
    const isValid = await trigger(field);
    if (!isValid) {
      return;
    }
    setCurrentStep((value) => Math.min(value + 1, steps.length - 1));
  }

  async function onSubmit(formValues: CreationRequestInput) {
    setSubmitError(null);
    setIsSubmitting(true);

    try {
      const response = await submitCreationRequest(formValues);
      router.push(`/generating/${response.generation_id}`);
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : "提交失败，请稍后重试。");
    } finally {
      setIsSubmitting(false);
    }
  }

  function applyPreset(preset: CreationPreset) {
    setValue("theme_text", preset.payload.theme_text, { shouldValidate: true });
    setValue("content_type", preset.payload.content_type, { shouldValidate: true });
    setValue("target_platform", preset.payload.target_platform, { shouldValidate: true });
    setValue("target_audience_text", preset.payload.target_audience_text, { shouldValidate: true });
    setValue("style_tone", preset.payload.style_tone, { shouldValidate: true });
    setValue("custom_style_text", preset.payload.custom_style_text ?? "", { shouldValidate: true });
    setCurrentStep(0);
    setSubmitError(null);
  }

  return (
    <div className={styles.layout}>
      <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
      <CreationPresetDeck presets={creationPresets} onApply={applyPreset} />
      <ConsistencyPreviewDeck
        themeText={values.theme_text}
        audienceText={values.target_audience_text}
        platformLabel={currentPlatformLabel}
        styleLabel={resolvedStyleTones.find((item) => item.value === values.style_tone)?.label ?? "待选择风格"}
      />
      <section style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 24, padding: 24 }}>
        <p style={{ color: "var(--accent-2)", letterSpacing: "0.12em", margin: 0, textTransform: "uppercase" }}>{progressLabel}</p>
        <h2 style={{ marginBottom: 8 }}>{steps[currentStep].title}</h2>
        <p style={{ color: "var(--muted)", lineHeight: 1.7 }}>{steps[currentStep].description}</p>
      </section>

      {currentStep === 0 ? (
        <section style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 24, padding: 24 }}>
          <label htmlFor="theme_text" style={{ display: "block", fontSize: 18, marginBottom: 12 }}>
            写下这次想做的主题
          </label>
          <textarea
            id="theme_text"
            {...register("theme_text")}
            rows={6}
            style={{ border: "1px solid var(--border)", borderRadius: 18, fontSize: 16, padding: 16, resize: "vertical", width: "100%" }}
          />
          {errors.theme_text ? <p style={{ color: "#b42318" }}>{errors.theme_text.message}</p> : null}
          <div style={{ marginTop: 20 }}>
            <p style={{ marginBottom: 8 }}>可以参考这些写法：</p>
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              {resolvedExamplePrompts.map((prompt) => (
                <li key={prompt} style={{ marginBottom: 8 }}>
                  <button
                    onClick={() => setValue("theme_text", prompt, { shouldValidate: true })}
                    style={{ background: "transparent", border: "none", color: "var(--accent)", cursor: "pointer", padding: 0 }}
                    type="button"
                  >
                    {prompt}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </section>
      ) : null}

      {currentStep === 1 ? (
        <section style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))" }}>
          {resolvedContentTypes.map((option) => (
            <button
              key={option.value}
              onClick={() => setValue("content_type", option.value as CreationRequestInput["content_type"], { shouldValidate: true })}
              style={cardStyle(values.content_type === option.value)}
              type="button"
            >
              <strong>{option.label}</strong>
            </button>
          ))}
          {errors.content_type ? <p style={{ color: "#b42318", gridColumn: "1 / -1" }}>{errors.content_type.message}</p> : null}
        </section>
      ) : null}

      {currentStep === 2 ? (
        <section style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))" }}>
          {resolvedPlatforms.map((option) => (
            <button
              key={option.value}
              onClick={() => setValue("target_platform", option.value as CreationRequestInput["target_platform"], { shouldValidate: true })}
              style={cardStyle(values.target_platform === option.value)}
              type="button"
            >
              <strong>{option.label}</strong>
            </button>
          ))}
          {errors.target_platform ? <p style={{ color: "#b42318", gridColumn: "1 / -1" }}>{errors.target_platform.message}</p> : null}
        </section>
      ) : null}

      {currentStep === 3 ? (
        <section style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 24, padding: 24 }}>
          <label htmlFor="target_audience_text" style={{ display: "block", fontSize: 18, marginBottom: 12 }}>
            描述你希望打动的人
          </label>
          <textarea
            id="target_audience_text"
            {...register("target_audience_text")}
            rows={5}
            style={{ border: "1px solid var(--border)", borderRadius: 18, fontSize: 16, padding: 16, resize: "vertical", width: "100%" }}
          />
          {errors.target_audience_text ? <p style={{ color: "#b42318" }}>{errors.target_audience_text.message}</p> : null}
        </section>
      ) : null}

      {currentStep === 4 ? (
        <section style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 24, padding: 24 }}>
          <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", marginBottom: 18 }}>
            {resolvedStyleTones.map((option) => (
              <button
                key={option.value}
                onClick={() => setValue("style_tone", option.value as CreationRequestInput["style_tone"], { shouldValidate: true })}
                style={cardStyle(values.style_tone === option.value)}
                type="button"
              >
                <strong>{option.label}</strong>
              </button>
            ))}
          </div>
          <label htmlFor="custom_style_text" style={{ display: "block", fontSize: 18, marginBottom: 12 }}>
            可选：补充更细的风格要求
          </label>
          <textarea
            id="custom_style_text"
            {...register("custom_style_text")}
            rows={4}
            style={{ border: "1px solid var(--border)", borderRadius: 18, fontSize: 16, padding: 16, resize: "vertical", width: "100%" }}
          />
          {errors.style_tone ? <p style={{ color: "#b42318" }}>{errors.style_tone.message}</p> : null}
          {errors.custom_style_text ? <p style={{ color: "#b42318" }}>{errors.custom_style_text.message}</p> : null}
        </section>
      ) : null}

      <section style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 24, padding: 24 }}>
        <h3 style={{ marginTop: 0 }}>你刚刚填写的内容</h3>
        <p><strong>主题：</strong>{values.theme_text || "待输入"}</p>
        <p><strong>内容类型：</strong>{currentContentTypeLabel}</p>
        <p><strong>目标平台：</strong>{currentPlatformLabel}</p>
        <p><strong>目标受众：</strong>{values.target_audience_text || "待输入"}</p>
        <p><strong>风格基调：</strong>{resolvedStyleTones.find((item) => item.value === values.style_tone)?.label ?? "待选择"}</p>
        <p><strong>补充说明：</strong>{values.custom_style_text || "无"}</p>
      </section>

      <section className={styles.actions}>
        <button
          onClick={() => setCurrentStep((value) => Math.max(value - 1, 0))}
          style={{ border: "1px solid var(--border)", borderRadius: 999, minWidth: 120, padding: "12px 18px" }}
          disabled={currentStep === 0 || isSubmitting}
          type="button"
        >
          上一步
        </button>
        {currentStep < steps.length - 1 ? (
          <button
            onClick={goNext}
            style={{ background: "var(--accent)", border: "none", borderRadius: 999, color: "white", cursor: "pointer", fontSize: 16, padding: "14px 22px" }}
            disabled={isSubmitting}
            type="button"
          >
            下一步
          </button>
        ) : (
          <button
            disabled={isSubmitting}
            style={{ background: "var(--accent)", border: "none", borderRadius: 999, color: "white", cursor: "pointer", fontSize: 16, opacity: isSubmitting ? 0.65 : 1, padding: "14px 22px" }}
            type="submit"
          >
            {isSubmitting ? "正在提交..." : "开始生成方案"}
          </button>
        )}
      </section>

      {submitError ? (
        <p style={{ background: "rgba(180, 35, 24, 0.08)", border: "1px solid rgba(180, 35, 24, 0.2)", borderRadius: 16, color: "#912018", padding: 16 }}>
          {submitError}
        </p>
      ) : null}
      </form>

      <div className={styles.sidebar}>
        <TrendSignalPanel
          platform={values.target_platform}
          contentType={values.content_type}
          platformLabel={currentPlatformLabel}
          contentTypeLabel={currentContentTypeLabel}
        />
      </div>
    </div>
  );
}
