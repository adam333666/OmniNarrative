"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import ReactMarkdown from "react-markdown";

import { fetchMarkdownExport } from "@/lib/api-client/backend";

import styles from "./markdown-preview.module.css";

type OutlineItem = {
  id: string;
  level: number;
  text: string;
};

function slugify(value: string) {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^\p{L}\p{N}\s-]/gu, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

function flattenText(children: ReactNode): string {
  if (typeof children === "string" || typeof children === "number") {
    return String(children);
  }

  if (Array.isArray(children)) {
    return children.map((child) => flattenText(child)).join("");
  }

  if (children && typeof children === "object" && "props" in children) {
    return flattenText((children as { props?: { children?: ReactNode } }).props?.children ?? "");
  }

  return "";
}

function extractOutline(markdown: string): OutlineItem[] {
  const counts = new Map<string, number>();

  return markdown
    .split("\n")
    .map((line) => line.match(/^(#{1,3})\s+(.+)$/))
    .filter((match): match is RegExpMatchArray => Boolean(match))
    .map((match) => {
      const level = match[1].length;
      const text = match[2].trim();
      const base = slugify(text) || "section";
      const nextCount = (counts.get(base) ?? 0) + 1;
      counts.set(base, nextCount);

      return {
        id: nextCount === 1 ? base : base + "-" + nextCount,
        level,
        text,
      };
    });
}

export function MarkdownPreview({ generationId }: { generationId: string }) {
  const [markdown, setMarkdown] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [retryNonce, setRetryNonce] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function loadMarkdown() {
      try {
        const response = await fetchMarkdownExport(generationId);
        if (!cancelled) {
          setMarkdown(response);
          setError(null);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(requestError instanceof Error ? requestError.message : "Markdown 预览加载失败。");
        }
      }
    }

    loadMarkdown();
    return () => {
      cancelled = true;
    };
  }, [generationId, retryNonce]);

  const outline = useMemo(() => {
    if (!markdown) {
      return [];
    }

    return extractOutline(markdown);
  }, [markdown]);

  const headingIds = useMemo(() => {
    const lookup = new Map<string, string[]>();

    outline.forEach((item) => {
      const base = slugify(item.text) || "section";
      const bucket = lookup.get(base) ?? [];
      bucket.push(item.id);
      lookup.set(base, bucket);
    });

    return lookup;
  }, [outline]);

  const headingUsage = new Map<string, number>();

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <h3 className={styles.title}>Markdown 预览</h3>
        <span className={styles.lead}>这里会展示适合阅读和讨论的文本版本，方便你先通读一遍再决定是否导出。</span>
      </div>

      <div className={styles.summaryGrid}>
        <article className={styles.summaryCard}>
          <span className={styles.summaryLabel}>内容来源</span>
          <p className={styles.summaryValue}>当前结果的 Markdown 版本</p>
        </article>
        <article className={styles.summaryCard}>
          <span className={styles.summaryLabel}>阅读方式</span>
          <p className={styles.summaryValue}>先看结构，再读正文</p>
        </article>
        <article className={styles.summaryCard}>
          <span className={styles.summaryLabel}>章节目录</span>
          <p className={styles.summaryValue}>{outline.length > 0 ? `已识别 ${outline.length} 个标题` : "正文加载后自动识别标题"}</p>
        </article>
      </div>

      {outline.length > 0 ? (
        <nav aria-label="Markdown 目录导航" className={styles.outlineNav}>
          <div className={styles.outlineRail}>
            {outline.map((item) => (
              <a className={styles.outlinePill} data-level={item.level} href={`#${item.id}`} key={item.id}>
                {item.text}
              </a>
            ))}
          </div>
        </nav>
      ) : null}

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
      {!markdown && !error ? <p className={styles.status}>正在加载内容预览...</p> : null}
      {markdown ? (
        <div className={styles.markdown}>
          <ReactMarkdown
            components={{
              h1({ children }) {
                const text = flattenText(children);
                const base = slugify(text) || "section";
                const nextIndex = headingUsage.get(base) ?? 0;
                headingUsage.set(base, nextIndex + 1);
                const id = headingIds.get(base)?.[nextIndex] ?? base + "-" + (nextIndex + 1);

                return (
                  <h1 id={id}>
                    {children}
                  </h1>
                );
              },
              h2({ children }) {
                const text = flattenText(children);
                const base = slugify(text) || "section";
                const nextIndex = headingUsage.get(base) ?? 0;
                headingUsage.set(base, nextIndex + 1);
                const id = headingIds.get(base)?.[nextIndex] ?? base + "-" + (nextIndex + 1);

                return (
                  <h2 id={id}>
                    {children}
                  </h2>
                );
              },
              h3({ children }) {
                const text = flattenText(children);
                const base = slugify(text) || "section";
                const nextIndex = headingUsage.get(base) ?? 0;
                headingUsage.set(base, nextIndex + 1);
                const id = headingIds.get(base)?.[nextIndex] ?? base + "-" + (nextIndex + 1);

                return (
                  <h3 id={id}>
                    {children}
                  </h3>
                );
              },
            }}
          >
            {markdown}
          </ReactMarkdown>
        </div>
      ) : null}
    </div>
  );
}
