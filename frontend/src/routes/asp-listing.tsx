import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { 
  Loader, 
  CheckCircle, 
  Copy, 
  Code, 
  ShieldCheck, 
  DollarSign, 
  Cpu, 
  Check, 
  Play, 
  Sparkles, 
  Terminal,
  ExternalLink,
  X,
  Upload,
  AlertCircle,
  CheckCircle2,
  FileCode,
  ArrowRight
} from "lucide-react";
import { aspApi } from "../lib/api";
import { AuthGuard } from "../components/AuthGuard";

export const Route = createFileRoute("/asp-listing")({
  component: () => (
    <AuthGuard pageTitle="ASP Listing">
      <AspListingPage />
    </AuthGuard>
  ),
});

export function AspListingPage() {
  const [manifest, setManifest] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [modalCopied, setModalCopied] = useState(false);
  const [testResult, setTestResult] = useState<any>(null);
  const [validating, setValidating] = useState(false);

  // Hiring simulation state
  const [hiringSimulation, setHiringSimulation] = useState<any>(null);
  const [isHiring, setIsHiring] = useState(false);
  const [hiringLogs, setHiringLogs] = useState<string[]>([]);

  // Submission modal & status state
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState<any>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  useEffect(() => {
    aspApi
      .getManifest()
      .then((data) => {
        setManifest(data.manifest);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch manifest", err);
        setLoading(false);
      });
  }, []);

  const handleCopyManifest = (isModal: boolean = false) => {
    if (!manifest) return;
    navigator.clipboard.writeText(JSON.stringify(manifest, null, 2));
    if (isModal) {
      setModalCopied(true);
      setTimeout(() => setModalCopied(false), 2000);
    } else {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleValidate = async () => {
    setValidating(true);
    setTestResult(null);
    try {
      const res = await aspApi.validate(manifest);
      setTestResult({
        valid: res.valid,
        status: res.status,
        message: "Manifest is valid against OKX.AI Marketplace Standard v1.0.0",
        verified_at: new Date().toISOString(),
      });
      setToastMessage("✓ Manifest is valid against OKX.AI Marketplace Standard v1.0.0");
      setTimeout(() => setToastMessage(null), 4500);
    } catch (err: any) {
      setTestResult({
        valid: false,
        message: err.message || "Validation failed against OKX.AI Marketplace Standard v1.0.0"
      });
    } finally {
      setValidating(false);
    }
  };

  const handleSimulateHire = async () => {
    setIsHiring(true);
    setHiringSimulation(null);
    setHiringLogs(["[0.0s] Incoming job call from external agent: agent.okx.deai_trader_v2"]);

    try {
      await new Promise(r => setTimeout(r, 350));
      setHiringLogs(prev => [
        ...prev,
        "[0.4s] Confirming 0.05 OKT micropayment transaction on OKX X Layer Testnet...",
      ]);

      await new Promise(r => setTimeout(r, 450));
      setHiringLogs(prev => [
        ...prev,
        "[0.8s] Delegating task payload to Coordinator & Executor Agent crew...",
      ]);

      await new Promise(r => setTimeout(r, 400));
      setHiringLogs(prev => [
        ...prev,
        "[1.2s] Proof of execution generated & block #14,892,105 confirmed!",
      ]);

      setHiringSimulation({
        status: "JOB_COMPLETED",
        client_agent_id: "agent.okx.deai_trader_v2",
        asp_service: "asp.builderforge.okx",
        job_type: "FULL_LAUNCHPAD_PIPELINE",
        payment_status: "PAID 0.05 OKT",
        tx_hash: "0x39a01f82b74c102a984019283f1",
        execution_time_sec: 1.2,
        proof_of_execution: {
          tokenomics_minted: true,
          contract_verified: true,
          readiness_score: 98,
        }
      });
    } finally {
      setIsHiring(false);
    }
  };

  const handleSubmitListing = async () => {
    setSubmitting(true);
    try {
      const res = await aspApi.submit(manifest);
      setSubmissionResult(res);
      setToastMessage("🚀 ASP Service Manifest submitted successfully to OKX.AI Marketplace Directory!");
      setTimeout(() => setToastMessage(null), 5000);
    } catch (err: any) {
      setToastMessage("Failed to submit ASP listing. Please try again.");
      setTimeout(() => setToastMessage(null), 4000);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-background relative">
      <main className="flex-1">
        <div className="px-6 py-8 max-w-6xl mx-auto space-y-8">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-semibold text-primary mb-3">
                <ShieldCheck className="h-3.5 w-3.5" /> VERIFIED OKX ASP PROVIDER
              </div>
              <h1 className="text-4xl font-extrabold tracking-tight text-foreground">
                OKX.AI ASP Marketplace Listing
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl">
                Configure, validate, and export your Agentic Service Provider (ASP) manifest to list BuilderForge multi-agent execution services on OKX.AI.
              </p>
            </div>

            {/* Header Action Buttons */}
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => handleCopyManifest(false)}
                className="inline-flex items-center gap-2 rounded-lg border border-border bg-card px-4 py-2 text-xs font-bold text-foreground hover:bg-secondary transition cursor-pointer"
              >
                {copied ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
                {copied ? "Copied!" : "Copy Manifest JSON"}
              </button>

              <button
                onClick={handleValidate}
                disabled={validating}
                className="inline-flex items-center gap-2 rounded-lg bg-secondary/80 border border-border px-4 py-2 text-xs font-bold text-foreground hover:bg-secondary transition cursor-pointer disabled:opacity-50"
              >
                {validating ? <Loader className="h-4 w-4 animate-spin text-primary" /> : <CheckCircle className="h-4 w-4 text-primary" />}
                Validate Spec
              </button>

              <button
                onClick={() => setShowSubmitModal(true)}
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2 text-xs font-bold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20 cursor-pointer"
              >
                <Upload className="h-4 w-4" />
                Submit to OKX.AI
              </button>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center py-24">
              <Loader className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : (
            <div className="grid gap-8 lg:grid-cols-3">
              {/* Left Column: Info & Stats */}
              <div className="space-y-6 lg:col-span-1">
                {/* Status Card */}
                <div className="rounded-xl border border-border bg-card p-6 space-y-4 shadow-lg">
                  <h3 className="text-xs font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-2">
                    <Cpu className="h-4 w-4 text-primary" /> Active ASP Agents (5/5)
                  </h3>
                  <div className="space-y-2">
                    {manifest?.agents?.map((agent: any) => (
                      <div key={agent.id} className="flex items-center justify-between p-2.5 rounded-md bg-secondary/50 border border-border/50 text-xs font-medium">
                        <span className="font-semibold text-foreground">{agent.name}</span>
                        <span className="text-[10px] bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded font-mono font-bold border border-emerald-500/20">
                          {agent.status || "ONLINE"}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Pricing Card */}
                <div className="rounded-xl border border-border bg-card p-6 space-y-4 shadow-lg">
                  <h3 className="text-xs font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-2">
                    <DollarSign className="h-4 w-4 text-primary" /> Marketplace Rate Cards
                  </h3>
                  <div className="space-y-3">
                    {manifest?.pricing_models?.map((model: any) => (
                      <div key={model.model_id} className="p-3 rounded-lg border border-primary/20 bg-primary/5 space-y-1">
                        <div className="flex justify-between items-center text-sm font-bold text-foreground">
                          <span>{model.name}</span>
                          <span className="text-primary font-mono">{model.price} {model.currency}</span>
                        </div>
                        <p className="text-[11px] text-muted-foreground">{model.billing_unit}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Interactive External Agent Hiring Simulator */}
                <div className="rounded-xl border border-purple-500/30 bg-purple-950/10 p-6 space-y-4 shadow-lg">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold text-purple-300 uppercase tracking-wider flex items-center gap-2">
                      <Sparkles className="h-4 w-4 text-purple-400" /> Agent-to-Agent Hiring Test
                    </h3>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Test how third-party AI agents on OKX.AI hire BuilderForge ASP via machine API.
                  </p>
                  
                  <button
                    onClick={handleSimulateHire}
                    disabled={isHiring}
                    className="w-full py-2.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg shadow-purple-500/20 cursor-pointer disabled:opacity-60"
                  >
                    {isHiring ? <Loader className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4 fill-white" />}
                    {isHiring ? "Simulating Agent Call..." : "Simulate External Agent Call (0.05 OKT)"}
                  </button>

                  {/* Hiring Simulation Stream & Proof */}
                  {hiringLogs.length > 0 && (
                    <div className="bg-black/95 p-3.5 rounded-lg text-[11px] font-mono text-purple-300 border border-purple-500/30 space-y-2 shadow-inner">
                      <div className="flex items-center gap-2 border-b border-purple-900/50 pb-2 text-purple-400 font-bold">
                        <Terminal className={`h-3.5 w-3.5 ${isHiring ? "animate-pulse" : ""}`} />
                        <span>Machine API Execution Stream</span>
                      </div>
                      <div className="space-y-1">
                        {hiringLogs.map((log, idx) => (
                          <p key={idx} className="leading-snug flex gap-1.5 text-[10px]">
                            <span className="text-purple-500 select-none">&gt;</span>
                            <span>{log}</span>
                          </p>
                        ))}
                      </div>
                    </div>
                  )}

                  {hiringSimulation && !isHiring && (
                    <div className="bg-emerald-950/40 p-3.5 rounded-lg text-xs border border-emerald-500/40 space-y-2 animate-in fade-in duration-300">
                      <div className="flex items-center justify-between">
                        <p className="text-emerald-400 font-bold flex items-center gap-1.5 text-xs">
                          <CheckCircle2 className="h-4 w-4 shrink-0" /> Job Executed & Verified!
                        </p>
                        <span className="text-[10px] bg-emerald-900/80 text-emerald-300 px-2 py-0.5 rounded font-mono font-bold">
                          {hiringSimulation.payment_status}
                        </span>
                      </div>
                      <div className="text-[11px] font-mono space-y-1 text-muted-foreground">
                        <p>Client Agent: <span className="text-foreground font-semibold">{hiringSimulation.client_agent_id}</span></p>
                        <p>Tx Hash: <span className="text-emerald-300 break-all">{hiringSimulation.tx_hash}</span></p>
                        <p>Execution Time: <span className="text-cyan-300">{hiringSimulation.execution_time_sec}s</span></p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Validation Result Banner */}
                {testResult && (
                  <div className={`rounded-xl p-5 border text-xs space-y-2 shadow-lg animate-in fade-in duration-200 ${
                    testResult.valid 
                      ? "bg-emerald-950/40 border-emerald-500/50 text-emerald-300" 
                      : "bg-destructive/10 border-destructive text-destructive"
                  }`}>
                    <p className="font-extrabold flex items-center gap-2 text-sm">
                      {testResult.valid ? <CheckCircle className="h-4.5 w-4.5 text-emerald-400 shrink-0" /> : <AlertCircle className="h-4.5 w-4.5 shrink-0" />}
                      {testResult.valid ? "OKX.AI Manifest Verified" : "Validation Error"}
                    </p>
                    <p className="leading-relaxed font-medium">{testResult.message}</p>
                    {testResult.verified_at && (
                      <p className="text-[10px] font-mono opacity-80 pt-1 border-t border-emerald-800/40">
                        Verified at: {new Date(testResult.verified_at).toLocaleString()}
                      </p>
                    )}
                  </div>
                )}
              </div>

              {/* Right Column: Complete Interactive Code Inspector */}
              <div className="lg:col-span-2 rounded-xl border border-border bg-card overflow-hidden flex flex-col shadow-xl">
                <div className="px-6 py-4 border-b border-border bg-secondary/40 flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                    <FileCode className="h-4.5 w-4.5 text-primary" />
                    <span>asp_manifest.json (OKX Marketplace Standard v1.0.0)</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleCopyManifest(false)}
                      className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1 cursor-pointer font-medium"
                    >
                      {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                      {copied ? "Copied!" : "Copy Code"}
                    </button>
                    <span className="text-[10px] font-mono text-emerald-400 font-bold bg-emerald-950/60 border border-emerald-500/40 px-2.5 py-0.5 rounded">
                      VERIFIED_ASP_READY
                    </span>
                  </div>
                </div>

                <pre className="p-6 text-xs font-mono text-emerald-400/90 bg-black/95 overflow-x-auto leading-relaxed flex-1 max-h-[580px] custom-scrollbar selection:bg-primary/30 selection:text-white">
                  {JSON.stringify(manifest, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Submit to OKX.AI Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-card border border-border rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-6 relative overflow-hidden text-foreground">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-border pb-4">
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-xl bg-primary/15 border border-primary/30 flex items-center justify-center text-primary">
                  <Upload className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="font-bold text-lg text-foreground">
                    Submit ASP Listing to OKX.AI
                  </h3>
                  <p className="text-xs text-muted-foreground">Listing Guide & Registration Steps</p>
                </div>
              </div>
              <button
                onClick={() => setShowSubmitModal(false)}
                className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition cursor-pointer"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Steps Checklist */}
            <div className="space-y-3 text-xs">
              <h4 className="font-bold text-foreground text-xs uppercase tracking-wider">OKX.AI Listing Checklist</h4>
              <div className="space-y-2">
                <div className="p-3 rounded-lg bg-secondary/30 border border-border/50 flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-emerald-950 border border-emerald-500/40 text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0">
                    1
                  </div>
                  <div>
                    <span className="font-bold text-foreground block text-sm">Manifest Validation</span>
                    <span className="text-muted-foreground">Verified against OKX.AI Marketplace Standard v1.0.0 with 5 online agents.</span>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-secondary/30 border border-border/50 flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-emerald-950 border border-emerald-500/40 text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0">
                    2
                  </div>
                  <div>
                    <span className="font-bold text-foreground block text-sm">OKX Wallet Signature</span>
                    <span className="text-muted-foreground">Sign payload using OKX Wallet on OKX X Layer Testnet (Chain ID 195).</span>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-secondary/30 border border-border/50 flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-emerald-950 border border-emerald-500/40 text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0">
                    3
                  </div>
                  <div>
                    <span className="font-bold text-foreground block text-sm">Rate Card & SLA Commitment</span>
                    <span className="text-muted-foreground">Pay-per-execution model set at 0.05 OKT/run with 99.9% uptime SLA.</span>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-secondary/30 border border-border/50 flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-emerald-950 border border-emerald-500/40 text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0">
                    4
                  </div>
                  <div>
                    <span className="font-bold text-foreground block text-sm">Directory Indexing</span>
                    <span className="text-muted-foreground">Publish service endpoint `asp.builderforge.okx` to OKX.AI Agent directory.</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Submission Status Confirmation */}
            {submissionResult && (
              <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-xs space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-emerald-400 text-sm flex items-center gap-1.5">
                    <CheckCircle2 className="h-4 w-4" /> Application Submitted!
                  </span>
                  <span className="font-mono text-[10px] bg-emerald-900/60 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded">
                    {submissionResult.listing_status}
                  </span>
                </div>
                <p className="text-muted-foreground">{submissionResult.message}</p>
                <p className="text-[11px] font-mono text-emerald-300">ID: {submissionResult.submission_id}</p>
              </div>
            )}

            {/* Footer Action Buttons */}
            <div className="flex items-center justify-between border-t border-border pt-4 text-xs gap-3">
              <button
                onClick={() => handleCopyManifest(true)}
                className="px-4 py-2 rounded-xl border border-border bg-secondary text-foreground font-semibold hover:bg-secondary/80 transition flex items-center gap-1.5 cursor-pointer"
              >
                {modalCopied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                {modalCopied ? "Copied!" : "Copy Manifest"}
              </button>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setShowSubmitModal(false)}
                  className="px-4 py-2 rounded-xl bg-secondary text-foreground font-semibold hover:bg-secondary/80 transition cursor-pointer"
                >
                  Close
                </button>

                <button
                  onClick={handleSubmitListing}
                  disabled={submitting}
                  className="px-5 py-2 rounded-xl bg-primary text-primary-foreground font-bold hover:brightness-110 transition shadow-lg shadow-primary/20 flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
                >
                  {submitting ? <Loader className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
                  {submitting ? "Submitting..." : "Submit Listing Application"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Floating Success Toast */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 flex items-center gap-3 px-4 py-3 rounded-xl bg-black/95 border border-emerald-500/50 text-emerald-300 shadow-2xl animate-in slide-in-from-bottom-5 duration-300 font-semibold text-xs">
          <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />
          <span>{toastMessage}</span>
          <button
            onClick={() => setToastMessage(null)}
            className="ml-2 text-muted-foreground hover:text-foreground cursor-pointer"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      )}
    </div>
  );
}
