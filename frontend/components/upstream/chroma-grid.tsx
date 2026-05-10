"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";

import styles from "./chroma-grid.module.css";

export type ChromaGridItem = {
  title: string;
  subtitle: string;
  handle?: string;
  location?: string;
  borderColor?: string;
  gradient?: string;
  preview?: string;
  url?: string;
};

type ChromaGridProps = {
  items: ChromaGridItem[];
  className?: string;
  radius?: number;
  columns?: number;
  rows?: number;
  damping?: number;
  fadeOut?: number;
  ease?: string;
};

type SetterFn = (value: number | string) => void;

export function ChromaGrid({
  items,
  className = "",
  radius = 300,
  columns = 3,
  rows = 2,
  damping = 0.45,
  fadeOut = 0.6,
  ease = "power3.out",
}: ChromaGridProps) {
  const rootRef = useRef<HTMLDivElement>(null);
  const fadeRef = useRef<HTMLDivElement>(null);
  const setX = useRef<SetterFn | null>(null);
  const setY = useRef<SetterFn | null>(null);
  const pos = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const element = rootRef.current;
    if (!element) {
      return;
    }

    setX.current = gsap.quickSetter(element, "--x", "px") as SetterFn;
    setY.current = gsap.quickSetter(element, "--y", "px") as SetterFn;
    const { width, height } = element.getBoundingClientRect();
    pos.current = { x: width / 2, y: height / 2 };
    setX.current(pos.current.x);
    setY.current(pos.current.y);
  }, []);

  function moveTo(x: number, y: number) {
    gsap.to(pos.current, {
      x,
      y,
      duration: damping,
      ease,
      onUpdate: () => {
        setX.current?.(pos.current.x);
        setY.current?.(pos.current.y);
      },
      overwrite: true,
    });
  }

  function handleMove(event: React.PointerEvent) {
    const rect = rootRef.current?.getBoundingClientRect();
    if (!rect) {
      return;
    }
    moveTo(event.clientX - rect.left, event.clientY - rect.top);
    gsap.to(fadeRef.current, { opacity: 0, duration: 0.25, overwrite: true });
  }

  function handleLeave() {
    gsap.to(fadeRef.current, {
      opacity: 1,
      duration: fadeOut,
      overwrite: true,
    });
  }

  function handleCardMove(event: React.MouseEvent<HTMLElement>) {
    const card = event.currentTarget;
    const rect = card.getBoundingClientRect();
    card.style.setProperty("--mouse-x", `${event.clientX - rect.left}px`);
    card.style.setProperty("--mouse-y", `${event.clientY - rect.top}px`);
  }

  function handleCardClick(url?: string) {
    if (!url) {
      return;
    }
    window.open(url, "_self");
  }

  return (
    <div
      ref={rootRef}
      className={`${styles.grid} ${className}`.trim()}
      style={
        {
          "--r": `${radius}px`,
          "--cols": columns,
          "--rows": rows,
        } as React.CSSProperties
      }
      onPointerMove={handleMove}
      onPointerLeave={handleLeave}
    >
      {items.map((item) => (
        <article
          className={styles.card}
          key={`${item.title}-${item.subtitle}`}
          onClick={() => handleCardClick(item.url)}
          onMouseMove={handleCardMove}
          style={
            {
              "--card-border": item.borderColor ?? "rgba(239, 124, 72, 0.44)",
              "--card-gradient":
                item.gradient ?? "linear-gradient(145deg, rgba(29, 34, 56, 0.98), rgba(11, 14, 24, 0.96))",
              cursor: item.url ? "pointer" : "default",
            } as React.CSSProperties
          }
        >
          <div className={styles.previewShell}>
            <div className={styles.previewCard}>{item.preview ?? item.title}</div>
          </div>

          <footer className={styles.info}>
            <h3 className={styles.name}>{item.title}</h3>
            {item.handle ? <span className={styles.handle}>{item.handle}</span> : null}
            <p className={styles.role}>{item.subtitle}</p>
            {item.location ? <span className={styles.location}>{item.location}</span> : null}
          </footer>
        </article>
      ))}
      <div className={styles.overlay} />
      <div ref={fadeRef} className={styles.fade} />
    </div>
  );
}
