import Dropzone from "@/components/Dropzone";
import { ArrowLeft, Sparkles, Shield, Palette } from "lucide-react";
import Link from "next/link";

export default function NewRenderPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div>
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors mb-4"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Studio Dashboard</span>
        </Link>
        <h1 className="text-2xl md:text-3xl font-bold text-white font-serif">
          Upload Floor Plan Drawing
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Our architectural engine will extract vector paths, classify room functions, and render publication-grade materials.
        </p>
      </div>

      {/* Main Upload Box */}
      <Dropzone />

      {/* Feature Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-slate-300 space-y-2">
          <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
            <Shield className="w-4 h-4" />
          </div>
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">Zero Wall Distortion</h4>
          <p className="text-xs text-slate-400 leading-relaxed">
            Walls and dimensions are never modified, moved, or deleted. 100% geometric line retention guaranteed.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-slate-300 space-y-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <Palette className="w-4 h-4" />
          </div>
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">Authentic Materials</h4>
          <p className="text-xs text-slate-400 leading-relaxed">
            Herringbone French oak, Calacatta marble, honed sage quartzite, and textured terrazzo tiles.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-slate-300 space-y-2">
          <div className="w-8 h-8 rounded-lg bg-sky-500/10 text-sky-400 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <h4 className="text-xs font-bold text-white uppercase tracking-wider">A1 Presentation PDF</h4>
          <p className="text-xs text-slate-400 leading-relaxed">
            Export print-ready presentation sheets with section views, title blocks, and color swatches.
          </p>
        </div>
      </div>
    </div>
  );
}
