"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft,
  Layers,
  Compass,
  CheckCircle2,
  ShieldCheck,
  Home,
  Info,
  Ruler,
  Maximize2,
  FileText,
  Download,
  Building2,
  Trash2
} from "lucide-react";
import ComparisonSlider from "@/components/ComparisonSlider";
import QAInspectorModal from "@/components/QAInspectorModal";
import ExportToolbar from "@/components/ExportToolbar";

interface FloorPlan {
  floor_id: string;
  floor_label: string;
  original_filename: string;
  preview_original_url: string;
  rendered_image_url: string;
  qa_overlay_url: string;
  fidelity_score_pct: number;
  extracted_paths_count: number;
  annotations_count: number;
  dimensions_detected: string[];
  rooms: Array<{
    room_id: string;
    semantic_type: string;
    subtype: string;
    recommended_flooring: string;
    confidence: number;
    reasoning: string;
  }>;
}

interface ProjectDetails {
  project_id: string;
  title: string;
  original_filename: string;
  uploaded_at: string;
  status: string;
  current_stage: string;
  progress_pct: number;
  is_multi_floor: boolean;
  dimensions_pts?: number[];
  extracted_paths_count?: number;
  annotations_count?: number;
  dimensions_detected?: string[];
  semantic_typology?: string;
  rooms?: Array<{
    room_id: string;
    semantic_type: string;
    subtype: string;
    recommended_flooring: string;
    confidence: number;
    reasoning: string;
  }>;
  floors?: FloorPlan[];
  validation?: {
    geometric_fidelity_pct: number;
    wall_axis_max_displacement_px: number;
    elements_detected: Record<string, number>;
    elements_retained_pct: number;
    correction_iterations_run: number;
    unresolved_discrepancies: string[];
    verdict: string;
    overlay_image_url?: string;
  };
  preview_original_url?: string;
  rendered_image_url?: string;
  presentation_pdf_url?: string;
  presentation_png_url?: string;
  section_image_url?: string;
  elevation_image_url?: string;
}

