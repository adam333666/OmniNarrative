import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "内容创作助手",
  description: "把一句想法整理成可继续修改、导出和制作的内容方案",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
