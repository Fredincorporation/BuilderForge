import React, { ReactNode } from "react";
import { useWallet } from "../context/WalletContext";
import { Wallet, ShieldAlert, ArrowRight, Loader } from "lucide-react";

export function AuthGuard({ children, pageTitle }: { children: ReactNode; pageTitle: string }) {
  const { isConnected, connecting, connectWallet } = useWallet();

  if (!isConnected) {
    return (
      <div className="flex min-h-[80vh] items-center justify-center p-6 bg-background">
        <div className="max-w-md w-full rounded-2xl border border-primary/30 bg-card p-8 shadow-2xl text-center space-y-6">
          <div className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 border border-primary/30 text-primary shadow-lg shadow-primary/20 mx-auto">
            <Wallet className="h-8 w-8" />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl font-extrabold text-foreground tracking-tight">
              OKX Wallet Required
            </h2>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Connect your OKX Wallet to authenticate and access <span className="font-semibold text-foreground">{pageTitle}</span> services.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-secondary/50 border border-border text-xs text-muted-foreground space-y-1 text-left font-mono">
            <p className="font-bold text-foreground">🔒 Protected ASP Features:</p>
            <p>• Multi-agent execution & project management</p>
            <p>• OKX ecosystem dealflow & grant access</p>
            <p>• On-chain contract deployment & simulation</p>
          </div>

          <button
            onClick={connectWallet}
            disabled={connecting}
            className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-6 py-3.5 text-sm font-bold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20"
          >
            {connecting ? <Loader className="h-4 w-4 animate-spin" /> : <Wallet className="h-4 w-4" />}
            <span>Connect OKX Wallet</span>
            <ArrowRight className="h-4 w-4 ml-1" />
          </button>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
