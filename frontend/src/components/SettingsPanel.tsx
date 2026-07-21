'use client';

import React, { useState } from "react";

export default function SettingsPanel() {
  const [open, setOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [simulateMode, setSimulateMode] = useState(true);

  // Dynamic import to avoid SSR issues
  const [Icons, setIcons] = useState<any>(null);

  React.useEffect(() => {
    import("lucide-react").then(setIcons);
  }, []);

  if (!Icons) return null;

  const { Gear, Settings, Sun, Moon, Zap } = Icons;

  return (
    <>
      {/* Floating button clipped at bottom-left (over sidebar) */}
      <div className="fixed left-6 bottom-6 z-50 md:left-72">
        <button
          onClick={() => setOpen((v) => !v)}
          aria-label="Open settings"
          className="inline-flex items-center gap-2 rounded-full bg-card/80 border border-border px-3 py-2 shadow-lg backdrop-blur hover:brightness-105 transition"
        >
          <Gear className="h-4 w-4 text-primary" />
          <span className="hidden sm:inline text-sm font-medium text-foreground">Settings</span>
        </button>
      </div>

      {/* Bottom-clipped panel */}
      <div
        className={`fixed left-0 right-0 bottom-0 z-40 flex justify-center pointer-events-none ${
          open ? "" : ""
        }`}
      >
        <div
          className={`pointer-events-auto max-w-3xl w-full mx-4 mb-4 rounded-t-2xl border border-border bg-card/95 shadow-2xl transition-transform transform ${
            open ? "translate-y-0" : "translate-y-96"
          }`}
          style={{
            backdropFilter: "blur(8px)",
            WebkitBackdropFilter: "blur(8px)",
          }}
        >
          <div className="px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-md bg-primary/10 p-2">
                <Settings className="h-5 w-5 text-primary" />
              </div>
              <div>
                <div className="text-sm font-semibold text-foreground">Settings</div>
                <div className="text-xs text-muted-foreground">App preferences and quick toggles</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setOpen(false)}
                className="text-sm text-muted-foreground hover:text-foreground transition"
              >
                Close
              </button>
            </div>
          </div>

          <div className="border-t border-border px-6 py-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex flex-col gap-2">
              <div className="text-xs font-semibold text-muted-foreground">Theme</div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setDarkMode(false)}
                  className={`rounded-md px-3 py-2 border ${!darkMode ? "border-primary bg-primary/10" : "border-border"}`}
                >
                  <Sun className="h-4 w-4 mr-2 inline" /> Light
                </button>
                <button
                  onClick={() => setDarkMode(true)}
                  className={`rounded-md px-3 py-2 border ${darkMode ? "border-primary bg-primary/10" : "border-border"}`}
                >
                  <Moon className="h-4 w-4 mr-2 inline" /> Dark
                </button>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <div className="text-xs font-semibold text-muted-foreground">Mode</div>
              <div className="flex items-center gap-2">
                <label className="inline-flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={simulateMode}
                    onChange={(e) => setSimulateMode(e.target.checked)}
                    className="form-checkbox h-4 w-4 rounded"
                  />
                  <span className="text-sm">Simulated Mode</span>
                </label>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <div className="text-xs font-semibold text-muted-foreground">Quick Actions</div>
              <div className="flex flex-wrap gap-2">
                <button className="rounded-md border border-border px-3 py-2 text-sm hover:border-primary transition inline-flex items-center gap-2">
                  <Zap className="h-4 w-4 text-primary" /> Run Diagnostics
                </button>
                <button className="rounded-md border border-border px-3 py-2 text-sm hover:border-primary transition">Clear Cache</button>
              </div>
            </div>
          </div>

          <div className="px-6 py-4 border-t border-border text-xs text-muted-foreground">
            Changes are local to this browser session.
          </div>
        </div>
      </div>
    </>
  );
}
