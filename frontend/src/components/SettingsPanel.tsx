'use client';

import React, { useState } from "react";
import { Settings, Sun, Moon, Zap, X } from "lucide-react";

interface SettingsPanelProps {
  open: boolean;
  onClose: () => void;
}

export default function SettingsPanel({ open, onClose }: SettingsPanelProps) {
  const [darkMode, setDarkMode] = useState(true);
  const [simulateMode, setSimulateMode] = useState(true);

  if (!open) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-background/70 backdrop-blur-sm p-4 transition-all"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="max-w-2xl w-full rounded-2xl border border-border bg-card/95 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200"
        style={{
          backdropFilter: "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
        }}
      >
        {/* Header */}
        <div className="px-6 py-4 flex items-center justify-between border-b border-border">
          <div className="flex items-center gap-3">
            <div className="rounded-md bg-primary/10 p-2">
              <Settings className="h-5 w-5 text-primary" />
            </div>
            <div>
              <div className="text-sm font-semibold text-foreground">Settings & Preferences</div>
              <div className="text-xs text-muted-foreground">Configure BuilderForge environment and display settings</div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="rounded-md p-1.5 text-muted-foreground hover:text-foreground hover:bg-secondary transition"
            aria-label="Close settings"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex flex-col gap-2">
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Theme</div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setDarkMode(false)}
                className={`flex-1 rounded-md px-3 py-2 text-xs font-medium border transition ${!darkMode ? "border-primary bg-primary/10 text-primary" : "border-border text-muted-foreground"}`}
              >
                <Sun className="h-3.5 w-3.5 mr-1.5 inline" /> Light
              </button>
              <button
                onClick={() => setDarkMode(true)}
                className={`flex-1 rounded-md px-3 py-2 text-xs font-medium border transition ${darkMode ? "border-primary bg-primary/10 text-primary" : "border-border text-muted-foreground"}`}
              >
                <Moon className="h-3.5 w-3.5 mr-1.5 inline" /> Dark
              </button>
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Execution Mode</div>
            <div className="flex items-center gap-2">
              <label className="inline-flex items-center gap-2 cursor-pointer text-xs font-medium text-foreground">
                <input
                  type="checkbox"
                  checked={simulateMode}
                  onChange={(e) => setSimulateMode(e.target.checked)}
                  className="rounded border-border text-primary focus:ring-primary accent-primary"
                />
                <span>Simulated (No API key)</span>
              </label>
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Quick Actions</div>
            <div className="flex flex-col gap-2">
              <button className="rounded-md border border-border px-3 py-2 text-xs font-medium hover:border-primary transition inline-flex items-center gap-1.5">
                <Zap className="h-3.5 w-3.5 text-primary" /> Run Diagnostics
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-border bg-secondary/30 text-[11px] text-muted-foreground flex justify-between items-center">
          <span>Changes are local to this session</span>
          <button
            onClick={onClose}
            className="rounded-md bg-primary px-3 py-1 text-xs font-semibold text-primary-foreground hover:brightness-110 transition"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
