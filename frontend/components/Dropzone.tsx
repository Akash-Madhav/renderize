"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { UploadCloud, FileText, Check, AlertCircle, Sparkles, Plus, Trash2, Zap } from "lucide-react";

export default function Dropzone() {
  const router = useRouter();
  const [files, setFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoadingDemo, setIsLoadingDemo] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getFloorBadge = (name: string) => {
    const upper = name.toUpperCase();
    if (upper.includes("PLINTH") || upper.includes("GROUND") || upper.includes("PL PLAN") || upper.includes(" PL ")) {
      return { label: "Ground Floor (Plinth)", color: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" };
    }
    if (upper.includes("FIRST") || upper.includes("1ST") || upper.includes("FL PLAN") || upper.includes(" FL ")) {
      return { label: "First Floor", color: "bg-amber-500/20 text-amber-300 border-amber-500/30" };
    }
    if (upper.includes("SECOND") || upper.includes("2ND") || upper.includes("SL PLAN") || upper.includes(" SL ")) {
      return { label: "Second Floor", color: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30" };
    }
    if (upper.includes("ROOF") || upper.includes("TERRACE")) {
      return { label: "Roof Plan", color: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30" };
    }
    return { label: "Architectural Plan", color: "bg-slate-700/40 text-slate-300 border-slate-600/40" };
  };

  const handleFiles = (incoming: FileList | File[]) => {
    const valid: File[] = [];
    for (let i = 0; i < incoming.length; i++) {
      const f = incoming[i];
      if (f.name.toLowerCase().endsWith(".pdf")) {
        valid.push(f);
      }
    }
    if (valid.length === 0) {
      setError("Please upload architectural drawing files in PDF format.");
      return;
    }
    setError(null);
    setFiles((prev) => [...prev, ...valid]);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const removeFile = (idx: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    files.forEach((f) => {
      formData.append("files", f);
    });

    try {
      const response = await fetch("http://127.0.0.1:8000/api/projects", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed with status: ${response.statusText}`);
      }

      const project = await response.json();
      router.push(`/render/${project.project_id}/processing`);
    } catch (err: any) {
      setError(err.message || "Failed to initiate rendering pipeline.");
      setIsUploading(false);
    }
  };

  const handleLoadDemo = async () => {
    setIsLoadingDemo(true);
    setError(null);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/projects/demo-multi-floor", {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error(`Demo failed to initialize: ${response.statusText}`);
      }
      const project = await response.json();
      router.push(`/render/${project.project_id}/processing`);
    } catch (err: any) {
      setError(err.message || "Failed to load demonstration project.");
      setIsLoadingDemo(false);
    }
  };

  return (
    <div className="w-full space-y-4">
      {/* Drag & Drop Area */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center transition-all ${
          isDragging
            ? "border-amber-400 bg-amber-500/10 scale-[1.01]"
            : files.length > 0
            ? "border-emerald-500/50 bg-emerald-500/5"
            : "border-slate-800 hover:border-slate-700 bg-slate-900/40 hover:bg-slate-900/60"
        }`}
      >
        <input
          type="file"
          accept=".pdf"
          id="pdf-upload"
          multiple
          className="hidden"
          onChange={(e) => e.target.files && handleFiles(e.target.files)}
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-amber-400 shadow-xl">
            {files.length > 0 ? <FileText className="w-8 h-8 text-emerald-400" /> : <UploadCloud className="w-8 h-8" />}
          </div>

          <div>
            <h3 className="text-lg font-bold text-white mb-1">
              {files.length > 0
                ? `${files.length} Floor Plan Drawing${files.length > 1 ? "s" : ""} Staged`
                : "Drop your architectural floor plan PDFs here"}
            </h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto leading-relaxed">
              Supports multi-floor sets (Ground, First, Second floors). Automatically assembles into a publication-grade A1 Presentation Sheet (DIRECTOR SHEET 1).
            </p>
          </div>

          <label
            htmlFor="pdf-upload"
            className="cursor-pointer inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs transition-colors border border-slate-700 shadow-md"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>{files.length > 0 ? "Add more floor plans" : "Browse files (Multiple PDFs supported)"}</span>
          </label>
        </div>
      </div>

      {/* Staged Files List */}
      {files.length > 0 && (
        <div className="rounded-xl border border-slate-800 bg-[#0F141C] p-4 space-y-2">
          <div className="text-xs font-semibold text-slate-300 font-mono flex items-center justify-between">
            <span>Staged Floor Plans ({files.length}):</span>
            <span className="text-[11px] text-amber-400">All floors will be rendered and assembled</span>
          </div>
          <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
            {files.map((f, i) => {
              const badge = getFloorBadge(f.name);
              return (
                <div
                  key={i}
                  className="flex items-center justify-between px-3 py-2 rounded-lg bg-slate-900/80 border border-slate-800 text-xs"
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <FileText className="w-4 h-4 text-slate-400 shrink-0" />
                    <span className="truncate text-slate-200 font-medium">{f.name}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border ${badge.color}`}>
                      {badge.label}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-[11px] text-slate-500 font-mono">
                      {(f.size / (1024 * 1024)).toFixed(2)} MB
                    </span>
                    <button
                      onClick={() => removeFile(i)}
                      className="text-slate-500 hover:text-rose-400 p-1"
                      title="Remove file"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {error && (
        <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center gap-3">
        {files.length > 0 && (
          <button
            onClick={handleUpload}
            disabled={isUploading}
            className="flex-1 w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm shadow-xl shadow-amber-900/30 flex items-center justify-center gap-2 transition-all active:scale-95 disabled:opacity-50"
          >
            <Sparkles className="w-4 h-4" />
            <span>{isUploading ? "Analyzing & Rendering Floors..." : `Render All ${files.length} Floor Plans & Compose Sheet`}</span>
          </button>
        )}

        <button
          onClick={handleLoadDemo}
          disabled={isLoadingDemo || isUploading}
          className="w-full sm:w-auto py-3.5 px-5 rounded-xl bg-slate-800/90 hover:bg-slate-700/90 text-amber-300 font-semibold text-xs border border-amber-500/30 hover:border-amber-500/60 flex items-center justify-center gap-2 transition-all shadow-lg shadow-black/40 disabled:opacity-50"
        >
          <Zap className="w-4 h-4 text-amber-400 fill-amber-400" />
          <span>{isLoadingDemo ? "Spinning up 3-Floor Demo..." : "⚡ 1-Click Demo: Director Residence (3 Floors → Master Sheet 1)"}</span>
        </button>
      </div>
    </div>
  );
}
