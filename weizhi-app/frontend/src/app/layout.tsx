import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "未至",
    template: "%s | 未至",
  },
  description: "出发之前，先进入一座城市。",
  applicationName: "未至",
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "未至",
  },
  formatDetection: {
    telephone: false,
  },
  manifest: "/manifest.webmanifest",
  openGraph: {
    title: "未至",
    description: "出发之前，先进入一座城市。",
    locale: "zh_CN",
    siteName: "未至",
    type: "website",
  },
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
