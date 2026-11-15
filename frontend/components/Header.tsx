import Link from "next/link";
import { Layers, Sparkles, Building2, ShieldCheck, Compass } from "lucide-react";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-[#0F141C]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-amber-500 to-amber-700 flex items-center justify-center shadow-lg shadow-amber-900/20 group-hover:scale-105 transition-transform">
            <Compass className="w-6 h-6 text-slate-950 font-bold" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-xl font-bold tracking-tight text-white font-serif">RENDERIZE</span>
              <span className="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
                PRO
              </span>
            </div>
            <p className="text-[11px] text-slate-400 tracking-wide">Architectural Plan AI Studio</p>
          </div>
        </Link>

        <nav className="flex items-center gap-6">
          <div className="hidden md:flex items-center gap-5 text-sm font-medium text-slate-300">
            <Link href="/" className="hover:text-amber-400 transition-colors flex items-center gap-1.5">
              <Layers className="w-4 h-4" /> Studio Dashboard
            </Link>
            <div className="h-4 w-px bg-slate-800" />
            <div className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-full">
              <ShieldCheck className="w-3.5 h-3.5" /> 100% Geometric Accuracy Engine Active
            </div>
          </div>

          <Link
            href="/render/new"
            className="flex items-center gap-2 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-semibold px-4 py-2 rounded-lg text-sm shadow-md shadow-amber-900/20 transition-all hover:shadow-lg active:scale-95"
          >
            <Sparkles className="w-4 h-4" />
            <span>Render New Plan</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
