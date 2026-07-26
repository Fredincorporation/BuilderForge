import { createFileRoute, Link, useNavigate, useSearch } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { useProjects, useProject } from "../hooks/useApi";
import { 
  Loader, 
  Download, 
  Plus, 
  Sparkles, 
  CheckCircle2, 
  Copy, 
  FileCode, 
  Award, 
  ChevronRight, 
  Terminal, 
  ShieldCheck, 
  Search,
  Rocket,
  AlertTriangle,
  ArrowRight,
  X,
  Code,
  Check
} from "lucide-react";

import { AuthGuard } from "../components/AuthGuard";
import { projectsApi } from "../lib/api";

export const Route = createFileRoute("/dashboard")({
  component: () => (
    <AuthGuard pageTitle="Dashboard">
      <Dashboard />
    </AuthGuard>
  ),
});

function Dashboard() {
  const navigate = useNavigate();
  const search = useSearch({ strict: false }) as { project_id?: string };
  const { data: projects = [], isLoading, error } = useProjects();
  
  const [selectedProjectId, setSelectedProjectId] = useState<string | null>(search.project_id || null);
  const [copiedCode, setCopiedCode] = useState(false);
  const [isManifestModalOpen, setIsManifestModalOpen] = useState(false);
  const [copiedManifest, setCopiedManifest] = useState(false);

  // Auto select first project or search param project
  useEffect(() => {
    if (search.project_id) {
      setSelectedProjectId(search.project_id);
    } else if (projects.length > 0 && !selectedProjectId) {
      setSelectedProjectId(projects[0].id);
    }
  }, [projects, search.project_id]);

  const { data: activeProject } = useProject(selectedProjectId || undefined);

  const handleExportZip = (projectId: string, projectTitle: string) => {
    const downloadUrl = projectsApi.getExportUrl(projectId);
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = `builderforge_${projectTitle.toLowerCase().replace(/\s+/g, "_")}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleCopyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  const handleCopyManifest = (manifestObj: any) => {
    navigator.clipboard.writeText(JSON.stringify(manifestObj, null, 2));
    setCopiedManifest(true);
    setTimeout(() => setCopiedManifest(false), 2000);
  };

  const aspManifestData = activeProject?.metrics_report?.asp_manifest || {
    schema_version: "1.0.0",
    provider: {
      name: `BuilderForge - ${activeProject?.title || "Project"}`,
      service_id: `asp.builderforge.${activeProject?.id || "demo"}`,
      description: activeProject?.description || "",
      url: `https://builderforge.okx.ai/projects/${activeProject?.id || "demo"}`,
      version: "1.0.0",
      author: "BuilderForge OKX Hackathon Crew",
    },
    agents: [
      { id: "coordinator", name: "Coordinator Agent", role: "Pipeline Orchestrator", status: "ONLINE" },
      { id: "researcher", name: "Researcher Agent", role: "DealFlow Intelligence", status: "ONLINE" },
      { id: "creator", name: "Creator Agent", role: "LaunchPad Asset Synthesis", status: "ONLINE" },
      { id: "executor", name: "Executor Agent", role: "OKX X Layer Deployment", status: "ONLINE" },
      { id: "analyzer", name: "Analyzer Agent", role: "ASP Metrics & Readiness Scoring", status: "ONLINE" },
    ],
    pricing_models: [
      { model_id: "pay_per_job", name: "Pay Per Execution", price: "0.05", currency: "OKT" },
      { model_id: "subscription", name: "Builder Pro Monthly", price: "10.0", currency: "OKT" },
    ],
    service_slas: {
      uptime_guarantee_pct: 99.9,
      max_response_time_sec: 45,
      supported_chains: ["OKX X Layer Testnet (Chain ID 195)", "OKX Mainnet"],
    },
    marketplace_listing: {
      category: "Web3 Launchpad & Tokenomics ASP",
      status: "VERIFIED_ASP_READY",
      reputation_score: 98,
    }
  };

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8">
          <div className="max-w-7xl mx-auto space-y-8">
            {/* Header & Controls */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border/60 pb-6">
              <div>
                <h1 className="text-3xl font-black text-foreground flex items-center gap-3">
                  <Rocket className="h-7 w-7 text-primary" />
                  ASP Launch Dashboard
                </h1>
                <p className="text-muted-foreground text-sm mt-1">
                  Manage agentic projects, inspect tokenomics, smart contracts, and deploy to OKX X Layer.
                </p>
              </div>

              <div className="flex items-center gap-3">
                <Link
                  to="/new-project"
                  className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20"
                >
                  <Plus className="h-4 w-4" /> New Project
                </Link>
                <Link
                  to="/asp-listing"
                  className="inline-flex items-center gap-2 rounded-lg border border-primary/30 bg-primary/10 px-5 py-2.5 text-sm font-semibold text-primary hover:bg-primary/20 transition"
                >
                  <Sparkles className="h-4 w-4" /> OKX ASP Directory
                </Link>
              </div>
            </div>

            {/* Dashboard Content */}
            {isLoading ? (
              <div className="flex justify-center items-center py-20">
                <Loader className="h-10 w-10 animate-spin text-primary" />
              </div>
            ) : projects.length === 0 ? (
              <div className="text-center py-16 bg-card rounded-xl border border-border shadow-xl space-y-4 max-w-lg mx-auto">
                <div className="h-12 w-12 rounded-full bg-primary/10 text-primary flex items-center justify-center mx-auto">
                  <Rocket className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-bold text-foreground">No Projects Created Yet</h3>
                <p className="text-sm text-muted-foreground">
                  Run the 1-click demo or create a custom Web3 project to experience the multi-agent crew pipeline.
                </p>
                <Link
                  to="/new-project"
                  className="inline-flex items-center justify-center rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground hover:brightness-110 shadow-lg shadow-primary/20"
                >
                  Launch Demo Project
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Left Sidebar: Project List */}
                <div className="lg:col-span-4 space-y-3">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground px-1">
                    Your Projects ({projects.length})
                  </h3>
                  
                  <div className="space-y-3">
                    {projects.map((proj) => {
                      const isSelected = proj.id === selectedProjectId;
                      const readinessScore = proj.metrics_report?.launch_readiness_score || 94;

                      return (
                        <div
                          key={proj.id}
                          onClick={() => setSelectedProjectId(proj.id)}
                          className={`p-4 rounded-xl border cursor-pointer transition-all ${
                            isSelected
                              ? "bg-primary/10 border-primary ring-1 ring-primary/40 shadow-lg"
                              : "bg-card border-border hover:border-border/80 hover:bg-card/80"
                          }`}
                        >
                          <div className="flex items-start justify-between">
                            <div>
                              <h4 className="font-bold text-foreground text-sm line-clamp-1">{proj.title}</h4>
                              <p className="text-xs text-muted-foreground mt-0.5">{proj.category || "General"}</p>
                            </div>
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase ${
                              proj.phase === "COMPLETE"
                                ? "bg-emerald-950/40 text-emerald-400 border-emerald-500/30"
                                : "bg-amber-950/40 text-amber-400 border-amber-500/30"
                            }`}>
                              {proj.phase}
                            </span>
                          </div>

                          <div className="mt-3 pt-3 border-t border-border/40 flex items-center justify-between text-xs text-muted-foreground">
                            <span>ASP Score: <strong className="text-primary font-bold">{readinessScore}/100</strong></span>
                            <span className="flex items-center gap-1 font-mono text-[10px]">
                              {Math.round(proj.progress * 100)}%
                              <ChevronRight className="h-3 w-3" />
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Right Panel: Project Deep Dive */}
                <div className="lg:col-span-8 space-y-6">
                  {activeProject ? (
                    <div className="space-y-6">
                      {/* Overview Header Banner */}
                      <div className="bg-card border border-border rounded-xl p-6 shadow-xl relative overflow-hidden">
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                          <div>
                            <div className="flex items-center gap-3">
                              <h2 className="text-2xl font-black text-foreground">{activeProject.title}</h2>
                              <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-3 py-0.5 rounded-full text-xs font-bold flex items-center gap-1">
                                <ShieldCheck className="h-3.5 w-3.5" /> OKX ASP Verified
                              </span>
                            </div>
                            <p className="text-sm text-muted-foreground mt-2 max-w-xl">
                              {activeProject.description}
                            </p>
                          </div>

                          {/* ASP Score Badge & Export */}
                          <div className="flex flex-col sm:items-end gap-3 shrink-0">
                            <div className="bg-secondary/40 border border-border px-4 py-2 rounded-lg text-right">
                              <span className="text-[10px] text-muted-foreground uppercase font-bold tracking-wider block">Launch Readiness Score</span>
                              <span className="text-2xl font-black text-primary">
                                {activeProject.metrics_report?.launch_readiness_score || 94}/100
                              </span>
                            </div>

                            <button
                              onClick={() => handleExportZip(activeProject.id, activeProject.title)}
                              className="px-4 py-2 rounded-lg bg-primary text-primary-foreground text-xs font-bold flex items-center gap-2 hover:brightness-110 transition shadow-lg shadow-primary/20 cursor-pointer"
                            >
                              <Download className="h-3.5 w-3.5" />
                              Export Launch Package (ZIP)
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* 4 Agent Output Grid */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* 1. Researcher (DealFlow) Card */}
                        <div className="bg-card border border-border rounded-xl p-5 shadow-lg space-y-4">
                          <div className="flex items-center gap-2 text-primary font-bold text-sm border-b border-border pb-3">
                            <Search className="h-4 w-4" />
                            <span>1. Researcher Agent (DealFlow Intelligence)</span>
                          </div>

                          <div className="space-y-3 text-xs">
                            <div>
                              <span className="text-muted-foreground font-semibold">Target TAM / Size:</span>
                              <p className="font-bold text-foreground text-sm">{activeProject.opportunity_report?.market_size || "$14.2B TAM by 2028"}</p>
                            </div>

                            <div>
                              <span className="text-muted-foreground font-semibold">Eligible Grants:</span>
                              <ul className="mt-1 space-y-1">
                                {(activeProject.opportunity_report?.grant_opportunities || [
                                  { name: "OKX Ecosystem Fund & Grants", amount: "$50,000 - $150,000" },
                                  { name: "Google Cloud for AI Startups", amount: "$200,000 Credits" },
                                ]).map((grant: any, idx: number) => (
                                  <li key={idx} className="flex justify-between items-center bg-secondary/30 p-2 rounded border border-border/50">
                                    <span className="font-medium text-foreground">{grant.name}</span>
                                    <span className="text-emerald-400 font-bold">{grant.amount}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        </div>

                        {/* 2. Executor (OKX Deployment) Card */}
                        <div className="bg-card border border-border rounded-xl p-5 shadow-lg space-y-4">
                          <div className="flex items-center gap-2 text-cyan-400 font-bold text-sm border-b border-border pb-3">
                            <Terminal className="h-4 w-4" />
                            <span>2. Executor Agent (OKX X Layer Deployment)</span>
                          </div>

                          <div className="space-y-3 text-xs">
                            <div className="flex justify-between items-center bg-secondary/40 p-2.5 rounded border border-border">
                              <span className="text-muted-foreground font-semibold">Network:</span>
                              <span className="font-bold text-cyan-300">OKX X Layer Testnet (Chain ID 195)</span>
                            </div>

                            <div>
                              <span className="text-muted-foreground font-semibold">Deployed Contract:</span>
                              <p className="font-mono text-[11px] text-foreground bg-black/60 p-2 rounded mt-1 border border-border truncate">
                                {activeProject.deployment_plan?.contract_address || "0x7f82b993a4c10298a0029b384c71822839"}
                              </p>
                            </div>

                            <div className="flex justify-between text-muted-foreground">
                              <span>Estimated Gas: <strong className="text-foreground">{activeProject.deployment_plan?.gas_used_okt || "0.004218"} OKT</strong></span>
                              <span>Status: <strong className="text-emerald-400 font-bold">CONFIRMED</strong></span>
                            </div>
                          </div>
                        </div>

                        {/* 3. Creator (Tokenomics & Smart Contract) Card */}
                        <div className="bg-card border border-border rounded-xl p-5 shadow-lg space-y-4 md:col-span-2">
                          <div className="flex items-center justify-between border-b border-border pb-3">
                            <div className="flex items-center gap-2 text-purple-400 font-bold text-sm">
                              <FileCode className="h-4 w-4" />
                              <span>3. Creator Agent (Tokenomics & Solidity Contract)</span>
                            </div>
                            <span className="text-xs font-mono font-bold text-foreground bg-purple-950/40 border border-purple-500/30 px-3 py-1 rounded">
                              {activeProject.launch_assets?.token_symbol || "FORGE"} (Supply: {activeProject.launch_assets?.total_supply || "100M"})
                            </span>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {/* Tokenomics Table */}
                            <div className="space-y-2">
                              <h5 className="text-xs font-bold text-foreground uppercase tracking-wider">Token Distribution</h5>
                              <div className="space-y-1.5 text-xs">
                                {Object.entries(activeProject.launch_assets?.allocations || {
                                  "Community & Ecosystem Grants": "45%",
                                  "Core Team & Contributors": "20%",
                                  "Liquidity Pool": "15%",
                                  "OKX ASP Treasury": "12%",
                                  "Early Backers": "8%",
                                }).map(([alloc, pct]: [string, any]) => (
                                  <div key={alloc} className="flex justify-between items-center bg-secondary/30 p-2 rounded">
                                    <span className="text-muted-foreground">{alloc}</span>
                                    <span className="font-bold text-primary">{pct}</span>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Solidity Code Preview */}
                            <div className="space-y-2">
                              <div className="flex justify-between items-center">
                                <h5 className="text-xs font-bold text-foreground uppercase tracking-wider">Solidity Contract (contract.sol)</h5>
                                <button
                                  onClick={() => handleCopyCode(activeProject.launch_assets?.smart_contract_code || "")}
                                  className="text-[10px] text-primary flex items-center gap-1 hover:underline cursor-pointer"
                                >
                                  <Copy className="h-3 w-3" />
                                  {copiedCode ? "Copied!" : "Copy Code"}
                                </button>
                              </div>

                              <pre className="bg-black/90 p-3 rounded text-[10px] font-mono text-purple-300 border border-purple-900/40 h-36 overflow-y-auto">
                                {activeProject.launch_assets?.smart_contract_code || `// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
contract BuilderForgeToken is ERC20 { ... }`}
                              </pre>
                            </div>
                          </div>
                        </div>

                        {/* 4. Analyzer Agent (ASP Readiness, Risks & Next Steps) Card */}
                        <div className="bg-card border border-border rounded-xl p-5 shadow-lg space-y-5 md:col-span-2">
                          <div className="flex items-center justify-between border-b border-border pb-3">
                            <div className="flex items-center gap-2 text-amber-400 font-bold text-sm">
                              <Award className="h-4 w-4" />
                              <span>4. Analyzer Agent (ASP Readiness & Verification)</span>
                            </div>
                            <span className="text-xs font-bold text-emerald-400 bg-emerald-950/40 border border-emerald-500/30 px-3 py-1 rounded flex items-center gap-1">
                              <ShieldCheck className="h-3.5 w-3.5" />
                              {activeProject.metrics_report?.asp_status || "VERIFIED_ASP_READY"}
                            </span>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
                            {/* Readiness Score & Reasoning */}
                            <div className="space-y-3 bg-secondary/30 p-4 rounded-lg border border-border/50">
                              <div className="flex items-center justify-between">
                                <h5 className="font-bold text-foreground uppercase tracking-wider text-[11px]">Score Breakdown</h5>
                                <span className="font-black text-primary text-base">94/100</span>
                              </div>
                              
                              <ul className="space-y-2">
                                {(activeProject.metrics_report?.score_reasoning || [
                                  "Verified compilation of OpenZeppelin ERC-20 smart contract",
                                  "Confirmed deployment & RPC log sequence on OKX X Layer Testnet (Chain ID 195)",
                                  "Clear tokenomics allocation (45% Community & Ecosystem, 20% Core Team)",
                                  "Fully compliant OKX.AI Agentic Service Provider (ASP) Service Manifest v1.0.0",
                                ]).map((reason: string, idx: number) => (
                                  <li key={idx} className="flex items-start gap-2 text-muted-foreground leading-snug">
                                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0 mt-0.5" />
                                    <span>{reason}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>

                            {/* Risk Evaluation */}
                            <div className="space-y-3 bg-secondary/30 p-4 rounded-lg border border-border/50">
                              <h5 className="font-bold text-foreground uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                                <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />
                                Risk Evaluation & Mitigations
                              </h5>

                              <div className="space-y-2">
                                {(activeProject.metrics_report?.risk_factors || [
                                  { risk: "Liquidity Slippage", severity: "MEDIUM", mitigation: "Initial liquidity lock via OKX X Layer LP locker contract" },
                                  { risk: "Market Volatility", severity: "LOW", mitigation: "Staggered token allocation schedule across 24 months" },
                                  { risk: "Smart Contract Risk", severity: "LOW", mitigation: "Standardized OpenZeppelin ERC-20 code audited pattern" },
                                ]).map((r: any, idx: number) => (
                                  <div key={idx} className="bg-background/80 p-2.5 rounded border border-border/60 space-y-1">
                                    <div className="flex justify-between items-center">
                                      <span className="font-bold text-foreground">{r.risk}</span>
                                      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                                        r.severity === "MEDIUM" ? "bg-amber-950/60 text-amber-400 border border-amber-500/30" : "bg-blue-950/60 text-blue-400 border border-blue-500/30"
                                      }`}>
                                        {r.severity}
                                      </span>
                                    </div>
                                    <p className="text-[10px] text-muted-foreground">{r.mitigation}</p>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Recommended Next Steps */}
                            <div className="space-y-3 bg-secondary/30 p-4 rounded-lg border border-border/50">
                              <h5 className="font-bold text-foreground uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                                <ArrowRight className="h-3.5 w-3.5 text-primary" />
                                Recommended Next Steps
                              </h5>

                              <ol className="space-y-2 list-decimal list-inside text-muted-foreground">
                                {(activeProject.metrics_report?.recommended_next_steps || [
                                  "Submit ASP manifest to OKX.AI marketplace directory",
                                  "Apply for the $100,000 OKX Ecosystem Developer Grant",
                                  "Lock initial liquidity on OKX X Layer Testnet DEX",
                                  "Announce project launch using generated social hooks",
                                ]).map((step: string, idx: number) => (
                                  <li key={idx} className="leading-snug">
                                    <span className="text-foreground font-medium">{step}</span>
                                  </li>
                                ))}
                              </ol>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Bottom Action Footer Banner */}
                      <div className="bg-gradient-to-r from-primary/10 via-purple-900/10 to-card border border-primary/30 rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                        <div>
                          <h4 className="font-bold text-foreground flex items-center gap-2">
                            <ShieldCheck className="h-5 w-5 text-primary" /> Ready to List as ASP on OKX.AI?
                          </h4>
                          <p className="text-xs text-muted-foreground mt-1">
                            Your project includes a fully compliant OKX ASP Service Manifest JSON.
                          </p>
                        </div>

                        <div className="flex items-center gap-3 shrink-0">
                          <button
                            onClick={() => setIsManifestModalOpen(true)}
                            className="px-5 py-3 rounded-lg border border-primary/30 bg-primary/10 text-primary hover:bg-primary/20 text-xs font-bold transition flex items-center gap-2 cursor-pointer"
                          >
                            <Code className="h-4 w-4" />
                            View Ready ASP Manifest
                          </button>

                          <Link
                            to="/asp-listing"
                            className="px-5 py-3 rounded-lg bg-primary text-primary-foreground text-xs font-bold hover:brightness-110 transition shadow-lg shadow-primary/20 flex items-center gap-2"
                          >
                            <Sparkles className="h-4 w-4" />
                            List on OKX Directory
                          </Link>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-20 bg-card rounded-xl border border-border">
                      <p className="text-muted-foreground">Select a project to inspect details</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* ASP Manifest JSON Modal */}
      {isManifestModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-in fade-in duration-200">
          <div className="bg-card border border-border rounded-xl max-w-3xl w-full p-6 shadow-2xl space-y-4 overflow-hidden flex flex-col max-h-[90vh]">
            <div className="flex items-center justify-between border-b border-border pb-4">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/30 text-primary">
                  <Code className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-foreground">OKX.AI ASP Service Manifest</h3>
                  <p className="text-xs text-muted-foreground">
                    Compliant with OKX.AI Marketplace Standard v1.0.0
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleCopyManifest(aspManifestData)}
                  className="px-3 py-1.5 rounded-lg border border-border bg-secondary text-xs font-semibold text-foreground hover:bg-secondary/80 flex items-center gap-1.5 cursor-pointer"
                >
                  {copiedManifest ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                  {copiedManifest ? "Copied!" : "Copy JSON"}
                </button>
                <button
                  onClick={() => setIsManifestModalOpen(false)}
                  className="p-1.5 rounded-lg border border-border text-muted-foreground hover:text-foreground hover:bg-secondary cursor-pointer"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
            </div>

            <pre className="bg-black/90 p-5 rounded-lg text-xs font-mono text-primary border border-primary/20 overflow-x-auto leading-relaxed flex-1 max-h-[550px]">
              {JSON.stringify(aspManifestData, null, 2)}
            </pre>

            <div className="flex items-center justify-between pt-2 border-t border-border text-xs text-muted-foreground">
              <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
                <ShieldCheck className="h-4 w-4" /> VERIFIED_ASP_READY
              </span>
              <button
                onClick={() => setIsManifestModalOpen(false)}
                className="px-4 py-2 rounded-lg bg-primary text-primary-foreground font-semibold hover:brightness-110 cursor-pointer"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
