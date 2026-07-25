import React, { useEffect, useRef } from "react";
import { CheckCircle2, Circle, Loader2, Terminal, Sparkles, ArrowRight, ShieldCheck } from "lucide-react";

interface PipelineModalProps {
  isOpen: boolean;
  projectTitle: string;
  progress: number;
  phase: string;
  logs: string[];
  onComplete: () => void;
}

const STAGES = [
  { id: "RESEARCH", name: "Researcher Agent", subtitle: "DealFlow & Market Research" },
  { id: "CREATION", name: "Creator Agent", subtitle: "Tokenomics & Solidity Contract" },
  { id: "EXECUTION", name: "Executor Agent", subtitle: "OKX X Layer Deployment" },
  { id: "ANALYSIS", name: "Analyzer Agent", subtitle: "ASP Metrics & Readiness Scoring" },
];

export const PipelineModal: React.FC<PipelineModalProps> = ({
  isOpen,
  projectTitle,
  progress,
  phase,
  logs,
  onComplete,
}) => {
  const terminalEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  if (!isOpen) return null;

  const isFinished = progress >= 1.0 || phase === "COMPLETE";

  // Determine current stage index based on progress
  const currentStageIndex = isFinished
    ? 4
    : progress >= 0.75
    ? 3
    : progress >= 0.5
    ? 2
    : progress >= 0.25
    ? 1
    : 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-in fade-in duration-200">
      <div className="bg-card border border-border rounded-xl max-w-3xl w-full p-6 shadow-2xl space-y-6 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-border pb-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/30 text-primary">
              <Sparkles className="h-5 w-5 animate-pulse" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-foreground flex items-center gap-2">
                Multi-Agent Pipeline Executing
              </h2>
              <p className="text-sm text-muted-foreground">
                Target Project: <span className="font-semibold text-foreground">{projectTitle}</span>
              </p>
            </div>
          </div>
          <div className="text-right">
            <span className="text-2xl font-bold text-primary">{Math.round(progress * 100)}%</span>
            <p className="text-xs text-muted-foreground">Progress</p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-secondary/50 rounded-full h-2.5 overflow-hidden border border-border">
          <div
            className="bg-gradient-to-r from-primary via-emerald-400 to-cyan-400 h-full transition-all duration-500 ease-out"
            style={{ width: `${Math.max(5, progress * 100)}%` }}
          />
        </div>

        {/* 4 Agent Pipeline Stage Tracker */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {STAGES.map((stage, idx) => {
            const isDone = idx < currentStageIndex || isFinished;
            const isCurrent = idx === currentStageIndex && !isFinished;

            return (
              <div
                key={stage.id}
                className={`p-3 rounded-lg border text-left transition-all ${
                  isDone
                    ? "bg-emerald-950/20 border-emerald-500/30 text-emerald-400"
                    : isCurrent
                    ? "bg-primary/10 border-primary text-primary ring-1 ring-primary/40"
                    : "bg-secondary/20 border-border text-muted-foreground opacity-60"
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-semibold uppercase tracking-wider">
                    Phase {idx + 1}
                  </span>
                  {isDone ? (
                    <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  ) : isCurrent ? (
                    <Loader2 className="h-4 w-4 animate-spin text-primary" />
                  ) : (
                    <Circle className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <h4 className="text-xs font-bold text-foreground truncate">{stage.name}</h4>
                <p className="text-[10px] text-muted-foreground truncate">{stage.subtitle}</p>
              </div>
            );
          })}
        </div>

        {/* Terminal Log Output */}
        <div className="bg-black/90 rounded-lg p-4 font-mono text-xs text-green-400 border border-green-500/20 h-56 overflow-y-auto space-y-1.5 shadow-inner">
          <div className="flex items-center gap-2 border-b border-green-900/40 pb-2 text-green-500 font-semibold mb-2">
            <Terminal className="h-4 w-4" />
            <span>OKX ASP Agent Execution Log Stream</span>
          </div>

          {logs.length === 0 ? (
            <p className="text-muted-foreground italic text-center py-8">
              Initializing agent environment...
            </p>
          ) : (
            logs.map((log, index) => (
              <div key={index} className="leading-relaxed flex gap-2">
                <span className="text-green-600 select-none">&gt;</span>
                <span className={log.includes("ERROR") ? "text-red-400" : log.includes("Complete") ? "text-emerald-300 font-semibold" : "text-green-300"}>
                  {log}
                </span>
              </div>
            ))
          )}
          <div ref={terminalEndRef} />
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-2 border-t border-border">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <ShieldCheck className="h-4 w-4 text-primary" />
            <span>Simulated OKX X Layer Testnet Mode (Zero Gas Required)</span>
          </div>

          <button
            onClick={onComplete}
            disabled={!isFinished}
            className={`px-6 py-2.5 rounded-lg text-sm font-semibold flex items-center gap-2 transition-all shadow-lg ${
              isFinished
                ? "bg-primary text-primary-foreground hover:brightness-110 cursor-pointer animate-bounce"
                : "bg-secondary text-muted-foreground opacity-50 cursor-not-allowed"
            }`}
          >
            {isFinished ? "View Project Launch Package" : "Agents Working..."}
            {isFinished ? <ArrowRight className="h-4 w-4" /> : <Loader2 className="h-4 w-4 animate-spin" />}
          </button>
        </div>
      </div>
    </div>
  );
};
