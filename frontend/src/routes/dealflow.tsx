import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { useDeals, useDiscoverDeals, useProjects } from "../hooks/useApi";
import { 
  Loader, 
  Search, 
  Sparkles, 
  TrendingUp, 
  CheckCircle2, 
  ExternalLink, 
  X, 
  Award, 
  DollarSign, 
  Zap, 
  Filter, 
  Bookmark, 
  BookmarkCheck,
  ChevronRight,
  Target,
  ArrowUpRight
} from "lucide-react";
import { AuthGuard } from "../components/AuthGuard";
import type { Deal } from "../lib/api";

export const Route = createFileRoute("/dealflow")({
  component: () => (
    <AuthGuard pageTitle="DealFlow">
      <DealFlow />
    </AuthGuard>
  ),
});

export function DealFlow() {
  const { data: rawDeals = [], isLoading, error } = useDeals("all");
  const { data: projects = [] } = useProjects();
  const discoverMutation = useDiscoverDeals();

  const [searchQuery, setSearchQuery] = useState("");
  const [activeFilter, setActiveFilter] = useState<string>("All");
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);
  const [trackedDealIds, setTrackedDealIds] = useState<string[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [discovering, setDiscovering] = useState(false);
  const [extraDeals, setExtraDeals] = useState<Deal[]>([]);

  // Merge deals from API and locally discovered deals
  const deals = [...extraDeals, ...rawDeals];

  // Filter chips list
  const filterChips = ["All", "Tracked", "Grants", "Funding", "Partnerships", "Active"];

  // Filter deals based on search and selected chip
  const filteredDeals = deals.filter((deal) => {
    // Search query match
    const q = searchQuery.toLowerCase().trim();
    const matchesSearch = !q || 
      deal.title.toLowerCase().includes(q) ||
      deal.description.toLowerCase().includes(q) ||
      (deal.category && deal.category.toLowerCase().includes(q)) ||
      deal.tags.some(t => t.toLowerCase().includes(q));

    // Filter chip match
    if (!matchesSearch) return false;

    if (activeFilter === "All") return true;
    if (activeFilter === "Tracked") return trackedDealIds.includes(deal.id);
    if (activeFilter === "Active") return deal.status === "active";
    if (activeFilter === "Grants") return deal.category?.toLowerCase() === "grants" || deal.tags.some(t => t.toLowerCase().includes("grant"));
    if (activeFilter === "Funding") return deal.category?.toLowerCase() === "funding" || deal.tags.some(t => t.toLowerCase().includes("seed") || t.toLowerCase().includes("fund"));
    if (activeFilter === "Partnerships") return deal.category?.toLowerCase() === "partnerships" || deal.tags.some(t => t.toLowerCase().includes("partner") || t.toLowerCase().includes("asp"));

    return true;
  });

  const handleDiscoverNew = async () => {
    setDiscovering(true);
    try {
      const discovered = await discoverMutation.mutateAsync("OKX Ecosystem DeAI Grants");
      if (discovered && discovered.length > 0) {
        setExtraDeals(prev => [...discovered, ...prev]);
        setToastMessage(`✨ Discovered ${discovered.length} new high-match opportunities!`);
      } else {
        setToastMessage("🔍 Scanned OKX registry: All current opportunities up to date.");
      }
    } catch (err: any) {
      setToastMessage("Failed to discover new opportunities. Please try again.");
    } finally {
      setDiscovering(false);
      setTimeout(() => setToastMessage(null), 4000);
    }
  };

  const toggleTrackDeal = (dealId: string, dealTitle: string) => {
    if (trackedDealIds.includes(dealId)) {
      setTrackedDealIds(prev => prev.filter(id => id !== dealId));
      setToastMessage(`Removed '${dealTitle}' from tracked opportunities.`);
    } else {
      setTrackedDealIds(prev => [...prev, dealId]);
      setToastMessage(`Saved '${dealTitle}' to tracked opportunities!`);
    }
    setTimeout(() => setToastMessage(null), 3500);
  };

  return (
    <div className="flex min-h-screen bg-background relative">
      <main className="flex-1">
        <div className="px-6 py-8 max-w-6xl mx-auto space-y-6">
          {/* Header & Title Bar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-semibold text-primary mb-3">
                <TrendingUp className="h-3.5 w-3.5" /> OKX ECOSYSTEM DEALFLOW
              </div>
              <h1 className="text-4xl font-extrabold tracking-tight text-foreground">DealFlow</h1>
              <p className="text-muted-foreground mt-2">
                Discover active grant pools, venture funding, and strategic partnerships tailored for your BuilderForge projects
              </p>
            </div>

            <button
              onClick={handleDiscoverNew}
              disabled={discovering}
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-bold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20 cursor-pointer disabled:opacity-60 shrink-0"
            >
              {discovering ? <Loader className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              {discovering ? "Scanning OKX Ecosystem..." : "Discover New Opportunities"}
            </button>
          </div>

          {/* Search Bar & Filter Chips Header */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-card p-4 rounded-xl border border-border shadow-md">
            {/* Search Input */}
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by title, category, tags (e.g. Grant, OKX, DeAI)..."
                className="w-full bg-background border border-input rounded-lg pl-10 pr-4 py-2 text-xs font-medium text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery("")}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground text-xs"
                >
                  Clear
                </button>
              )}
            </div>

            {/* Filter Chips */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
              <Filter className="h-3.5 w-3.5 text-muted-foreground shrink-0 mr-1 hidden md:inline-block" />
              {filterChips.map((chip) => {
                const isActive = activeFilter === chip;
                const countBadge = chip === "Tracked" ? ` (${trackedDealIds.length})` : "";
                return (
                  <button
                    key={chip}
                    onClick={() => setActiveFilter(chip)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer shrink-0 border ${
                      isActive
                        ? "bg-primary text-primary-foreground border-primary shadow-sm"
                        : "bg-secondary/60 text-muted-foreground border-border hover:text-foreground hover:bg-secondary"
                    }`}
                  >
                    {chip}{countBadge}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Results Summary */}
          <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
            <span>
              Showing <strong className="text-foreground font-semibold">{filteredDeals.length}</strong> opportunities
              {activeFilter !== "All" && <span> in <strong className="text-primary">{activeFilter}</strong></span>}
            </span>
            {projects.length > 0 && (
              <span className="flex items-center gap-1 text-emerald-400 font-medium">
                <CheckCircle2 className="h-3.5 w-3.5" /> Matched with {projects.length} Dashboard project{projects.length > 1 ? "s" : ""}
              </span>
            )}
          </div>

          {/* Deals Grid */}
          {isLoading ? (
            <div className="flex justify-center items-center py-16">
              <Loader className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : error ? (
            <div className="bg-destructive/10 border border-destructive rounded-xl p-6 text-destructive text-sm">
              <p className="font-semibold">Error loading dealflow data</p>
              <p className="text-xs mt-1">{String(error)}</p>
            </div>
          ) : filteredDeals.length === 0 ? (
            <div className="text-center py-16 bg-card border border-border rounded-xl p-8 space-y-3">
              <Target className="h-10 w-10 text-muted-foreground mx-auto" />
              <h3 className="text-base font-bold text-foreground">No matching opportunities found</h3>
              <p className="text-xs text-muted-foreground max-w-md mx-auto">
                Try adjusting your search query or filter chips, or click "Discover New Opportunities" to run a fresh scan.
              </p>
              <button
                onClick={() => { setSearchQuery(""); setActiveFilter("All"); }}
                className="px-4 py-2 rounded-lg bg-secondary text-xs font-semibold text-foreground hover:bg-secondary/80 transition cursor-pointer mt-2"
              >
                Reset Filters
              </button>
            </div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {filteredDeals.map((deal) => {
                const isTracked = trackedDealIds.includes(deal.id);
                const score = deal.match_score || 90;

                return (
                  <div 
                    key={deal.id} 
                    className="bg-card border border-border rounded-xl p-5 hover:border-primary/50 transition-all duration-200 shadow-lg flex flex-col justify-between space-y-4 relative group overflow-hidden"
                  >
                    {/* Top Row: Category & Status Badges */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] font-bold uppercase px-2.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20 font-mono">
                            {deal.category || "Grants"}
                          </span>
                          <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded border ${
                            deal.status === "active"
                              ? "bg-emerald-950/60 text-emerald-400 border-emerald-500/30"
                              : deal.status === "upcoming"
                              ? "bg-cyan-950/60 text-cyan-300 border-cyan-500/30"
                              : "bg-secondary text-muted-foreground border-border"
                          }`}>
                            {deal.status}
                          </span>
                        </div>

                        {/* Match Score Badge */}
                        <div className="flex items-center gap-1 bg-black/60 px-2.5 py-1 rounded-full border border-emerald-500/30 text-emerald-300 font-mono text-[11px] font-bold shadow-sm">
                          <Sparkles className="h-3 w-3 text-emerald-400" />
                          <span>{score}% Match</span>
                        </div>
                      </div>

                      {/* Title & Description */}
                      <div>
                        <h3 className="text-base font-extrabold text-foreground group-hover:text-primary transition line-clamp-2 leading-snug">
                          {deal.title}
                        </h3>
                        <p className="text-xs text-muted-foreground mt-2 line-clamp-3 leading-relaxed">
                          {deal.description}
                        </p>
                      </div>
                    </div>

                    {/* Funding Stage / Amount Pill */}
                    <div className="space-y-4 pt-2">
                      <div className="flex items-center justify-between text-xs bg-secondary/40 p-2.5 rounded-lg border border-border/50">
                        <span className="text-muted-foreground flex items-center gap-1 text-[11px]">
                          <Award className="h-3.5 w-3.5 text-primary" /> Funding Tier
                        </span>
                        <span className="font-bold text-foreground font-mono">{deal.funding_stage}</span>
                      </div>

                      {/* Tags */}
                      <div className="flex flex-wrap gap-1.5">
                        {deal.tags.map((tag) => (
                          <span key={tag} className="text-[10px] bg-secondary text-muted-foreground px-2 py-0.5 rounded font-medium border border-border/40">
                            #{tag}
                          </span>
                        ))}
                      </div>

                      {/* Card Action Buttons */}
                      <div className="flex items-center gap-2 pt-1 border-t border-border/40">
                        <button
                          onClick={() => setSelectedDeal(deal)}
                          className="flex-1 rounded-lg bg-primary/10 border border-primary/30 px-3 py-2 text-xs font-bold text-primary hover:bg-primary hover:text-primary-foreground transition flex items-center justify-center gap-1 cursor-pointer"
                        >
                          View Details
                          <ChevronRight className="h-3.5 w-3.5" />
                        </button>

                        <button
                          onClick={() => toggleTrackDeal(deal.id, deal.title)}
                          className={`p-2 rounded-lg border text-xs transition cursor-pointer ${
                            isTracked 
                              ? "bg-emerald-950/60 border-emerald-500/40 text-emerald-400" 
                              : "bg-secondary/80 border-border text-muted-foreground hover:text-foreground hover:bg-secondary"
                          }`}
                          title={isTracked ? "Tracked Opportunity" : "Track Opportunity"}
                        >
                          {isTracked ? <BookmarkCheck className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </main>

      {/* Opportunity Details Modal */}
      {selectedDeal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-card border border-border rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-6 relative max-h-[90vh] overflow-y-auto custom-scrollbar text-foreground">
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-border pb-4 gap-3">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-[10px] font-bold uppercase px-2.5 py-0.5 rounded bg-primary/10 text-primary border border-primary/20 font-mono">
                    {selectedDeal.category || "Grants"}
                  </span>
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-500/30">
                    {selectedDeal.status}
                  </span>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-black/60 text-emerald-300 border border-emerald-500/30 font-mono">
                    ✨ {selectedDeal.match_score || 94}% Match Score
                  </span>
                </div>
                <h2 className="text-xl font-extrabold text-foreground leading-tight">
                  {selectedDeal.title}
                </h2>
              </div>
              <button
                onClick={() => setSelectedDeal(null)}
                className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition cursor-pointer shrink-0"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Opportunity Description */}
            <div className="space-y-2">
              <h4 className="text-xs uppercase font-bold tracking-wider text-muted-foreground">Overview</h4>
              <p className="text-xs leading-relaxed text-muted-foreground bg-secondary/20 p-3.5 rounded-xl border border-border/50">
                {selectedDeal.description}
              </p>
            </div>

            {/* Why It Matches Rationale */}
            <div className="space-y-2">
              <h4 className="text-xs uppercase font-bold tracking-wider text-primary flex items-center gap-1.5">
                <Sparkles className="h-4 w-4" /> Why It Matches Your Project
              </h4>
              <div className="bg-primary/10 border border-primary/30 p-3.5 rounded-xl text-xs space-y-1 text-foreground">
                <p className="leading-relaxed">
                  {selectedDeal.why_it_matches || "Matches your active BuilderForge project stack with target smart contract infrastructure on OKX X Layer Testnet (Chain ID 195)."}
                </p>
              </div>
            </div>

            {/* Recommended Next Action */}
            <div className="space-y-2">
              <h4 className="text-xs uppercase font-bold tracking-wider text-emerald-400 flex items-center gap-1.5">
                <Zap className="h-4 w-4" /> Recommended Next Action
              </h4>
              <div className="bg-emerald-950/30 border border-emerald-500/30 p-3.5 rounded-xl text-xs space-y-1 text-emerald-300 font-medium">
                <p className="leading-relaxed">
                  {selectedDeal.recommended_action || "Run contract deployment simulation on LaunchPad and submit verified ASP manifest payload to OKX ecosystem review portal."}
                </p>
              </div>
            </div>

            {/* Quick Details Grid */}
            <div className="grid grid-cols-2 gap-3 text-xs font-mono">
              <div className="bg-secondary/40 p-3 rounded-lg border border-border/50">
                <span className="text-muted-foreground text-[10px] uppercase font-sans font-bold block mb-1">Funding Amount</span>
                <span className="text-foreground font-bold">{selectedDeal.funding_stage}</span>
              </div>
              <div className="bg-secondary/40 p-3 rounded-lg border border-border/50">
                <span className="text-muted-foreground text-[10px] uppercase font-sans font-bold block mb-1">Target Ecosystem</span>
                <span className="text-cyan-300 font-bold">OKX X Layer Testnet</span>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-border pt-4">
              <button
                onClick={() => toggleTrackDeal(selectedDeal.id, selectedDeal.title)}
                className={`w-full sm:w-auto px-4 py-2.5 rounded-xl text-xs font-bold transition cursor-pointer flex items-center justify-center gap-2 border ${
                  trackedDealIds.includes(selectedDeal.id)
                    ? "bg-emerald-950/80 border-emerald-500/40 text-emerald-400"
                    : "bg-secondary border-border text-foreground hover:bg-secondary/80"
                }`}
              >
                {trackedDealIds.includes(selectedDeal.id) ? (
                  <>
                    <BookmarkCheck className="h-4 w-4" /> Tracked Opportunity
                  </>
                ) : (
                  <>
                    <Bookmark className="h-4 w-4" /> Track Opportunity
                  </>
                )}
              </button>

              <div className="flex items-center gap-2 w-full sm:w-auto">
                <button
                  onClick={() => setSelectedDeal(null)}
                  className="px-4 py-2.5 rounded-xl bg-secondary text-xs font-semibold text-foreground hover:bg-secondary/80 transition cursor-pointer"
                >
                  Close
                </button>

                <a
                  href={selectedDeal.apply_url || "https://www.okx.com/xlayer"}
                  target="_blank"
                  rel="noreferrer"
                  className="flex-1 sm:flex-initial px-5 py-2.5 rounded-xl bg-primary text-xs font-bold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20 flex items-center justify-center gap-1.5"
                >
                  Apply Now
                  <ArrowUpRight className="h-4 w-4" />
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Success Toast Notification */}
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
