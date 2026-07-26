import React from "react";
import { useWallet } from "../context/WalletContext";
import { Wallet, LogOut, Loader, Shield, CheckCircle } from "lucide-react";

export function Header() {
  const { wallet, isConnected, connecting, connectWallet, disconnectWallet } = useWallet();

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-border/60 bg-background/85 px-6 backdrop-blur-md">
      {/* Brand Label on top bar */}
      <div className="flex items-center gap-2 md:hidden">
        <img
          src="/builderforge-logo.png"
          alt="BuilderForge logo"
          className="h-8 w-8 rounded-md border border-border/20 bg-white/5 object-contain"
        />
        <span className="text-lg font-bold tracking-tight text-foreground">BuilderForge</span>
      </div>
      <div className="hidden md:block">
        <span className="text-xs font-mono tracking-widest text-muted-foreground uppercase">
          OKX AGENTIC SERVICE PROVIDER (ASP)
        </span>
      </div>

      {/* Top Right: Connect OKX Wallet / Account Badge */}
      <div className="flex items-center gap-3">
        {isConnected && wallet ? (
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2.5 px-3.5 py-1.5 rounded-lg bg-primary/10 border border-primary/30">
              <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <div className="text-xs">
                <span className="font-bold text-foreground font-mono">
                  {wallet.address.slice(0, 6)}...{wallet.address.slice(-4)}
                </span>
              </div>
              <span className="text-[10px] bg-primary/20 text-primary px-1.5 py-0.5 rounded font-semibold hidden sm:inline-block">
                {wallet.providerName.includes("OKX") ? "OKX Wallet" : "Web3"}
              </span>
            </div>

            <button
              onClick={disconnectWallet}
              className="p-2 rounded-lg border border-border text-muted-foreground hover:text-foreground hover:bg-secondary transition"
              title="Disconnect Wallet"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        ) : (
          <button
            onClick={connectWallet}
            disabled={connecting}
            className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-xs font-bold text-primary-foreground hover:brightness-110 transition shadow-md shadow-primary/20"
          >
            {connecting ? <Loader className="h-3.5 w-3.5 animate-spin" /> : <Wallet className="h-3.5 w-3.5" />}
            <span>Connect OKX Wallet</span>
          </button>
        )}
      </div>
    </header>
  );
}
