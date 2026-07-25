import { createFileRoute, Link } from "@tanstack/react-router";
import { useProjects } from "../hooks/useApi";
import { Loader, Download, Plus } from "lucide-react";

import { AuthGuard } from "../components/AuthGuard";

export const Route = createFileRoute("/dashboard")({
  component: () => (
    <AuthGuard pageTitle="Dashboard">
      <Dashboard />
    </AuthGuard>
  ),
});

function Dashboard() {
  const { data: projects = [], isLoading, error } = useProjects();

  const handleExportZip = (projectId: string, projectTitle: string) => {
    const apiUrl = process.env.REACT_APP_API_URL || "http://localhost:8000/api";
    const downloadUrl = `${apiUrl}/projects/${projectId}/export`;
    
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = `builderforge_${projectTitle.toLowerCase().replace(/\s+/g, "_")}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-foreground">Dashboard</h1>
              <p className="text-muted-foreground mt-2">Manage and export your BuilderForge ASP projects</p>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mb-8">
              <Link
                to="/new-project"
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground hover:brightness-110 transition shadow-lg shadow-primary/20"
              >
                <Plus className="h-4 w-4" /> New Project
              </Link>
            </div>

            {/* Projects List */}
            {isLoading ? (
              <div className="flex justify-center items-center py-12">
                <Loader className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : error ? (
              <div className="bg-destructive/10 border border-destructive rounded-lg p-6 text-destructive">
                <p className="font-semibold">Error loading projects</p>
                <p className="text-sm">{String(error)}</p>
              </div>
            ) : projects.length === 0 ? (
              <div className="text-center py-12 bg-card rounded-lg border border-border">
                <p className="text-muted-foreground mb-4">No projects yet</p>
                <Link
                  to="/new-project"
                  className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
                >
                  Create your first project
                </Link>
              </div>
            ) : (
              <div className="grid gap-6">
                {projects.map((project) => (
                  <div
                    key={project.id}
                    className="bg-card border border-border rounded-xl p-6 hover:border-primary/50 transition flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-xl font-bold text-foreground hover:text-primary transition">
                            {project.title}
                          </h3>
                          <p className="text-sm text-muted-foreground mt-1">
                            {project.description}
                          </p>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="text-xs font-bold uppercase tracking-widest text-primary bg-primary/10 px-3 py-1 rounded-md border border-primary/20">
                            {project.phase}
                          </span>
                          <button
                            onClick={() => handleExportZip(project.id, project.title)}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border bg-secondary/60 text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground hover:border-primary transition"
                            title="Export ZIP package with contract, pitch deck, and ASP manifest"
                          >
                            <Download className="h-3.5 w-3.5" />
                            Export ZIP
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="mt-4 pt-4 border-t border-border/50">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-xs font-medium text-muted-foreground">Pipeline Execution</span>
                        <span className="text-xs font-bold font-mono text-primary">
                          {Math.round(project.progress * 100)}%
                        </span>
                      </div>
                      <div className="h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary transition-all duration-300 shadow-sm shadow-primary"
                          style={{ width: `${project.progress * 100}%` }}
                        />
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
