import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "Renderize | AI-Powered Architectural Plan Rendering SaaS",
  description: "Transform technical CAD blueprints into publication-grade architectural presentation plans with 100% geometric fidelity.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="stylesheet" href="/tailwind.css" />
      </head>
      <body className="font-sans bg-[#0A0D14] text-slate-100 min-h-screen antialiased flex flex-col">
        <Header />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="border-t border-slate-800/80 bg-[#0F141C] py-6 text-center text-xs text-slate-500 font-mono">
          Renderize Architectural AI Studio &bull; Precision CAD-to-Presentation Engine &bull; Zero Geometric Drift Guarantee
        </footer>
      </body>
    </html>
  );
}
