"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  Layers,
  ShieldCheck,
  ArrowRight,
  Clock,
  Trash2,
  AlertTriangle
} from "lucide-react";
import Dropzone from "@/components/Dropzone";

interface Project {
  project_id: string;
  title: string;
  original_filename: string;
  uploaded_at: string;
  status: string;
  current_stage: string;
  progress_pct: number;
  is_multi_floor?: boolean;
  rendered_image_url?: string;
  validation?: {
    geometric_fidelity_pct: number;
    verdict: string;
  };
}

export default function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeleting, setIsDeleting] = useState(false);

  const fetchProjects = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/projects");
      if (res.ok) {
        const data = await res.json();
        setProjects(data);
      }
    } catch (e) {
      console.error("Backend not reachable yet", e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
    const interval = setInterval(fetchProjects, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleDeleteProject = async (projectId: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (!confirm(`Are you sure you want to delete project '${projectId}' and its generated files?`)) {
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setProjects((prev) => prev.filter((p) => p.project_id !== projectId));
      } else {
        alert("Failed to delete project.");
      }
    } catch (err) {
      console.error("Delete failed", err);
      alert("Error deleting project.");
    }
  };

  const handleDeleteAll = async () => {
    if (!confirm("Are you sure you want to delete ALL projects and clear all generated presentation files? This cannot be undone.")) {
      return;
    }

    setIsDeleting(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/projects", {
        method: "DELETE",
      });
      if (res.ok) {
        setProjects([]);
      } else {
        alert("Failed to delete all projects.");
      }
    } catch (err) {
      console.error("Delete all failed", err);
      alert("Error deleting all projects.");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div className="space-y-12">
      {/* Hero Header */}
      <div className="relative rounded-3xl p-8 md:p-12 border border-slate-800 bg-gradient-to-b from-slate-900/80 via-[#0C1017] to-[#0A0D14] shadow-2xl overflow-hidden">
        <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 rounded-full bg-amber-500/10 blur-3xl pointer-events-none" />
        
        <div className="max-w-3xl space-y-4 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Architectural Visualization AI Engine</span>
          </div>

          <h1 className="text-3xl md:text-5xl font-bold tracking-tight text-white font-serif leading-tight">
            Turn Technical CAD Blueprints into Publication-Grade Presentation Plans.
          </h1>

          <p className="text-slate-400 text-sm md:text-base leading-relaxed">
            Renderize preserves 100% of your original floor plan geometry, walls, and dimensions while applying warm French oak parquet, Calacatta marble, Verde sage stone, and architectural lighting.
          </p>
        </div>

        {/* Quick Dropzone Widget */}
        <div className="mt-8 max-w-2xl">
          <Dropzone />
        </div>
      </div>

      {/* Recent Projects Section */}
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white font-serif">Recent Architectural Projects</h2>
            <p className="text-xs text-slate-400">Processed floor plans, presentation sheets, and QA validation reports</p>
          </div>
          <div className="flex items-center gap-3">
            {projects.length > 0 && (
              <button
                onClick={handleDeleteAll}
                disabled={isDeleting}
                className="text-xs font-semibold text-rose-400 hover:text-rose-300 px-3 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 flex items-center gap-1.5 transition-colors"
                title="Purge all project history and cache"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>{isDeleting ? "Deleting..." : "Clear All Projects"}</span>
              </button>
            )}
            <Link
              href="/render/new"
              className="text-xs font-semibold text-amber-400 hover:text-amber-300 flex items-center gap-1"
            >
              <span>Upload New PDF</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {projects.length === 0 ? (
          <div className="border border-slate-800 rounded-2xl p-12 text-center bg-slate-900/20 text-slate-500 space-y-3">
            <Layers className="w-10 h-10 mx-auto text-slate-700" />
            <p className="text-sm font-medium">No floor plans rendered yet.</p>
            <p className="text-xs text-slate-600">Upload your architectural CAD PDFs above or use the 1-Click Demo to see publication-grade results.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((proj) => (
              <div
                key={proj.project_id}
                className="group relative rounded-2xl border border-slate-800/80 bg-slate-900/40 hover:bg-slate-900/80 p-5 transition-all hover:border-slate-700 hover:shadow-xl flex flex-col justify-between"
              >
                <Link
                  href={proj.status === "COMPLETED" ? `/render/${proj.project_id}` : `/render/${proj.project_id}/processing`}
                  className="block space-y-3 flex-1"
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                      ID: {proj.project_id}
                    </span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider ${
                        proj.status === "COMPLETED"
                          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                          : proj.status === "FAILED"
                          ? "bg-rose-500/10 text-rose-400 border border-rose-500/30"
                          : "bg-amber-500/10 text-amber-400 border border-amber-500/30 animate-pulse"
                      }`}
                    >
                      {proj.status}
                    </span>
                  </div>

                  <h3 className="font-bold text-white text-base truncate group-hover:text-amber-400 transition-colors">
                    {proj.title}
                  </h3>
                  <p className="text-xs text-slate-500 truncate mt-0.5 font-mono">
                    {proj.original_filename}
                  </p>

                  <div className="mt-4 flex items-center gap-4 text-xs text-slate-400">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-500" />
                      {proj.uploaded_at}
                    </span>
                  </div>
                </Link>

                <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs">
                  {proj.validation ? (
                    <span className="flex items-center gap-1 text-emerald-400 font-semibold text-[11px]">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      {proj.validation.geometric_fidelity_pct.toFixed(1)}% Fidelity
                    </span>
                  ) : (
                    <span className="text-slate-500 text-[11px] truncate max-w-[180px]">{proj.current_stage}</span>
                  )}
                  
                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => handleDeleteProject(proj.project_id, e)}
                      className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                      title="Delete this project"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                    <Link
                      href={proj.status === "COMPLETED" ? `/render/${proj.project_id}` : `/render/${proj.project_id}/processing`}
                      className="text-amber-400 group-hover:translate-x-1 transition-transform p-1.5"
                    >
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
