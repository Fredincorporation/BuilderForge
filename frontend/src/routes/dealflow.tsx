import { createFileRoute } from "@tanstack/react-router";
import { useDeals } from "../hooks/useApi";
import { Loader } from "lucide-react";

import { AuthGuard } from "../components/AuthGuard";

export const Route = createFileRoute("/dealflow")({
  component: () => (
    <AuthGuard pageTitle="DealFlow">
      <DealFlow />
    </AuthGuard>
  ),
});

function DealFlow() {
  const { data: deals = [], isLoading, error } = useDeals("active");

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-foreground">DealFlow</h1>
              <p className="text-muted-foreground mt-2">
                Discover active opportunities in the OKX ecosystem
              </p>
            </div>

            {/* Deals Grid */}
            {isLoading ? (
              <div className="flex justify-center items-center py-12">
                <Loader className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : error ? (
              <div className="bg-destructive/10 border border-destructive rounded-lg p-6 text-destructive">
                <p className="font-semibold">Error loading deals</p>
                <p className="text-sm">{String(error)}</p>
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {deals.map((deal) => (
                  <div key={deal.id} className="bg-card border border-border rounded-lg p-6 hover:border-primary/50 transition">
                    <h3 className="text-lg font-semibold text-foreground mb-2">{deal.title}</h3>
                    <p className="text-sm text-muted-foreground mb-4">{deal.description}</p>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Status</span>
                        <span className="font-semibold text-primary">{deal.status.toUpperCase()}</span>
                      </div>
                      <div className="flex justify-between items-center text-sm">
                        <span className="text-muted-foreground">Funding Stage</span>
                        <span className="font-semibold">{deal.funding_stage}</span>
                      </div>
                    </div>

                    {/* Tags */}
                    <div className="mt-4 flex flex-wrap gap-2">
                      {deal.tags.map((tag) => (
                        <span key={tag} className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>

                    <button className="w-full mt-4 rounded-md bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:brightness-110 transition">
                      Learn More
                    </button>
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
