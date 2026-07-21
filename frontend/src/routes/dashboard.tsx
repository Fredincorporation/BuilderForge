import { createFileRoute, Link } from "@tanstack/react-router";
import { useProjects } from "../../hooks/useApi";
import { Loader } from "lucide-react";

export const Route = createFileRoute("/dashboard")({
  component: Dashboard,
});

function Dashboard() {
  const { data: projects = [], isLoading, error } = useProjects();

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8">
          <div className="max-w-6xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-foreground">Dashboard</h1>
              <p className="text-muted-foreground mt-2">Manage your BuilderForge projects</p>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mb-8">
              <Link
                to="/new-project"
                className="rounded-md bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground hover:brightness-110 transition"
              >
                + New Project
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
                  <Link
                    key={project.id}
                    to={`/project/${project.id}`}
                    className="group block"
                  >
                    <div className="bg-card border border-border rounded-lg p-6 hover:border-primary/50 hover:bg-card/80 transition">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition">
                            {project.title}
                          </h3>
                          <p className="text-sm text-muted-foreground mt-1">
                            {project.description}
                          </p>
                        </div>
                        <span className="text-xs font-bold uppercase tracking-widest text-primary bg-primary/10 px-3 py-1 rounded">
                          {project.phase}
                        </span>
                      </div>

                      {/* Progress Bar */}
                      <div className="mt-4">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-xs text-muted-foreground">Progress</span>
                          <span className="text-xs font-semibold text-foreground">
                            {Math.round(project.progress * 100)}%
                          </span>
                        </div>
                        <div className="h-2 bg-secondary rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary transition-all duration-300"
                            style={{ width: `${project.progress * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
