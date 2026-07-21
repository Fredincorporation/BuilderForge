import { createFileRoute, Link } from "@tanstack/react-router";
import {
  Hammer,
  Home,
  Plus,
  LayoutGrid,
  Briefcase,
  Rocket,
  Link2,
  Lightbulb,
  Search,
  Palette,
  Zap,
  BarChart3,
  Bot,
  Binary,
  Globe,
  Circle,
} from "lucide-react";

export const Route = createFileRoute("/")({
  component: Index,
});

const navItems = [
  { icon: Home, label: "Home", active: true },
  { icon: Plus, label: "New Project" },
  { icon: LayoutGrid, label: "Dashboard" },
  { icon: Briefcase, label: "DealFlow" },
  { icon: Rocket, label: "LaunchPad" },
  { icon: Link2, label: "OKX ASP Listing" },
];

const pipeline = [
  { icon: Lightbulb, label: "Idea Input" },
  { icon: Search, label: "Research" },
  { icon: Palette, label: "Creation" },
  { icon: Zap, label: "Execution" },
  { icon: BarChart3, label: "Analysis" },
];

const features = [
  {
    icon: Bot,
    tint: "bg-[oklch(0.28_0.12_40)] text-[oklch(0.78_0.19_40)]",
    title: "5 Specialized Agents",
    body: "Coordinator, Researcher, Creator, Executor, and Analyzer work in perfect sync to handle the complexity of your deployment.",
  },
  {
    icon: Binary,
    tint: "bg-[oklch(0.25_0.1_240)] text-[oklch(0.72_0.17_240)]",
    title: "OKX Testnet Integration",
    body: "Simulate token deployment and smart contract interactions on OKC testnet with precision gas estimation.",
  },
  {
    icon: Globe,
    tint: "bg-[oklch(0.25_0.09_160)] text-[oklch(0.72_0.15_160)]",
    title: "ASP Ready",
    body: "Seamlessly list on the OKX.AI marketplace with pre-structured manifests and dynamic pricing capabilities.",
  },
];

const stack = [
  { icon: Binary, label: "PYTHON" },
  { icon: Bot, label: "CREWAI" },
  { icon: Link2, label: "LANGCHAIN" },
  { icon: BarChart3, label: "STREAMLIT" },
  { icon: Zap, label: "CLAUDE" },
  { icon: LayoutGrid, label: "OKX WEB3" },
];

function Index() {
  return (
    <div className="flex min-h-screen bg-background text-foreground">
      {/* Sidebar */}
      <aside className="hidden md:flex flex-col w-64 shrink-0 border-r border-border bg-[var(--sidebar-bg)]">
        <div className="flex items-center gap-3 px-6 pt-6 pb-8">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Hammer className="h-5 w-5" />
          </div>
          <span className="text-xl font-bold tracking-tight">BuilderForge</span>
        </div>

        <div className="px-6 text-[10px] font-semibold tracking-[0.2em] text-muted-foreground">
          NAVIGATION
        </div>

        <nav className="mt-3 flex flex-col gap-1 px-3">
          {navItems.map(({ icon: Icon, label, active }) => (
            <Link
              key={label}
              to={
                label === "Home"
                  ? "/"
                  : label === "New Project"
                  ? "/new-project"
                  : label === "Dashboard"
                  ? "/dashboard"
                  : label === "DealFlow"
                  ? "/dealflow"
                  : label === "LaunchPad"
                  ? "/launchpad"
                  : "/"
              }
              className={`flex items-center gap-3 rounded-md px-3 py-2.5 text-sm transition-colors ${
                active
                  ? "bg-[oklch(0.24_0.08_40/0.4)] text-primary"
                  : "text-muted-foreground hover:bg-secondary hover:text-foreground"
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{label}</span>
            </Link>
          ))}
        </nav>

        <div className="mt-auto p-6">
          <div className="flex items-center gap-2 text-xs">
            <Circle className="h-2 w-2 fill-green-500 text-green-500" />
            <span className="font-medium tracking-wider text-muted-foreground">
              SYSTEM ONLINE
            </span>
          </div>
          <div className="mt-1 text-xs text-muted-foreground/70">
            v1.2.4 — Simulated Mode
          </div>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col">
        <section className="flex-1 px-6 py-16 md:py-24">
          <div className="mx-auto max-w-5xl text-center">
            <div className="inline-flex items-center gap-2 rounded-full border border-primary/40 bg-primary/10 px-4 py-1.5 text-xs font-medium text-primary">
              <Circle className="h-1.5 w-1.5 fill-primary text-primary" />
              OKX AI Genesis Hackathon MVP
            </div>

            <h1 className="mt-8 text-6xl md:text-8xl font-black tracking-tight">
              BuilderForge
            </h1>

            <p className="mt-8 text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              The Autonomous Idea-to-Launch Agent for the OKX Ecosystem.
              <br />
              Transform vision into architecture in seconds.
            </p>

            <div className="mt-10 flex flex-wrap justify-center gap-4">
              <Link
                to="/new-project"
                className="rounded-md bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-lg shadow-primary/30 hover:brightness-110 transition"
              >
                Start New Project
              </Link>
              <Link
                to="/dealflow"
                className="rounded-md border border-border bg-card/50 px-6 py-3 text-sm font-semibold text-foreground hover:bg-card transition"
              >
                Explore DealFlow
              </Link>
            </div>

            {/* Pipeline */}
            <div className="mt-24">
              <div className="text-xs font-bold tracking-[0.3em] text-primary">
                EXECUTION PIPELINE
              </div>
              <div className="mx-auto mt-2 h-px w-16 bg-primary/60" />

              <div className="relative mt-12 flex items-start justify-between max-w-4xl mx-auto">
                <div className="absolute left-8 right-8 top-7 h-px bg-[var(--pipeline-line)]" />
                {pipeline.map(({ icon: Icon, label }) => (
                  <div key={label} className="relative flex flex-col items-center gap-3 w-24">
                    <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-border bg-card">
                      <Icon className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <span className="text-sm text-foreground">{label}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Features */}
            <div className="mt-24 grid gap-6 md:grid-cols-3 text-left">
              {features.map(({ icon: Icon, tint, title, body }) => (
                <div
                  key={title}
                  className="rounded-xl border border-border bg-card/70 p-6"
                >
                  <div className={`flex h-10 w-10 items-center justify-center rounded-md ${tint}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <h3 className="mt-5 text-lg font-bold">{title}</h3>
                  <p className="mt-3 text-sm text-muted-foreground leading-relaxed">
                    {body}
                  </p>
                </div>
              ))}
            </div>

            {/* Stack */}
            <div className="mt-24 border-t border-border pt-10">
              <div className="flex flex-wrap justify-center gap-x-10 gap-y-4 text-xs font-semibold tracking-wider text-muted-foreground">
                {stack.map(({ icon: Icon, label }) => (
                  <div key={label} className="flex items-center gap-2">
                    <Icon className="h-4 w-4" />
                    <span>{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <footer className="border-t border-border px-8 py-6">
          <div className="flex flex-wrap items-center justify-between gap-4 text-xs tracking-wider text-muted-foreground">
            <span>BUILDERFORGE — AI GENESIS HACKATHON 2026</span>
            <div className="flex gap-6">
              <a href="#" className="hover:text-foreground">DOCUMENTATION</a>
              <a href="#" className="hover:text-foreground">GITHUB</a>
              <a href="#" className="hover:text-foreground">OKX.AI</a>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
