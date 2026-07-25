import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Loader, CheckCircle, Copy, Code, ShieldCheck, DollarSign, Cpu, Check } from "lucide-react";
import { aspApi } from "../lib/api";

import { AuthGuard } from "../components/AuthGuard";

export const Route = createFileRoute("/asp-listing")({
  component: () => (
    <AuthGuard pageTitle="ASP Listing">
      <AspListingPage />
    </AuthGuard>
  ),
});

function AspListingPage() {
  const [manifest, setManifest] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [testResult, setTestResult] = useState<any>(null);
  const [validating, setValidating] = useState(false);

  useEffect(() => {
    aspApi
      .getManifest()
      .then((data) => {
        setManifest(data.manifest);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch manifest", err);
        setLoading(false);
      });
  }, []);

  const handleCopyManifest = () => {
    if (!manifest) return;
    navigator.clipboard.writeText(JSON.stringify(manifest, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleValidate = async () => {
    setValidating(true);
    try {
      const res = await aspApi.validate(manifest);
      setTestResult(res);
    } catch (err: any) {
      setTestResult({ valid: false, errors: [err.message || "Validation failed"] });
    } finally {
      setValidating(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8 max-w-6xl mx-auto space-y-8">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-xs font-semibold text-primary mb-3">
                <ShieldCheck className="h-3.5 w-3.5" /> VERIFIED OKX ASP PROVIDER
              </div>
              <h1 className="text-4xl font-extrabold tracking-tight text-foreground">
                OKX.AI ASP Marketplace Listing
              </h1>
              <p className="text-muted-foreground mt-2 max-w-2xl">
                Configure, validate, and export your Agentic Service Provider (ASP) manifest to list BuilderForge multi-agent execution services on OKX.AI.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={handleCopyManifest}
                className="inline-flex items-center gap-2 rounded-lg border border-border bg-card px-4 py-2.5 text-sm font-semibold text-foreground hover:bg-secondary transition"
              >
                {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
                {copied ? "Copied!" : "Copy Manifest JSON"}
              </button>
              <button
                onClick={handleValidate}
                disabled={validating}
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20"
              >
                {validating ? <Loader className="h-4 w-4 animate-spin" /> : <CheckCircle className="h-4 w-4" />}
                Validate Spec
              </button>
            </div>
          </div>

          {loading ? (
            <div className="flex justify-center items-center py-24">
              <Loader className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : (
            <div className="grid gap-8 lg:grid-cols-3">
              {/* Left Column: Info & Stats */}
              <div className="space-y-6 lg:col-span-1">
                {/* Status Card */}
                <div className="rounded-xl border border-border bg-card p-6 space-y-4">
                  <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-widest flex items-center gap-2">
                    <Cpu className="h-4 w-4 text-primary" /> Active Service Agents
                  </h3>
                  <div className="space-y-2">
                    {manifest?.agents?.map((agent: any) => (
                      <div key={agent.id} className="flex items-center justify-between p-2.5 rounded-md bg-secondary/50 border border-border/50 text-xs font-medium">
                        <span className="font-semibold text-foreground">{agent.name}</span>
                        <span className="text-[10px] bg-green-500/10 text-green-500 px-2 py-0.5 rounded font-mono font-bold">
                          {agent.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Pricing Card */}
                <div className="rounded-xl border border-border bg-card p-6 space-y-4">
                  <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-widest flex items-center gap-2">
                    <DollarSign className="h-4 w-4 text-primary" /> Marketplace Rate Cards
                  </h3>
                  <div className="space-y-3">
                    {manifest?.pricing_models?.map((model: any) => (
                      <div key={model.model_id} className="p-3 rounded-lg border border-primary/20 bg-primary/5 space-y-1">
                        <div className="flex justify-between items-center text-sm font-bold text-foreground">
                          <span>{model.name}</span>
                          <span className="text-primary">{model.price} {model.currency}</span>
                        </div>
                        <p className="text-xs text-muted-foreground">{model.billing_unit}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Validation Banner */}
                {testResult && (
                  <div className={`rounded-xl p-5 border text-sm ${testResult.valid ? "bg-green-500/10 border-green-500 text-green-400" : "bg-destructive/10 border-destructive text-destructive"}`}>
                    <p className="font-bold flex items-center gap-2">
                      {testResult.valid ? <CheckCircle className="h-4 w-4" /> : "Validation Failed"}
                      {testResult.valid ? "Manifest Validated!" : "Errors Found"}
                    </p>
                    <p className="mt-1 text-xs">{testResult.message || testResult.errors?.join(", ")}</p>
                  </div>
                )}
              </div>

              {/* Right Column: Interactive Code Inspector */}
              <div className="lg:col-span-2 rounded-xl border border-border bg-card overflow-hidden flex flex-col">
                <div className="px-6 py-4 border-b border-border bg-secondary/40 flex items-center justify-between">
                  <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                    <Code className="h-4 w-4 text-primary" />
                    <span>asp_manifest.json (OKX Standard v1.0.0)</span>
                  </div>
                  <span className="text-xs font-mono text-muted-foreground">JSON Schema Compliant</span>
                </div>
                <pre className="p-6 text-xs font-mono text-primary bg-black/80 overflow-x-auto leading-relaxed flex-1 max-h-[550px]">
                  {JSON.stringify(manifest, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
