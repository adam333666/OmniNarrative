"use client";

import { useEffect, useMemo, useRef, useState } from "react";

function formatValue(value: number, decimals: number, separator?: string) {
  const formatted = new Intl.NumberFormat("zh-CN", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
    useGrouping: Boolean(separator),
  }).format(value);

  return separator ? formatted.replace(/,/g, separator) : formatted;
}

export function CountUp({
  to,
  from = 0,
  duration = 1200,
  decimals = 0,
  prefix = "",
  suffix = "",
  separator,
  className,
}: {
  to: number;
  from?: number;
  duration?: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  separator?: string;
  className?: string;
}) {
  const ref = useRef<HTMLSpanElement | null>(null);
  const frameRef = useRef<number | null>(null);
  const [hasStarted, setHasStarted] = useState(false);
  const [value, setValue] = useState(from);

  const displayValue = useMemo(() => {
    return `${prefix}${formatValue(value, decimals, separator)}${suffix}`;
  }, [decimals, prefix, separator, suffix, value]);

  useEffect(() => {
    const target = ref.current;
    if (!target || hasStarted) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) {
          setHasStarted(true);
          observer.disconnect();
        }
      },
      { threshold: 0.45 },
    );

    observer.observe(target);
    return () => observer.disconnect();
  }, [hasStarted]);

  useEffect(() => {
    if (!hasStarted) {
      return;
    }

    const start = performance.now();
    const delta = to - from;

    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const nextValue = from + delta * eased;
      setValue(progress === 1 ? to : nextValue);

      if (progress < 1) {
        frameRef.current = window.requestAnimationFrame(tick);
      }
    };

    frameRef.current = window.requestAnimationFrame(tick);

    return () => {
      if (frameRef.current !== null) {
        window.cancelAnimationFrame(frameRef.current);
      }
    };
  }, [duration, from, hasStarted, to]);

  return (
    <span className={className} ref={ref}>
      {displayValue}
    </span>
  );
}
