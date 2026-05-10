import type { CSSProperties, ReactNode } from "react";

import styles from "./shiny-text.module.css";

type ShinyTextProps = {
  children: ReactNode;
  className?: string;
  baseColor?: string;
  highlightColor?: string;
  durationSeconds?: number;
  angleDeg?: number;
  pauseOnHover?: boolean;
  disabled?: boolean;
};

export function ShinyText({
  children,
  className,
  baseColor = "rgba(180, 79, 44, 0.88)",
  highlightColor = "rgba(255, 247, 234, 0.98)",
  durationSeconds = 5,
  angleDeg = 120,
  pauseOnHover = false,
  disabled = false,
}: ShinyTextProps) {
  const style = {
    "--shiny-base": baseColor,
    "--shiny-highlight": highlightColor,
    "--shiny-duration": `${durationSeconds}s`,
    "--shiny-angle": `${angleDeg}deg`,
  } as CSSProperties;

  return (
    <span
      className={[styles.shiny, disabled ? styles.paused : "", className ?? ""].filter(Boolean).join(" ")}
      data-pause-on-hover={pauseOnHover ? "true" : "false"}
      style={style}
    >
      {children}
    </span>
  );
}
