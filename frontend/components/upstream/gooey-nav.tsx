"use client";

import { useEffect, useRef, useState } from "react";

import styles from "./gooey-nav.module.css";

type GooeyNavItem = {
  label: string;
  href: string;
};

type GooeyNavProps = {
  items: GooeyNavItem[];
  initialActiveIndex?: number;
  className?: string;
};

export function GooeyNav({ items, initialActiveIndex = 0, className }: GooeyNavProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const navRef = useRef<HTMLUListElement>(null);
  const filterRef = useRef<HTMLSpanElement>(null);
  const textRef = useRef<HTMLSpanElement>(null);
  const [activeIndex, setActiveIndex] = useState(initialActiveIndex);

  const noise = (n = 1) => n / 2 - Math.random() * n;

  const getXY = (distance: number, pointIndex: number, totalPoints: number): [number, number] => {
    const angle = ((360 + noise(8)) / totalPoints) * pointIndex * (Math.PI / 180);
    return [distance * Math.cos(angle), distance * Math.sin(angle)];
  };

  const createParticle = (index: number) => {
    const particleCount = 15;
    const particleDistances: [number, number] = [90, 10];
    const particleR = 100;
    const animationTime = 600;
    const timeVariance = 300;
    const colors = [1, 2, 3, 1, 2, 3, 1, 4];
    const rotate = noise(particleR / 10);

    return {
      start: getXY(particleDistances[0], particleCount - index, particleCount),
      end: getXY(particleDistances[1] + noise(7), particleCount - index, particleCount),
      time: animationTime * 2 + noise(timeVariance * 2),
      scale: 1 + noise(0.2),
      color: colors[Math.floor(Math.random() * colors.length)],
      rotate: rotate > 0 ? (rotate + particleR / 20) * 10 : (rotate - particleR / 20) * 10,
    };
  };

  const updateEffectPosition = (element: HTMLElement) => {
    if (!containerRef.current || !filterRef.current || !textRef.current) {
      return;
    }
    const containerRect = containerRef.current.getBoundingClientRect();
    const pos = element.getBoundingClientRect();

    const nextStyles = {
      left: `${pos.x - containerRect.x}px`,
      top: `${pos.y - containerRect.y}px`,
      width: `${pos.width}px`,
      height: `${pos.height}px`,
    };

    Object.assign(filterRef.current.style, nextStyles);
    Object.assign(textRef.current.style, nextStyles);
    textRef.current.innerText = element.innerText;
  };

  const makeParticles = (element: HTMLElement) => {
    const animationTime = 600;
    const timeVariance = 300;
    const particleCount = 15;

    element.style.setProperty("--time", `${animationTime * 2 + timeVariance}ms`);
    element.classList.remove(styles.active);

    for (let index = 0; index < particleCount; index += 1) {
      const particleConfig = createParticle(index);
      window.setTimeout(() => {
        const particle = document.createElement("span");
        const point = document.createElement("span");

        particle.classList.add(styles.particle);
        particle.style.setProperty("--start-x", `${particleConfig.start[0]}px`);
        particle.style.setProperty("--start-y", `${particleConfig.start[1]}px`);
        particle.style.setProperty("--end-x", `${particleConfig.end[0]}px`);
        particle.style.setProperty("--end-y", `${particleConfig.end[1]}px`);
        particle.style.setProperty("--time", `${particleConfig.time}ms`);
        particle.style.setProperty("--scale", `${particleConfig.scale}`);
        particle.style.setProperty("--color", `var(--gooey-color-${particleConfig.color})`);
        particle.style.setProperty("--rotate", `${particleConfig.rotate}deg`);

        point.classList.add(styles.point);
        particle.appendChild(point);
        element.appendChild(particle);

        requestAnimationFrame(() => {
          element.classList.add(styles.active);
        });

        window.setTimeout(() => {
          if (element.contains(particle)) {
            element.removeChild(particle);
          }
        }, particleConfig.time);
      }, 30);
    }
  };

  const activate = (element: HTMLElement, index: number) => {
    if (activeIndex === index) {
      return;
    }

    setActiveIndex(index);
    updateEffectPosition(element);

    if (filterRef.current) {
      filterRef.current.querySelectorAll(`.${styles.particle}`).forEach((particle) => particle.remove());
      makeParticles(filterRef.current);
    }

    if (textRef.current) {
      textRef.current.classList.remove(styles.active);
      void textRef.current.offsetWidth;
      textRef.current.classList.add(styles.active);
    }
  };

  useEffect(() => {
    if (!navRef.current || !containerRef.current) {
      return;
    }

    const currentActive = navRef.current.querySelectorAll("li")[activeIndex] as HTMLElement | undefined;
    if (currentActive) {
      updateEffectPosition(currentActive);
      textRef.current?.classList.add(styles.active);
    }

    const observer = new ResizeObserver(() => {
      const activeElement = navRef.current?.querySelectorAll("li")[activeIndex] as HTMLElement | undefined;
      if (activeElement) {
        updateEffectPosition(activeElement);
      }
    });

    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [activeIndex]);

  return (
    <div className={[styles.container, className].filter(Boolean).join(" ")} ref={containerRef}>
      <nav className={styles.nav}>
        <ul ref={navRef}>
          {items.map((item, index) => (
            <li className={activeIndex === index ? styles.itemActive : ""} key={item.href}>
              <a
                href={item.href}
                onClick={(event) => {
                  activate(event.currentTarget.parentElement ?? event.currentTarget, index);
                }}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    activate(event.currentTarget.parentElement ?? event.currentTarget, index);
                  }
                }}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <span className={`${styles.effect} ${styles.filter}`} ref={filterRef} />
      <span className={`${styles.effect} ${styles.text}`} ref={textRef} />
    </div>
  );
}
