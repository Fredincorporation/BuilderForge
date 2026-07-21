import { createFileRoute } from "@tanstack/react-router";
import { useLaunches } from "../../hooks/useApi";
import { Loader, Calendar, Zap } from "lucide-react";

export const Route = createFileRoute("/launchpad")({
  component: LaunchPad,
});

function LaunchPad() {
  const { data: launches = [], isLoading, error } = useLaunches();

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-foreground">LaunchPad</h1>
              <p className="text-muted-foreground mt-2">
                Upcoming launches and project debuts on OKX
              </p>
            </div>

            {/* Launches List */}
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

                    <button className="mt-4 rounded-md bg-primary px-6 py-2 text-sm font-semibold text-primary-foreground hover:brightness-110 transition flex items-center gap-2">
                      <Zap className="h-4 w-4" />
                      Get Notified
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
