import React, { useState } from "react";
import { Link, useLocation } from "@tanstack/react-router";
import {
  Hammer,
  Home,
  Plus,
  LayoutGrid,
  Briefcase,
  Rocket,
  Circle,
  Settings,
  ShieldCheck,
} from "lucide-react";
import SettingsPanel from "./SettingsPanel";
import { useWallet } from "../context/WalletContext";

const navItems = [
  { icon: Home, label: "Home", href: "/" },
  { icon: Plus, label: "New", href: "/new-project" },
  { icon: LayoutGrid, label: "Dashboard", href: "/dashboard" },
  { icon: Briefcase, label: "DealFlow", href: "/dealflow" },
  { icon: Rocket, label: "LaunchPad", href: "/launchpad" },
  { icon: ShieldCheck, label: "ASP Listing", href: "/asp-listing" },
];

export function AppSidebar() {
  const location = useLocation();
  const [settingsOpen, setSettingsOpen] = useState(false);
  const { isConnected } = useWallet();

  // If no wallet is connected, only show Home in the navigation
  const visibleNavItems = isConnected
    ? navItems
    : navItems.filter((item) => item.href === "/");

  const isActive = (href: string) => {
    if (href === "/") {
      return location.pathname === "/";
    }
    return location.pathname.startsWith(href);
  };

  return (
    <>
      {/* ========================================================================= */}
      {/* DESKTOP SIDEBAR (Visible on md screens and larger)                       */}
      {/* ========================================================================= */}
      <aside className="hidden md:flex flex-col w-64 shrink-0 border-r border-border bg-[var(--sidebar-bg)] min-h-screen">
        <div className="flex items-center gap-3 px-6 pt-6 pb-8">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground shadow-md shadow-primary/20">
            <Hammer className="h-5 w-5" />
          </div>
          <span className="text-xl font-bold tracking-tight text-foreground">BuilderForge</span>
        </div>

        <div className="px-6 text-[10px] font-semibold tracking-[0.2em] text-muted-foreground uppercase">
          NAVIGATION
        </div>

        <nav className="mt-3 flex flex-col gap-1 px-3">
          {visibleNavItems.map(({ icon: Icon, label, href }) => {
            const active = isActive(href);
            return (
              <Link
                key={label}
                to={href}
                className={`flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors ${
                  active
                    ? "bg-primary/15 text-primary border-l-2 border-primary pl-2.5 font-semibold"
                    : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                }`}
              >
                <Icon className={`h-4 w-4 ${active ? "text-primary" : ""}`} />
                <span>{label === "New" ? "New Project" : label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Bottom Section: Settings Trigger + System Online */}
        <div className="mt-auto px-3 pt-3 pb-6 border-t border-border/40 space-y-3">
          {/* Settings Item */}
          <button
            onClick={() => setSettingsOpen(true)}
            className="w-full flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
          >
            <Settings className="h-4 w-4 text-muted-foreground" />
            <span>Settings</span>
          </button>

          {/* System Online Block */}
          <div className="px-3 pt-1 border-t border-border/20">
            <div className="flex items-center gap-2 text-xs">
              <Circle className="h-2 w-2 fill-green-500 text-green-500 animate-pulse" />
              <span className="font-medium tracking-wider text-muted-foreground uppercase">
                SYSTEM ONLINE
              </span>
            </div>
            <div className="mt-1 text-xs text-muted-foreground/70">
              v1.2.4 — OKX Ecosystem
            </div>
          </div>
        </div>
      </aside>

      {/* ========================================================================= */}
      {/* MOBILE BOTTOM NAVBAR (Visible on mobile screens below md)                 */}
      {/* ========================================================================= */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-[var(--sidebar-bg)]/95 backdrop-blur-lg border-t border-border px-2 py-1.5 flex items-center justify-around shadow-2xl">
        {visibleNavItems.map(({ icon: Icon, label, href }) => {
          const active = isActive(href);
          return (
            <Link
              key={label}
              to={href}
              className={`flex flex-col items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium transition-colors ${
                active ? "text-primary font-bold" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Icon className={`h-5 w-5 ${active ? "text-primary scale-110" : ""}`} />
              <span>{label}</span>
            </Link>
          );
        })}

        {/* Mobile Settings Tab Item */}
        <button
          onClick={() => setSettingsOpen(true)}
          className="flex flex-col items-center gap-1 px-2 py-1 rounded-md text-[11px] font-medium text-muted-foreground hover:text-foreground transition-colors"
        >
          <Settings className="h-5 w-5" />
          <span>Settings</span>
        </button>
      </nav>

      {/* Settings Modal Panel */}
      <SettingsPanel open={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </>
  );
}
