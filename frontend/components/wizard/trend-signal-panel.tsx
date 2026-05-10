"use client";

import { useEffect, useMemo, useState } from "react";

import { fetchTrendTemplates, type TrendTemplateSummary } from "@/lib/api-client/backend";
import { DotGrid } from "@/components/upstream/dot-grid";
import { TextType } from "@/components/upstream/text-type";
import { TrendStrategyDeck } from "@/components/wizard/trend-strategy-deck";

import styles from "./trend-signal-panel.module.css";

type TrendSignalPanelProps = {
  platform: string;
  contentType: string;
  platformLabel: string;
  contentTypeLabel: string;
};

export function TrendSignalPanel({
  platform,
  contentType,
  platformLabel,
  contentTypeLabel,
}: TrendSignalPanelProps) {
  const [items, setItems] = useState<TrendTemplateSummary[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function loadTemplates() {
      setLoading(true);
      try {
        const response = await fetchTrendTemplates(platform, contentType === "auto" ? undefined : contentType);
        if (cancelled) {
          return;
        }
        setItems(response.items);
        setError(null);
      } catch (requestError) {
        if (cancelled) {
          return;
        }
        setItems([]);
        setError(requestError instanceof Error ? requestError.message : "趋势摘要暂时不可用。");
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadTemplates();
    return () => {
      cancelled = true;
    };
  }, [platform, contentType]);

  const activeItem = items[0] ?? null;
  const textPhrases = useMemo(
    () => [
      `${platformLabel} 当前更偏好什么开场节奏？`,
      `${contentTypeLabel} 题材在这个平台最近更容易怎么起手？`,
      "先看参考提示，再决定标题、开场和封面方向。",
    ],
    [platformLabel, contentTypeLabel],
  );

  return (
    <aside className={styles.panel}>
      <div className={styles.gridLayer}>
        <DotGrid
          baseColor="#ffb48c"
          activeColor="#fff2e7"
          dotSize={8}
          gap={22}
          proximity={120}
          shockRadius={180}
          shockStrength={3}
          speedTrigger={60}
        />
      </div>

      <div className={styles.content}>
        <span className={styles.eyebrow}>参考提示</span>
        <div>
          <h3 className={styles.title}>先看这类内容最近怎么更容易起手</h3>
          <p className={styles.lead}>
            你当前选择的是 {platformLabel} / {contentTypeLabel}。先扫一眼这些参考提示，再决定标题、开场和表达方式，会更省力。
          </p>
        </div>

        <div className={styles.heroPhrase}>
          <TextType
            as="p"
            text={textPhrases}
            typingSpeed={28}
            deletingSpeed={18}
            pauseDuration={1200}
            initialDelay={200}
            cursorBlinkDuration={0.4}
            textColors={["#ffd7c4", "#fff0e8", "#ffc39c"]}
          />
        </div>

        {loading ? <p className={styles.loading}>正在读取这一步可参考的提示...</p> : null}
        {error ? <p className={styles.error}>{error}</p> : null}

        {!loading && !error && activeItem ? (
          <section className={styles.summaryCard}>
            <div className={styles.summaryHeader}>
              <h4 className={styles.summaryTitle}>这一步最值得先参考的方向</h4>
              <span className={styles.summaryMeta}>{activeItem.source_type}</span>
            </div>
            <p className={styles.summaryText}>{activeItem.summary}</p>
            <div className={styles.chipWrap}>
              {activeItem.hot_topics_summary.map((topic) => (
                <span className={styles.chip} key={topic}>
                  {topic}
                </span>
              ))}
            </div>

            {activeItem.source_trace.length > 0 ? (
              <div className={styles.traceSection}>
                <div className={styles.traceHeader}>
                  <span className={styles.traceBadge}>参考来源</span>
                  <span className={styles.traceLead}>如果你想知道这些建议从哪里来，可以先看这几条来源。</span>
                </div>

                <div className={styles.traceList}>
                  {activeItem.source_trace.slice(0, 2).map((trace) => (
                    <article className={styles.traceItem} key={`${trace.source_name}-${trace.title}`}>
                      <span className={styles.traceSource}>{trace.source_name}</span>
                      <h5 className={styles.traceTitle}>
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
          </section>
        ) : null}

        {!loading && !error && activeItem ? <TrendStrategyDeck item={activeItem} /> : null}

        {!loading && !error && items.length > 1 ? (
          <div className={styles.list}>
            {items.slice(1, 3).map((item) => (
              <div className={styles.listItem} key={`${item.platform}-${item.content_type}`}>
                <h5 className={styles.listItemTitle}>
                  {item.platform} / {item.content_type}
                </h5>
                <p className={styles.listItemBody}>{item.summary}</p>
              </div>
            ))}
          </div>
        ) : null}

        {!loading && !error && items.length === 0 ? (
          <div className={styles.empty}>当前没有额外参考提示也没关系，你仍然可以继续填写，系统会结合基础规则继续生成。</div>
        ) : null}
      </div>
    </aside>
  );
}
