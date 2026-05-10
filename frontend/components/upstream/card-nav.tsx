"use client";

import { useLayoutEffect, useRef, useState } from "react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { gsap } from "gsap";

import styles from "./card-nav.module.css";

type CardNavLink = {
  label: string;
  href: string;
  ariaLabel: string;
};

export type CardNavItem = {
  label: string;
  bgColor: string;
  textColor: string;
  links: CardNavLink[];
};

type CardNavProps = {
  brand: string;
  items: CardNavItem[];
  className?: string;
  ease?: string;
  baseColor?: string;
  menuColor?: string;
  buttonBgColor?: string;
  buttonTextColor?: string;
  ctaHref?: string;
  ctaLabel?: string;
};

export function CardNav({
  brand,
  items,
  className,
  ease = "power3.out",
  baseColor = "#fffaf3",
  menuColor = "#1a2035",
  buttonBgColor = "#1a2035",
  buttonTextColor = "#fffaf3",
  ctaHref = "/create",
  ctaLabel = "开始创作",
}: CardNavProps) {
  const [isHamburgerOpen, setIsHamburgerOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const navRef = useRef<HTMLDivElement | null>(null);
  const cardsRef = useRef<HTMLDivElement[]>([]);
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  const calculateHeight = () => {
    const navEl = navRef.current;
    if (!navEl) {
      return 260;
    }

    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    if (isMobile) {
      const contentEl = navEl.querySelector(`.${styles.content}`) as HTMLElement | null;
      if (contentEl) {
        const wasVisibility = contentEl.style.visibility;
        const wasPointerEvents = contentEl.style.pointerEvents;
        const wasPosition = contentEl.style.position;
        const wasHeight = contentEl.style.height;

        contentEl.style.visibility = "visible";
        contentEl.style.pointerEvents = "auto";
        contentEl.style.position = "static";
        contentEl.style.height = "auto";

        contentEl.offsetHeight;

        const topBar = 60;
        const padding = 16;
        const contentHeight = contentEl.scrollHeight;

        contentEl.style.visibility = wasVisibility;
        contentEl.style.pointerEvents = wasPointerEvents;
        contentEl.style.position = wasPosition;
        contentEl.style.height = wasHeight;

        return topBar + contentHeight + padding;
      }
    }

    return 260;
  };

  const createTimeline = () => {
    const navEl = navRef.current;
    if (!navEl) {
      return null;
    }

    gsap.set(navEl, { height: 60, overflow: "hidden" });
    gsap.set(cardsRef.current, { y: 50, opacity: 0 });

    const timeline = gsap.timeline({ paused: true });
    timeline.to(navEl, {
      height: calculateHeight,
      duration: 0.4,
      ease,
    });
    timeline.to(
      cardsRef.current,
      { y: 0, opacity: 1, duration: 0.4, ease, stagger: 0.08 },
      "-=0.1",
    );

    return timeline;
  };

  useLayoutEffect(() => {
    const timeline = createTimeline();
    tlRef.current = timeline;

    return () => {
      timeline?.kill();
      tlRef.current = null;
    };
  }, [ease, items]);

  useLayoutEffect(() => {
    const handleResize = () => {
      if (!tlRef.current) {
        return;
      }

      if (isExpanded) {
        gsap.set(navRef.current, { height: calculateHeight() });
        tlRef.current.kill();
        const nextTimeline = createTimeline();
        if (nextTimeline) {
          nextTimeline.progress(1);
          tlRef.current = nextTimeline;
        }
        return;
      }

      tlRef.current.kill();
      tlRef.current = createTimeline();
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [isExpanded]);

  const toggleMenu = () => {
    const timeline = tlRef.current;
    if (!timeline) {
      return;
    }

    if (!isExpanded) {
      setIsHamburgerOpen(true);
      setIsExpanded(true);
      timeline.play(0);
      return;
    }

    setIsHamburgerOpen(false);
    timeline.eventCallback("onReverseComplete", () => setIsExpanded(false));
    timeline.reverse();
  };

  const setCardRef = (index: number) => (element: HTMLDivElement | null) => {
    if (element) {
      cardsRef.current[index] = element;
    }
  };

  return (
    <div className={[styles.container, className].filter(Boolean).join(" ")}>
      <nav ref={navRef} className={[styles.nav, isExpanded ? styles.open : ""].join(" ")} style={{ backgroundColor: baseColor }}>
        <div className={styles.top}>
          <div
            className={[styles.hamburger, isHamburgerOpen ? styles.hamburgerOpen : ""].join(" ")}
            onClick={toggleMenu}
            role="button"
            aria-label={isExpanded ? "Close menu" : "Open menu"}
            tabIndex={0}
            style={{ color: menuColor }}
            onKeyDown={(event) => {
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                toggleMenu();
              }
            }}
          >
            <div className={styles.hamburgerLine} />
            <div className={styles.hamburgerLine} />
          </div>

          <div className={styles.brandContainer}>
            <span className={styles.brandText}>{brand}</span>
          </div>

          <Link
            href={ctaHref}
            className={styles.ctaButton}
            style={{ backgroundColor: buttonBgColor, color: buttonTextColor }}
          >
            {ctaLabel}
          </Link>
        </div>

        <div className={styles.content} aria-hidden={!isExpanded}>
          {items.slice(0, 3).map((item, index) => (
            <div
              key={`${item.label}-${index}`}
              className={styles.navCard}
              ref={setCardRef(index)}
              style={{ backgroundColor: item.bgColor, color: item.textColor }}
            >
              <div className={styles.navCardLabel}>{item.label}</div>
              <div className={styles.navCardLinks}>
                {item.links.map((link, linkIndex) => (
                  <Link
                    key={`${link.label}-${linkIndex}`}
                    className={styles.navCardLink}
                    href={link.href}
                    aria-label={link.ariaLabel}
                  >
                    <ArrowUpRight className={styles.navCardLinkIcon} aria-hidden="true" size={15} />
                    {link.label}
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>
      </nav>
    </div>
  );
}
