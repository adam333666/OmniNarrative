"use client";

import { useEffect, useMemo, useState } from "react";

import styles from "./animated-decision-list.module.css";

export function AnimatedDecisionList({ items }: { items: string[] }) {
  const [activeIndex, setActiveIndex] = useState(0);
  const safeItems = useMemo(() => items.filter(Boolean), [items]);

  useEffect(() => {
    setActiveIndex(0);
  }, [safeItems.length]);

  if (safeItems.length === 0) {
    return null;
  }

  return (
    <div className={styles.shell}>
      <div className={styles.header}>
        <p className={styles.eyebrow}>Decision Focus</p>
        <h4 className={styles.title}>关键设计决策</h4>
      </div>

      <div className={styles.list} role="list">
        {safeItems.map((item, index) => {
          const active = index === activeIndex;
          return (
            <button
              aria-pressed={active}
              className={`${styles.item} ${active ? styles.itemActive : ""}`.trim()}
              key={item}
              onFocus={() => setActiveIndex(index)}
              onMouseEnter={() => setActiveIndex(index)}
              type="button"
            >
              <span className={styles.index}>{String(index + 1).padStart(2, "0")}</span>
              <span className={styles.copy}>{item}</span>
            </button>
          );
        })}
      </div>

      <div className={styles.focusPanel}>
        <span className={styles.focusLabel}>当前聚焦</span>
        <p className={styles.focusCopy}>{safeItems[activeIndex]}</p>
      </div>
    </div>
  );
}
