import type { ReactNode } from "react";

import { FlowStageBanner, type FlowStageBannerProps } from "@/components/layout/flow-stage-banner";

import styles from "./site-shell.module.css";

type SiteShellProps = {
  title: string;
  eyebrow?: string;
  description: string;
  children: ReactNode;
  banner?: FlowStageBannerProps;
};

export function SiteShell({ title, eyebrow, description, children, banner }: SiteShellProps) {
  return (
    <main className={styles.shell}>
      <div className={styles.container}>
        <header className={styles.header}>
          {eyebrow ? (
            <p className={styles.eyebrow}>{eyebrow}</p>
          ) : null}
          <h1 className={styles.title}>{title}</h1>
          <p className={styles.description}>{description}</p>
        </header>
        {banner ? <FlowStageBanner {...banner} /> : null}
        {children}
      </div>
    </main>
  );
}
