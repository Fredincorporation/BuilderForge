import { createFileRoute, Link } from "@tanstack/react-router";
import { AnimatedMapBackground } from "../components/AnimatedMapBackground";
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
  Wallet,
  Loader,
} from "lucide-react";
import { useWallet } from "../context/WalletContext";

export const Route = createFileRoute("/")({
  component: Index,
});

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
  { icon: BarChart3, label: "FASTAPI" },
  { icon: Zap, label: "CLAUDE" },
  { icon: LayoutGrid, label: "OKX WEB3" },
];

function Index() {
  const { isConnected, connecting, connectWallet } = useWallet();

  return (
    <main className="flex-1 flex flex-col">
      <section className="relative flex-1 px-6 py-16 md:py-24 overflow-hidden border-b border-border/50">
        <AnimatedMapBackground />
        <div className="relative z-10 mx-auto max-w-5xl text-center">
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
            {!isConnected ? (
              <button
                onClick={connectWallet}
                disabled={connecting}
                className="rounded-md bg-primary px-8 py-3.5 text-sm font-bold text-primary-foreground shadow-lg shadow-primary/30 hover:brightness-110 transition flex items-center gap-2"
              >
                {connecting ? <Loader className="h-4 w-4 animate-spin" /> : <Wallet className="h-4 w-4" />}
                Connect OKX Wallet to Begin
              </button>
            ) : (
              <>
                <Link
                  to="/new-project"
                  className="rounded-md bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground shadow-lg shadow-primary/30 hover:brightness-110 transition"
                >
                  Start New Project
                </Link>
                <Link
                  to="/dashboard"
                  className="rounded-md border border-border bg-card/50 px-6 py-3 text-sm font-semibold text-foreground hover:bg-card transition"
                >
                  View Dashboard
                </Link>
              </>
            )}
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
  );
}
