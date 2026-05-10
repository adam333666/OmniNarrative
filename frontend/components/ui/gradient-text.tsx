import styles from "./gradient-text.module.css";

export function GradientText({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <span className={[styles.gradientText, className].filter(Boolean).join(" ")}>{children}</span>;
}
