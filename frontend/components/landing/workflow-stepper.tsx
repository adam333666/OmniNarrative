"use client";

import { useEffect, useState } from "react";

import styles from "./workflow-stepper.module.css";

export interface WorkflowStep {
  key: string;
  label: string;
  title: string;
  description: string;
}

export function WorkflowStepper({ steps }: { steps: WorkflowStep[] }) {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => {
      setActiveIndex((current) => (current + 1) % steps.length);
    }, 2600);

    return () => window.clearInterval(timer);
  }, [steps.length]);

  return (
    <div className={styles.shell}>
      <div className={styles.header}>
        <div>
          <p className={styles.eyebrow}>使用流程</p>
          <h3 className={styles.title}>从想法到结果的大致步骤</h3>
        </div>
        <p className={styles.summary}>这里用最简洁的方式告诉你，填写、生成、查看结果和导出大概会按什么顺序发生。</p>
      </div>

      <div className={styles.stepRail}>
        {steps.map((step, index) => {
          const status = index === activeIndex ? styles.stepActive : index < activeIndex ? styles.stepComplete : "";
          return (
            <button
              className={`${styles.stepButton} ${status}`.trim()}
              key={step.key}
              onClick={() => setActiveIndex(index)}
              type="button"
            >
              <span className={styles.stepIndex}>{String(index + 1).padStart(2, "0")}</span>
              <span className={styles.stepLabel}>{step.label}</span>
            </button>
          );
        })}
      </div>

      <div className={styles.progressTrack}>
        <div className={styles.progressFill} style={{ width: `${((activeIndex + 1) / steps.length) * 100}%` }} />
      </div>

      <article className={styles.detailCard}>
        <span className={styles.detailBadge}>{steps[activeIndex]?.label}</span>
        <h4 className={styles.detailTitle}>{steps[activeIndex]?.title}</h4>
        <p className={styles.detailDescription}>{steps[activeIndex]?.description}</p>
      </article>
    </div>
  );
}
