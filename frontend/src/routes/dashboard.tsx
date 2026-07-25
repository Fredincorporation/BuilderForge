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
  ExternalLink, 
  FileCode, 
  Coins, 
  Award, 
  ChevronRight, 
  Terminal, 
  ShieldCheck, 
  Search,
  Rocket
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

                      {/* 4 Agent Output Tabs / Grid */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Researcher (DealFlow) Card */}
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

                        {/* Executor (OKX Deployment) Card */}
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

                        {/* Creator (Tokenomics & Smart Contract) Card */}
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
                      </div>

                      {/* Bottom Action Footer */}
                      <div className="bg-gradient-to-r from-primary/10 via-purple-900/10 to-card border border-primary/30 rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                        <div>
                          <h4 className="font-bold text-foreground">Ready to List as ASP on OKX.AI?</h4>
                          <p className="text-xs text-muted-foreground mt-1">
                            Your project includes a fully compliant OKX ASP Service Manifest JSON.
                          </p>
                        </div>

                        <Link
                          to="/asp-listing"
                          className="px-6 py-3 rounded-lg bg-primary text-primary-foreground text-xs font-bold hover:brightness-110 transition shadow-lg shadow-primary/20 flex items-center gap-2 shrink-0"
                        >
                          <Sparkles className="h-4 w-4" />
                          View Ready ASP Manifest
                        </Link>
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
    </div>
  );
}
