"use client";

import { useCallback, useEffect, useRef, type ReactNode } from "react";

import styles from "./border-glow.module.css";

type BorderGlowProps = {
  children: ReactNode;
  className?: string;
  edgeSensitivity?: number;
  glowColor?: string;
  backgroundColor?: string;
  borderRadius?: number;
  glowRadius?: number;
  glowIntensity?: number;
  coneSpread?: number;
  colors?: string[];
  fillOpacity?: number;
};

function parseHsl(hslStr: string): { h: number; s: number; l: number } {
  const match = hslStr.match(/([\d.]+)\s*([\d.]+)%?\s*([\d.]+)%?/);
  if (!match) {
    return { h: 40, s: 80, l: 80 };
  }
  return { h: Number.parseFloat(match[1]), s: Number.parseFloat(match[2]), l: Number.parseFloat(match[3]) };
}

function buildGlowVars(glowColor: string, intensity: number): Record<string, string> {
  const { h, s, l } = parseHsl(glowColor);
  const base = `${h}deg ${s}% ${l}%`;
  const opacities = [100, 60, 50, 40, 30, 20, 10];
  const keys = ["", "-60", "-50", "-40", "-30", "-20", "-10"];
  const result: Record<string, string> = {};
  for (let index = 0; index < opacities.length; index += 1) {
    result[`--glow-color${keys[index]}`] = `hsl(${base} / ${Math.min(opacities[index] * intensity, 100)}%)`;
  }
  return result;
}

const GRADIENT_POSITIONS = ["80% 55%", "69% 34%", "8% 6%", "41% 38%", "86% 85%", "82% 18%", "51% 4%"];
const GRADIENT_KEYS = [
  "--gradient-one",
  "--gradient-two",
  "--gradient-three",
  "--gradient-four",
  "--gradient-five",
  "--gradient-six",
  "--gradient-seven",
];
const COLOR_MAP = [0, 1, 2, 0, 1, 2, 1];

function buildGradientVars(colors: string[]): Record<string, string> {
  const result: Record<string, string> = {};
  for (let index = 0; index < 7; index += 1) {
    const color = colors[Math.min(COLOR_MAP[index], colors.length - 1)];
    result[GRADIENT_KEYS[index]] = `radial-gradient(at ${GRADIENT_POSITIONS[index]}, ${color} 0px, transparent 50%)`;
  }
  result["--gradient-base"] = `linear-gradient(${colors[0]} 0 100%)`;
  return result;
}

export function BorderGlow({
  children,
  className = "",
  edgeSensitivity = 30,
  glowColor = "28 88 67",
  backgroundColor = "rgba(255, 252, 246, 0.96)",
  borderRadius = 28,
  glowRadius = 36,
  glowIntensity = 1,
  coneSpread = 25,
  colors = ["rgba(239, 124, 72, 0.9)", "rgba(63, 140, 126, 0.85)", "rgba(255, 223, 160, 0.84)"],
  fillOpacity = 0.42,
}: BorderGlowProps) {
  const cardRef = useRef<HTMLDivElement>(null);

  const getCenterOfElement = useCallback((element: HTMLElement) => {
    const { width, height } = element.getBoundingClientRect();
    return [width / 2, height / 2];
  }, []);

  const getEdgeProximity = useCallback(
    (element: HTMLElement, x: number, y: number) => {
      const [centerX, centerY] = getCenterOfElement(element);
      const deltaX = x - centerX;
      const deltaY = y - centerY;
      let ratioX = Number.POSITIVE_INFINITY;
      let ratioY = Number.POSITIVE_INFINITY;
      if (deltaX !== 0) {
        ratioX = centerX / Math.abs(deltaX);
      }
      if (deltaY !== 0) {
        ratioY = centerY / Math.abs(deltaY);
      }
      return Math.min(Math.max(1 / Math.min(ratioX, ratioY), 0), 1);
    },
    [getCenterOfElement],
  );

  const getCursorAngle = useCallback(
    (element: HTMLElement, x: number, y: number) => {
      const [centerX, centerY] = getCenterOfElement(element);
      const deltaX = x - centerX;
      const deltaY = y - centerY;
      if (deltaX === 0 && deltaY === 0) {
        return 0;
      }
      const radians = Math.atan2(deltaY, deltaX);
      let degrees = radians * (180 / Math.PI) + 90;
      if (degrees < 0) {
        degrees += 360;
      }
      return degrees;
    },
    [getCenterOfElement],
  );

  useEffect(() => {
    const element = cardRef.current;
    if (!element) {
      return;
    }

    function handlePointerMove(event: PointerEvent) {
      const current = cardRef.current;
      if (!current) {
        return;
      }
      const rect = current.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      const edge = getEdgeProximity(current, x, y);
      const angle = getCursorAngle(current, x, y);
      current.style.setProperty("--edge-proximity", `${(edge * 100).toFixed(3)}`);
      current.style.setProperty("--cursor-angle", `${angle.toFixed(3)}deg`);
    }

    element.addEventListener("pointermove", handlePointerMove);
    return () => {
      element.removeEventListener("pointermove", handlePointerMove);
    };
  }, [getCursorAngle, getEdgeProximity]);

  return (
    <div
      ref={cardRef}
      className={`${styles.card} ${className}`.trim()}
      style={
        {
          "--card-bg": backgroundColor,
          "--edge-sensitivity": edgeSensitivity,
          "--border-radius": `${borderRadius}px`,
          "--glow-padding": `${glowRadius}px`,
          "--cone-spread": coneSpread,
          "--fill-opacity": fillOpacity,
          ...buildGlowVars(glowColor, glowIntensity),
          ...buildGradientVars(colors),
        } as React.CSSProperties
      }
    >
      <span className={styles.edgeLight} />
      <div className={styles.inner}>{children}</div>
    </div>
  );
}
