import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "VC Intelligence - Investor Search & Analytics",
  description: "Search and analyze VC firms, family offices, and institutional investors with SEC data",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
