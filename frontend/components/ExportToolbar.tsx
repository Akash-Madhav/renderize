import { Download, FileText, Image as ImageIcon, RotateCcw } from "lucide-react";

interface ExportToolbarProps {
  projectId: string;
  pdfUrl?: string;
  pngUrl?: string;
  onRerender?: () => void;
}

export default function ExportToolbar({ projectId, pdfUrl, pngUrl, onRerender }: ExportToolbarProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-900/80 border border-slate-800 backdrop-blur-md">
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider font-mono">
          Final Deliverables
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        {pdfUrl && (
          <a
            href={pdfUrl}
            download
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs shadow-md shadow-amber-900/20 transition-all active:scale-95"
          >
            <FileText className="w-4 h-4" />
            <span>Download Presentation PDF (A1)</span>
          </a>
        )}

        {pngUrl && (
          <a
            href={pngUrl}
            download
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs border border-slate-700 transition-colors"
          >
            <ImageIcon className="w-4 h-4" />
            <span>Download 4K+ PNG</span>
          </a>
        )}

        {onRerender && (
          <button
            onClick={onRerender}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white font-medium text-xs border border-slate-800 transition-colors"
            title="Re-render plan with current settings"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Re-render</span>
          </button>
        )}
      </div>
    </div>
  );
}