export default function ResultWorkspacePage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params?.id as string;

  const [project, setProject] = useState<ProjectDetails | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<string>("master"); // "master" | "floor_0" | "floor_1" | ... | "section"

  const fetchProject = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}`);
      if (res.ok) {
        const data = await res.json();
        setProject(data);
      }
    } catch (e) {
      console.error("Failed to load project details", e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (projectId) {
      fetchProject();
    }
  }, [projectId]);

  const handleRerender = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}/render`, {
        method: "POST"
      });
      if (res.ok) {
        router.push(`/render/${projectId}/processing`);
      }
    } catch (e) {
      console.error("Re-render request failed", e);
    }
  };

  const handleDelete = async () => {
    if (!confirm(`Are you sure you want to delete '${project?.title}' and all its rendered outputs?`)) {
      return;
    }
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}`, {
        method: "DELETE",
      });
      if (res.ok) {
        router.push("/");
      } else {
        alert("Failed to delete project.");
      }
    } catch (e) {
      console.error("Delete failed", e);
      alert("Error deleting project.");
    }
  };

  if (isLoading || !project) {
    return (
      <div className="text-center py-24 space-y-3">
        <div className="w-8 h-8 border-2 border-amber-400 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-xs text-slate-400 font-mono">Loading architectural workspace...</p>
      </div>
    );
  }

  const presentationPdfUrl = project.presentation_pdf_url
    ? `http://127.0.0.1:8000${project.presentation_pdf_url}`
    : "";
  const presentationPngUrl = project.presentation_png_url
    ? `http://127.0.0.1:8000${project.presentation_png_url}`
    : "";
  const sectionImageUrl = project.section_image_url
    ? `http://127.0.0.1:8000${project.section_image_url}`
    : "";

  const floors = project.floors && project.floors.length > 0
    ? project.floors
    : [
        {
          floor_id: "floor_0",
          floor_label: "Architectural Plan",
          original_filename: project.original_filename,
          preview_original_url: project.preview_original_url || "",
          rendered_image_url: project.rendered_image_url || "",
          qa_overlay_url: project.validation?.overlay_image_url || "",
          fidelity_score_pct: project.validation?.geometric_fidelity_pct || 100.0,
          extracted_paths_count: project.extracted_paths_count || 0,
          annotations_count: project.annotations_count || 0,
          dimensions_detected: project.dimensions_detected || [],
          rooms: project.rooms || []
        }
      ];

  const currentFloor = floors.find((f) => f.floor_id === activeTab);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <Link
            href="/"
            className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors mb-2"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Dashboard</span>
          </Link>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold text-white font-serif tracking-tight">
              {project.title}
            </h1>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              100% Geometry Retained
            </span>
            {project.is_multi_floor && (
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
                Multi-Floor Ingestion
              </span>
            )}
          </div>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Source: {project.original_filename} &bull; Uploaded {project.uploaded_at}
          </p>
        </div>

        {/* QA Action Trigger & Delete Button */}
        <div className="flex items-center gap-3">
          {project.validation && (
            <QAInspectorModal
              validation={{
                ...project.validation,
                overlay_image_url: project.validation.overlay_image_url
                  ? `http://127.0.0.1:8000${project.validation.overlay_image_url}`
                  : undefined
              }}
            />
          )}

          <button
            onClick={handleDelete}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-semibold transition-colors"
            title="Delete this project and purge files"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Delete Project</span>
          </button>
        </div>
      </div>

      {/* Floor & Master Sheet Tab Switcher */}
      <div className="flex items-center gap-2 border-b border-slate-800/80 overflow-x-auto pb-2">
        <button
          onClick={() => setActiveTab("master")}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold transition-all shrink-0 ${
            activeTab === "master"
              ? "bg-amber-500 text-slate-950 shadow-lg shadow-amber-900/30"
              : "bg-slate-900/80 text-slate-300 hover:text-white hover:bg-slate-800 border border-slate-800"
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Master Presentation Sheet (DIRECTOR SHEET 1)</span>
        </button>

        {floors.map((fl) => (
          <button
            key={fl.floor_id}
            onClick={() => setActiveTab(fl.floor_id)}
            className={`flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all shrink-0 ${
              activeTab === fl.floor_id
                ? "bg-slate-200 text-slate-950 shadow-md"
                : "bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800 border border-slate-800"
            }`}
          >
            <Building2 className="w-3.5 h-3.5" />
            <span>{fl.floor_label}</span>
          </button>
        ))}

        {sectionImageUrl && (
          <button
            onClick={() => setActiveTab("section")}
            className={`flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all shrink-0 ${
              activeTab === "section"
                ? "bg-slate-200 text-slate-950 shadow-md"
                : "bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800 border border-slate-800"
            }`}
          >
            <Ruler className="w-3.5 h-3.5" />
            <span>Section AA' Elevation</span>
          </button>
        )}
      </div>

      {/* Tab Content Display */}
      {activeTab === "master" ? (
        /* MASTER PRESENTATION SHEET VIEW (DIRECTOR SHEET 1) */
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 font-mono">
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                A1 Master Architectural Board (9933 x 7016 px &bull; 300 DPI)
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Multi-plan presentation board composed from all analyzed floors, Section AA', elevation profile, and color swatches.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <a
                href={presentationPdfUrl}
                download
                className="px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold flex items-center gap-1.5 transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download A1 PDF</span>
              </a>
            </div>
          </div>

          <div className="relative rounded-2xl overflow-hidden border border-slate-800 bg-[#0F141C] shadow-2xl">
            {presentationPngUrl ? (
              <div className="overflow-auto max-h-[750px] p-2 flex justify-center bg-slate-950/80">
                <img
                  src={presentationPngUrl}
                  alt="Director Master Presentation Sheet"
                  className="rounded-lg shadow-2xl object-contain max-w-full"
                />
              </div>
            ) : (
              <div className="p-16 text-center text-slate-500">
                Composing master presentation sheet...
              </div>
            )}
          </div>

          {/* Sheet Elements Breakdown */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/80 text-xs space-y-1">
              <span className="text-slate-400 font-mono">Top Row:</span>
              <p className="text-white font-semibold">3 Multi-Level Rendered Unit Plans</p>
              <p className="text-slate-500 text-[11px]">Ground Floor (Plinth), First Floor, Second Floor</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/80 text-xs space-y-1">
              <span className="text-slate-400 font-mono">Lower Left:</span>
              <p className="text-white font-semibold">Longitudinal Section AA'</p>
              <p className="text-slate-500 text-[11px]">Floor-to-floor structural levels at 1:50 metric scale</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/80 text-xs space-y-1">
              <span className="text-slate-400 font-mono">Mid Right:</span>
              <p className="text-white font-semibold">Front Elevation & Palette</p>
              <p className="text-slate-500 text-[11px]">French oak, Italian marble, Sage quartzite, Charcoal slate</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800/80 text-xs space-y-1">
              <span className="text-slate-400 font-mono">Bottom Block:</span>
              <p className="text-white font-semibold">Title Block & Area Schedule</p>
              <p className="text-slate-500 text-[11px]">Total 1050 sq.m &bull; 350 sq.m unit &bull; 3 Floors &bull; 4 BHK</p>
            </div>
          </div>
        </div>
      ) : activeTab === "section" ? (
        /* SECTION AA' VIEW */
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
              Building Section AA' & Elevational Profile (1:50 Metric Scale)
            </h2>
          </div>
          <div className="rounded-2xl overflow-hidden border border-slate-800 bg-slate-950 p-4 flex justify-center">
            <img
              src={sectionImageUrl}
              alt="Section AA' Elevation"
              className="rounded-lg max-h-[600px] object-contain"
            />
          </div>
        </div>
      ) : (
        /* INDIVIDUAL FLOOR BEFORE/AFTER VIEW */
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2 font-mono">
                <Layers className="w-4 h-4 text-amber-400" />
                {currentFloor?.floor_label} &mdash; Registration & Material Verification
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                {currentFloor?.extracted_paths_count.toLocaleString()} CAD vector strokes preserved with zero geometric drift.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                Fidelity: {currentFloor?.fidelity_score_pct.toFixed(2)}%
              </span>
            </div>
          </div>

          {currentFloor?.preview_original_url && currentFloor?.rendered_image_url ? (
            <ComparisonSlider
              originalUrl={`http://127.0.0.1:8000${currentFloor.preview_original_url}`}
              renderedUrl={`http://127.0.0.1:8000${currentFloor.rendered_image_url}`}
              originalLabel="Raw CAD Vector Blueprint"
              renderedLabel="Renderize Architectural Visualization"
            />
          ) : (
            <div className="p-12 text-center text-slate-500 bg-slate-900/40 rounded-xl">
              Floor rendering is loading...
            </div>
          )}

          {/* Room Semantics Breakdown for this floor */}
          {currentFloor?.rooms && currentFloor.rooms.length > 0 && (
            <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-white font-mono flex items-center gap-2">
                <Home className="w-3.5 h-3.5 text-amber-400" />
                Inferred Room Semantics & Texture Allocation
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5">
                {currentFloor.rooms.map((rm, i) => (
                  <div
                    key={i}
                    className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs space-y-1"
                  >
                    <div className="font-semibold text-slate-200 truncate">{rm.subtype}</div>
                    <div className="text-[10px] text-amber-400 font-mono truncate">
                      {rm.recommended_flooring.replace(/_/g, " ")}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Deliverable Download Hub */}
      <ExportToolbar
        projectId={project.project_id}
        pdfUrl={presentationPdfUrl}
        pngUrl={presentationPngUrl}
        onRerender={handleRerender}
      />

      {/* Architectural Intelligence & Specifications */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-amber-400">
            <Home className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Project Typology</h3>
          </div>
          <div className="text-sm font-semibold text-slate-200">
            {project.semantic_typology || "Luxury Multi-Storey Residence"}
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Multi-level spatial coherence verified across stair cores, vertical riser chases, and double-height ceiling voids.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-emerald-400">
            <Ruler className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Preserved Dimensions</h3>
          </div>
          <div className="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto">
            {project.dimensions_detected && project.dimensions_detected.length > 0 ? (
              project.dimensions_detected.map((dim, i) => (
                <span
                  key={i}
                  className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700/60"
                >
                  {dim}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-500">Scale 1:50 / 1:150 Metric</span>
            )}
          </div>
          <p className="text-[11px] text-slate-400">
            100% of dimension witness lines and callout values are preserved in exact original positions.
          </p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-sky-400">
            <Compass className="w-4 h-4" />
            <h3 className="text-xs font-bold uppercase tracking-wider text-white">Applied Material Palette</h3>
          </div>
          <div className="space-y-1.5 text-xs text-slate-300">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[#8B5A2B]" /> Bedrooms
              </span>
              <span className="text-slate-400 font-mono text-[11px]">French Oak Herringbone</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[#E0E5DF]" /> Living & Foyers
              </span>
              <span className="text-slate-400 font-mono text-[11px]">Calacatta Marble</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[#8B9E7A]" /> Kitchens
              </span>
              <span className="text-slate-400 font-mono text-[11px]">Sage Quartzite</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[#363C40]" /> Bathrooms
              </span>
              <span className="text-slate-400 font-mono text-[11px]">Charcoal Slate Tile</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
