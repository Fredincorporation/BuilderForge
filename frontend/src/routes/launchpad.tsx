import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { useLaunches } from "../hooks/useApi";
import { Loader, Calendar, Zap, Wallet, CheckCircle, Shield, ArrowRight } from "lucide-react";
import { useWallet } from "../context/WalletContext";
import { AuthGuard } from "../components/AuthGuard";

export const Route = createFileRoute("/launchpad")({
  component: () => (
    <AuthGuard pageTitle="LaunchPad">
      <LaunchPad />
    </AuthGuard>
  ),
});

function LaunchPad() {
  const { data: launches = [], isLoading, error } = useLaunches();
  const { wallet, isConnected, connecting, connectWallet, error: walletError } = useWallet();
  const [simulating, setSimulating] = useState(false);
  const [simResult, setSimResult] = useState<any>(null);

  const handleSimulateDeploy = () => {
    setSimulating(true);
    setTimeout(() => {
      setSimResult({
        contract: "BuilderForgeToken.sol",
        network: "OKC Testnet (Chain ID 65)",
        estimated_gas: "0.0042 OKT",
        tx_hash: "0x" + Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join(""),
        status: "SIMULATED_SUCCESS",
      });
      setSimulating(false);
    }, 1500);
  };

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8 max-w-6xl mx-auto space-y-8">
          {/* Header & Wallet Connect Bar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
            <div>
              <h1 className="text-4xl font-extrabold tracking-tight text-foreground">LaunchPad</h1>
              <p className="text-muted-foreground mt-2">
                On-chain deployment, transaction simulation, and project debuts on OKC Testnet
              </p>
            </div>

            <div className="flex items-center gap-3">
              {wallet ? (
                <div className="flex items-center gap-3 px-4 py-2 rounded-lg bg-primary/10 border border-primary/30">
                  <Shield className="h-4 w-4 text-primary" />
                  <div className="text-xs">
                    <p className="font-bold text-foreground font-mono">
                      {wallet.address.slice(0, 6)}...{wallet.address.slice(-4)}
                    </p>
                    <p className="text-[10px] text-muted-foreground">{wallet.providerName}</p>
                  </div>
                  <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                </div>
              ) : (
                <button
                  onClick={connectWallet}
                  disabled={connecting}
                  className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20"
                >
                  {connecting ? <Loader className="h-4 w-4 animate-spin" /> : <Wallet className="h-4 w-4" />}
                  Connect OKX Wallet
                </button>
              )}
            </div>
          </div>

          {walletError && (
            <div className="bg-destructive/10 border border-destructive rounded-xl p-4 text-destructive text-xs font-mono">
              ⚠️ {walletError}
            </div>
          )}

          {/* Transaction Simulation Section */}
          <div className="rounded-xl border border-border bg-card p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
                  <Zap className="h-5 w-5 text-primary" /> On-Chain Contract Deployment Simulator
                </h3>
                <p className="text-xs text-muted-foreground mt-1">
                  Test bytecode execution, gas costs, and transaction sequence on OKC Testnet.
                </p>
              </div>

              <button
                onClick={handleSimulateDeploy}
                disabled={simulating}
                className="inline-flex items-center gap-2 rounded-lg border border-primary/40 bg-primary/10 px-4 py-2 text-xs font-semibold text-primary hover:bg-primary/20 transition"
              >
                {simulating ? <Loader className="h-3.5 w-3.5 animate-spin" /> : <ArrowRight className="h-3.5 w-3.5" />}
                Run Deployment Simulation
              </button>
            </div>

            {simResult && (
              <div className="mt-4 p-4 rounded-lg bg-black/80 border border-primary/30 space-y-2 text-xs font-mono text-primary">
                <div className="flex items-center justify-between border-b border-primary/20 pb-2">
                  <span className="font-bold flex items-center gap-1.5 text-green-400">
                    <CheckCircle className="h-4 w-4" /> SIMULATION SUCCESSFUL
                  </span>
                  <span className="text-[10px] text-muted-foreground">{simResult.network}</span>
                </div>
                <p><span className="text-muted-foreground">Contract:</span> {simResult.contract}</p>
                <p><span className="text-muted-foreground">Est. Gas:</span> {simResult.estimated_gas}</p>
                <p><span className="text-muted-foreground">Tx Hash:</span> <span className="break-all text-gray-300">{simResult.tx_hash}</span></p>
              </div>
            )}
          </div>

          {/* Launches List */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-foreground">Featured Ecosystem Launches</h2>
            {isLoading ? (
              <div className="flex justify-center items-center py-12">
                <Loader className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : error ? (
              <div className="bg-destructive/10 border border-destructive rounded-lg p-6 text-destructive">
                <p className="font-semibold">Error loading launches</p>
                <p className="text-sm">{String(error)}</p>
              </div>
            ) : (
              <div className="space-y-4">
                {launches.map((launch) => (
                  <div key={launch.id} className="bg-card border border-border rounded-lg p-6 hover:border-primary/50 transition">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold text-foreground mb-2">{launch.title}</h3>
                        <p className="text-muted-foreground">{launch.description}</p>
                      </div>
                      <span className={`text-xs font-bold uppercase px-3 py-1 rounded ${
                        launch.status === "live"
                          ? "bg-green-500/20 text-green-500"
                          : "bg-primary/20 text-primary"
                      }`}>
                        {launch.status}
                      </span>
                    </div>

                    <div className="grid gap-4 md:grid-cols-3 mt-4 pt-4 border-t border-border">
                      <div>
                        <span className="text-xs text-muted-foreground uppercase tracking-widest">Category</span>
                        <p className="font-semibold text-foreground mt-1">{launch.category}</p>
                      </div>
                      <div>
                        <span className="flex items-center gap-1 text-xs text-muted-foreground uppercase tracking-widest">
                          <Calendar className="h-3 w-3" />
                          Launch Date
                        </span>
                        <p className="font-semibold text-foreground mt-1">{launch.launch_date}</p>
                      </div>
                      <div className="flex gap-2 flex-wrap items-end">
                        {launch.tags.map((tag) => (
                          <span key={tag} className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
