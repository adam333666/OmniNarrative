"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";
import { gsap } from "gsap";

import styles from "./pill-nav.module.css";

export type PillNavItem = {
  label: string;
  href: string;
  ariaLabel?: string;
};

type PillNavProps = {
  brand: string;
  items: PillNavItem[];
  activeHref?: string;
  className?: string;
  ease?: string;
  baseColor?: string;
  pillColor?: string;
  hoveredPillTextColor?: string;
  pillTextColor?: string;
  initialLoadAnimation?: boolean;
};

export function PillNav({
  brand,
  items,
  activeHref,
  className,
  ease = "power3.easeOut",
  baseColor = "#1a2035",
  pillColor = "#fff8f1",
  hoveredPillTextColor = "#fff8f1",
  pillTextColor = "#1a2035",
  initialLoadAnimation = true,
}: PillNavProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const circleRefs = useRef<Array<HTMLSpanElement | null>>([]);
  const tlRefs = useRef<Array<gsap.core.Timeline | null>>([]);
  const activeTweenRefs = useRef<Array<gsap.core.Tween | null>>([]);
  const navItemsRef = useRef<HTMLDivElement | null>(null);
  const brandRef = useRef<HTMLDivElement | null>(null);
  const menuRef = useRef<HTMLDivElement | null>(null);
  const hamburgerRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    const layout = () => {
      circleRefs.current.forEach((circle) => {
        if (!circle?.parentElement) {
          return;
        }

        const pill = circle.parentElement as HTMLElement;
        const rect = pill.getBoundingClientRect();
        const { width, height } = rect;
        const radius = ((width * width) / 4 + height * height) / (2 * height);
        const diameter = Math.ceil(2 * radius) + 2;
        const delta = Math.ceil(radius - Math.sqrt(Math.max(0, radius * radius - (width * width) / 4))) + 1;
        const originY = diameter - delta;

        circle.style.width = `${diameter}px`;
        circle.style.height = `${diameter}px`;
        circle.style.bottom = `-${delta}px`;

        gsap.set(circle, {
          xPercent: -50,
          scale: 0,
          transformOrigin: `50% ${originY}px`,
        });

        const label = pill.querySelector<HTMLElement>(`.${styles.pillLabel}`);
        const hoverLabel = pill.querySelector<HTMLElement>(`.${styles.pillLabelHover}`);

        if (label) {
          gsap.set(label, { y: 0 });
        }
        if (hoverLabel) {
          gsap.set(hoverLabel, { y: height + 12, opacity: 0 });
        }

        const index = circleRefs.current.indexOf(circle);
        if (index === -1) {
          return;
        }

        tlRefs.current[index]?.kill();
        const timeline = gsap.timeline({ paused: true });
        timeline.to(circle, { scale: 1.2, xPercent: -50, duration: 2, ease, overwrite: "auto" }, 0);
        if (label) {
          timeline.to(label, { y: -(height + 8), duration: 2, ease, overwrite: "auto" }, 0);
        }
        if (hoverLabel) {
          gsap.set(hoverLabel, { y: Math.ceil(height + 100), opacity: 0 });
          timeline.to(hoverLabel, { y: 0, opacity: 1, duration: 2, ease, overwrite: "auto" }, 0);
        }

        tlRefs.current[index] = timeline;
      });
    };

    layout();
    window.addEventListener("resize", layout);

    const menu = menuRef.current;
    if (menu) {
      gsap.set(menu, { visibility: "hidden", opacity: 0, scaleY: 1 });
    }

    if (initialLoadAnimation) {
      if (brandRef.current) {
        gsap.set(brandRef.current, { scale: 0.92, opacity: 0 });
        gsap.to(brandRef.current, { scale: 1, opacity: 1, duration: 0.5, ease });
      }
      if (navItemsRef.current) {
        gsap.set(navItemsRef.current, { width: 0, overflow: "hidden", opacity: 0 });
        gsap.to(navItemsRef.current, { width: "auto", opacity: 1, duration: 0.6, ease });
      }
    }

    return () => window.removeEventListener("resize", layout);
  }, [ease, items, initialLoadAnimation]);

  const handleEnter = (index: number) => {
    const timeline = tlRefs.current[index];
    if (!timeline) {
      return;
    }
    activeTweenRefs.current[index]?.kill();
    activeTweenRefs.current[index] = timeline.tweenTo(timeline.duration(), {
      duration: 0.3,
      ease,
      overwrite: "auto",
    });
  };

  const handleLeave = (index: number) => {
    const timeline = tlRefs.current[index];
    if (!timeline) {
      return;
    }
    activeTweenRefs.current[index]?.kill();
    activeTweenRefs.current[index] = timeline.tweenTo(0, {
      duration: 0.2,
      ease,
      overwrite: "auto",
    });
  };

  const toggleMobileMenu = () => {
    const nextState = !isMobileMenuOpen;
    setIsMobileMenuOpen(nextState);

    if (hamburgerRef.current) {
      const lines = hamburgerRef.current.querySelectorAll(`.${styles.hamburgerLine}`);
      if (nextState) {
        gsap.to(lines[0], { rotation: 45, y: 3, duration: 0.3, ease });
        gsap.to(lines[1], { rotation: -45, y: -3, duration: 0.3, ease });
      } else {
        gsap.to(lines[0], { rotation: 0, y: 0, duration: 0.3, ease });
        gsap.to(lines[1], { rotation: 0, y: 0, duration: 0.3, ease });
      }
    }

    if (menuRef.current) {
      if (nextState) {
        gsap.set(menuRef.current, { visibility: "visible" });
        gsap.fromTo(
          menuRef.current,
          { opacity: 0, y: 10, scaleY: 1 },
          { opacity: 1, y: 0, scaleY: 1, duration: 0.3, ease, transformOrigin: "top center" },
        );
      } else {
        gsap.to(menuRef.current, {
          opacity: 0,
          y: 10,
          scaleY: 1,
          duration: 0.2,
          ease,
          transformOrigin: "top center",
          onComplete: () => {
            if (menuRef.current) {
              gsap.set(menuRef.current, { visibility: "hidden" });
            }
          },
        });
      }
    }
  };

  return (
    <div className={[styles.container, className].filter(Boolean).join(" ")}>
      <nav
        className={styles.nav}
        aria-label="结果页分区导航"
        style={
          {
            ["--base" as string]: baseColor,
            ["--pill-bg" as string]: pillColor,
            ["--hover-text" as string]: hoveredPillTextColor,
            ["--pill-text" as string]: pillTextColor,
          } as CSSProperties
        }
      >
        <div className={styles.brand} ref={brandRef}>
          <span className={styles.brandText}>{brand}</span>
        </div>

        <div className={styles.desktopOnly}>
          <div className={styles.items} ref={navItemsRef}>
            <ul className={styles.list}>
              {items.map((item, index) => (
                <li key={item.href}>
                  <a
                    className={[styles.pill, activeHref === item.href ? styles.activePill : ""].join(" ")}
                    href={item.href}
                    aria-label={item.ariaLabel ?? item.label}
                    onMouseEnter={() => handleEnter(index)}
                    onMouseLeave={() => handleLeave(index)}
                  >
                    <span
                      className={styles.hoverCircle}
                      ref={(el) => {
                        circleRefs.current[index] = el;
                      }}
                    />
                    <span className={styles.labelStack}>
                      <span className={styles.pillLabel}>{item.label}</span>
                      <span className={styles.pillLabelHover}>{item.label}</span>
                    </span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className={styles.mobileOnly}>
          <button
            className={styles.mobileMenuButton}
            ref={hamburgerRef}
            type="button"
            aria-label="Open result navigation"
            onClick={toggleMobileMenu}
          >
            <span className={styles.hamburgerLine} />
            <span className={styles.hamburgerLine} />
          </button>
          <div className={styles.mobileMenuPopover} ref={menuRef}>
            <ul className={styles.mobileMenuList}>
              {items.map((item) => (
                <li key={item.href}>
                  <a className={styles.mobileMenuLink} href={item.href} aria-label={item.ariaLabel ?? item.label}>
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}
