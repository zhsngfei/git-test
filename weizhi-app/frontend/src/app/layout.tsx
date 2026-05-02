import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "未至",
  description: "出发之前，先进入一座城市。",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
