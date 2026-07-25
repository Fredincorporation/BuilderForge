import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { connectWeb3Wallet, Web3WalletState } from "../lib/web3";

interface WalletContextType {
  wallet: Web3WalletState | null;
  isConnected: boolean;
  connecting: boolean;
  error: string | null;
  connectWallet: () => Promise<void>;
  disconnectWallet: () => void;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

const STORAGE_KEY = "builderforge_wallet_state";

export function WalletProvider({ children }: { children: ReactNode }) {
  const [wallet, setWallet] = useState<Web3WalletState | null>(null);
  const [mounted, setMounted] = useState<boolean>(false);
  const [connecting, setConnecting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Hydrate wallet state on client mount only to prevent SSR hydration mismatch
  useEffect(() => {
    setMounted(true);
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        try {
          setWallet(JSON.parse(saved));
        } catch (e) {
          localStorage.removeItem(STORAGE_KEY);
        }
      }
    }
  }, []);

  // Sync wallet changes to localStorage after mounting
  useEffect(() => {
    if (!mounted) return;
    if (wallet) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(wallet));
    } else {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, [wallet, mounted]);

  const connectWallet = async () => {
    setConnecting(true);
    setError(null);
    try {
      const state = await connectWeb3Wallet();
      setWallet(state);
    } catch (err: any) {
      console.error("Wallet connection failed", err);
      setError(err.message || "Failed to connect wallet");
    } finally {
      setConnecting(false);
    }
  };

  const disconnectWallet = () => {
    setWallet(null);
    if (typeof window !== "undefined") {
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  return (
    <WalletContext.Provider
      value={{
        wallet,
        isConnected: Boolean(mounted && wallet && wallet.connected),
        connecting,
        error,
        connectWallet,
        disconnectWallet,
      }}
    >
      {children}
    </WalletContext.Provider>
  );
}

export function useWallet() {
  const context = useContext(WalletContext);
  if (!context) {
    throw new Error("useWallet must be used within a WalletProvider");
  }
  return context;
}
