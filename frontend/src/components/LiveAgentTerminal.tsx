import React, { useEffect, useState, useRef } from "react";
import { Terminal, X, CheckCircle, AlertTriangle, Play, Pause, Loader } from "lucide-react";

interface LiveAgentTerminalProps {
  taskId: string | null;
  onClose?: () => void;
}

export function LiveAgentTerminal({ taskId, onClose }: LiveAgentTerminalProps) {
  const [logs, setLogs] = useState<string[]>([]);
  const [status, setStatus] = useState<string>("queued");
  const [progress, setProgress] = useState<number>(0);
  const [isAutoScroll, setIsAutoScroll] = useState<boolean>(true);
  const terminalEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!taskId) return;

    const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000/api";
    const eventSource = new EventSource(`${apiUrl}/crew/${taskId}/stream`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.log) {
          setLogs((prev) => [...prev, data.log]);
        }
        if (data.status) {
          setStatus(data.status);
        }
        if (data.progress !== undefined) {
          setProgress(data.progress);
        }
        if (data.status === "completed" || data.status === "error" || data.status === "cancelled") {
          eventSource.close();
        }
      } catch (err) {
        console.error("Error parsing SSE data", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE connection error", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [taskId]);

  useEffect(() => {
    if (isAutoScroll && terminalEndRef.current) {
      terminalEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs, isAutoScroll]);

  if (!taskId) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 w-full max-w-2xl rounded-xl border border-border bg-black/95 shadow-2xl overflow-hidden backdrop-blur-lg flex flex-col max-h-[450px]">
      {/* Terminal Header */}
      <div className="px-4 py-3 border-b border-border bg-card/90 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-mono text-primary font-bold">
            <Terminal className="h-4 w-4" />
            <span>AGENT TERMINAL // {taskId.slice(0, 8)}</span>
          </div>
          <span
            className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded font-bold ${
              status === "completed"
                ? "bg-green-500/20 text-green-400"
                : status === "running"
                ? "bg-primary/20 text-primary"
                : "bg-muted text-muted-foreground"
            }`}
          >
            {status}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsAutoScroll(!isAutoScroll)}
            className="p-1 rounded text-xs text-muted-foreground hover:text-foreground transition"
            title="Toggle Auto Scroll"
          >
            {isAutoScroll ? <Pause className="h-3.5 w-3.5" /> : <Play className="h-3.5 w-3.5" />}
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="p-1 rounded text-muted-foreground hover:text-foreground hover:bg-secondary transition"
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="h-1 bg-secondary w-full overflow-hidden">
        <div
          className="h-full bg-primary transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Terminal Body */}
      <div className="p-4 text-xs font-mono text-green-400 space-y-1.5 overflow-y-auto flex-1 leading-relaxed">
        {logs.length === 0 ? (
          <div className="flex items-center gap-2 text-muted-foreground py-4">
            <Loader className="h-3.5 w-3.5 animate-spin text-primary" />
            <span>Initializing CrewAI agent stream...</span>
          </div>
        ) : (
          logs.map((log, idx) => (
            <div key={idx} className="break-words">
              <span className="text-muted-foreground font-semibold mr-2">&gt;</span>
              <span className={log.includes("ERROR") ? "text-red-400 font-bold" : log.includes("✅") ? "text-green-300 font-semibold" : "text-gray-300"}>
                {log}
              </span>
            </div>
          ))
        )}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
}
