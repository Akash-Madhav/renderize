import { CheckCircle2, AlertCircle, RefreshCw, Layers } from "lucide-react";

interface ProcessingStepperProps {
  currentStage: string;
  progressPct: number;
  status: string;
  logs: string[];
}

const STAGES = [
  { id: 1, name: "Document Ingestion", key: "EXTRACTING_PDF" },
  { id: 2, name: "Vector Extraction", key: "EXTRACTING_PDF" },
  { id: 3, name: "Geometric Analysis", key: "ANALYZING_GEOMETRY" },
  { id: 4, name: "Gemma 2B Spatial AI", key: "SEMANTIC_REASONING" },
  { id: 5, name: "Material Synthesis", key: "RENDERING_MATERIALS" },
  { id: 6, name: "Architectural QA Audit", key: "VALIDATING_OUTPUT" },
  { id: 7, name: "Iterative Correction", key: "APPLYING_CORRECTIONS" },
  { id: 8, name: "Presentation Board Layout", key: "COMPOSING_SHEET" },
  { id: 9, name: "Certification & Export", key: "COMPLETED" },
];

export default function ProcessingStepper({
  currentStage,
  progressPct,
  status,
  logs
}: ProcessingStepperProps) {
  const isFailed = status === "FAILED";
  const isDone = status === "COMPLETED";

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 backdrop-blur-sm shadow-xl space-y-6">
      {/* Header and Progress Bar */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-semibold text-white">Pipeline Execution Telemetry</h3>
          </div>
          <span className="text-sm font-mono font-bold text-amber-400">{progressPct}%</span>
        </div>

        <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
          <div
            className={`h-full transition-all duration-500 rounded-full ${
              isFailed
                ? "bg-rose-500"
                : isDone
                ? "bg-emerald-500"
                : "bg-gradient-to-r from-amber-500 to-amber-400 animate-pulse"
            }`}
            style={{ width: `${Math.max(5, progressPct)}%` }}
          />
        </div>
        <p className="mt-2 text-xs font-mono text-slate-400 truncate">
          Active: <span className="text-slate-200">{currentStage}</span>
        </p>
      </div>

      {/* Stepper Grid */}
      <div className="grid grid-cols-3 md:grid-cols-9 gap-2">
        {STAGES.map((s, idx) => {
          const stepPercent = ((idx + 1) / STAGES.length) * 100;
          const isComplete = progressPct >= stepPercent || isDone;
          const isCurrent = !isComplete && progressPct >= (idx / STAGES.length) * 100 && !isFailed;

          return (
            <div
              key={s.id}
              className={`p-2.5 rounded-lg border text-center transition-all ${
                isComplete
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                  : isCurrent
                  ? "bg-amber-500/10 border-amber-500/50 text-amber-300 ring-1 ring-amber-500/40"
                  : "bg-slate-950/40 border-slate-800/80 text-slate-500"
              }`}
            >
              <div className="text-[10px] font-mono font-bold mb-1">ST {s.id}</div>
              <div className="text-[11px] font-medium leading-tight truncate">{s.name}</div>
            </div>
          );
        })}
      </div>

      {/* Real-time Streaming Logs Terminal */}
      <div className="rounded-lg bg-slate-950 border border-slate-800/80 p-4 font-mono text-xs text-slate-300 space-y-1 max-h-48 overflow-y-auto shadow-inner">
        <div className="text-slate-500 border-b border-slate-900 pb-1 mb-2 flex items-center justify-between">
          <span>PIPELINE ENGINE REALTIME TRACE</span>
          <span className="flex items-center gap-1 text-[10px] text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" /> ONLINE
          </span>
        </div>
        {logs.length === 0 ? (
          <div className="text-slate-600 italic">Waiting for processing events...</div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className="leading-relaxed hover:bg-slate-900/50 px-1 rounded">
              {log}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
