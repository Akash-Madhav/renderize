"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ProcessingStepper from "@/components/ProcessingStepper";
import { ArrowLeft, Clock, ShieldAlert } from "lucide-react";
import Link from "next/link";

interface StatusResponse {
  project_id: string;
  status: string;
  current_stage: string;
  progress_pct: number;
  logs: string[];
  error_message?: string;
}

export default function ProcessingPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params?.id as string;

  const [statusData, setStatusData] = useState<StatusResponse>({
    project_id: projectId,
    status: "QUEUED",
    current_stage: "Stage 1/10: Initializing Ingestion",
    progress_pct: 10,
    logs: ["Connecting to rendering coordinator..."]
  });

  useEffect(() => {
    if (!projectId) return;

    const checkStatus = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/projects/${projectId}/status`);
        if (res.ok) {
          const data: StatusResponse = await res.json();
          setStatusData(data);

          if (data.status === "COMPLETED") {
            // Processing finished, push to result workspace
            setTimeout(() => {
              router.push(`/render/${projectId}`);
            }, 1200);
          }
        }
      } catch (err) {
        console.error("Status polling error", err);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 1500);
    return () => clearInterval(interval);
  }, [projectId, router]);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Dashboard</span>
        </Link>
        <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
          <Clock className="w-3.5 h-3.5 text-amber-400" />
          <span>Project ID: {projectId}</span>
        </div>
      </div>

      <div>
        <h1 className="text-2xl font-bold text-white font-serif">
          Processing Architectural Floor Plan
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Our AI pipeline is parsing CAD vectors, classifying spatial zones, and rendering presentation layers.
        </p>
      </div>

      {statusData.status === "FAILED" && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-rose-400">Rendering Pipeline Encountered An Error</h4>
            <p className="text-xs text-rose-300/80 mt-1">{statusData.error_message || "An unexpected error occurred during rendering."}</p>
          </div>
        </div>
      )}

      {/* Real-time Stepper & Terminal Component */}
      <ProcessingStepper
        currentStage={statusData.current_stage}
        progressPct={statusData.progress_pct}
        status={statusData.status}
        logs={statusData.logs}
      />
    </div>
  );
}
