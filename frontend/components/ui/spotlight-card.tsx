"use client";

import type { CSSProperties, MouseEventHandler, ReactNode } from "react";

import styles from "./spotlight-card.module.css";

type SpotlightCardProps = {
  children: ReactNode;
  className?: string;
  contentClassName?: string;
  spotlightColor?: string;
};

export function SpotlightCard({
  children,
  className,
  contentClassName,
  spotlightColor = "rgba(255, 245, 235, 0.38)",
}: SpotlightCardProps) {
  const handleMouseMove: MouseEventHandler<HTMLDivElement> = (event) => {
    const target = event.currentTarget;
    const rect = target.getBoundingClientRect();
    target.style.setProperty("--mouse-x", `${event.clientX - rect.left}px`);
    target.style.setProperty("--mouse-y", `${event.clientY - rect.top}px`);
    target.style.setProperty("--spotlight-color", spotlightColor);
  };

  return (
    <div className={[styles.card, className ?? ""].filter(Boolean).join(" ")} onMouseMove={handleMouseMove}>
      <div className={[styles.content, contentClassName ?? ""].filter(Boolean).join(" ")}>{children}</div>
    </div>
  );
}
