import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { useCreateProject, useRunPipeline, useProject, useProjectLogs } from "../hooks/useApi";
import { Loader, Sparkles, Rocket, Zap } from "lucide-react";
import { AuthGuard } from "../components/AuthGuard";
import { PipelineModal } from "../components/PipelineModal";

export const Route = createFileRoute("/new-project")({
  component: () => (
    <AuthGuard pageTitle="New Project">
      <NewProject />
    </AuthGuard>
  ),
});

function NewProject() {
  const navigate = useNavigate();
  const createProject = useCreateProject();
  const runPipeline = useRunPipeline();

  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);
  const [isPipelineOpen, setIsPipelineOpen] = useState(false);

  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "General",
  });

  // Query project status & logs when pipeline is running
  const { data: project } = useProject(activeProjectId || undefined);
  const { data: logsData } = useProjectLogs(activeProjectId || undefined, isPipelineOpen);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleStartPipeline = async (title: string, description: string, category: string) => {
    try {
      const newProj = await createProject.mutateAsync({ title, description, category });
      setActiveProjectId(newProj.id);
      setIsPipelineOpen(true);
      
      // Start background pipeline
      await runPipeline.mutateAsync(newProj.id);
    } catch (error) {
      console.error("Error launching project pipeline:", error);
      alert(`Failed to launch project: ${error}`);
    }
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!formData.title.trim() || !formData.description.trim()) {
      alert("Please fill in all required fields");
      return;
    }
    handleStartPipeline(formData.title, formData.description, formData.category);
  };

  const handleFillDemo = () => {
    const demoTitle = "DeAI Compute DAO";
    const demoDesc = "Decentralized AI compute marketplace on OKX X Layer connecting idle GPU providers with AI developers using autonomous agent job matching.";
    const demoCat = "DeAI Infrastructure";
    
    setFormData({
      title: demoTitle,
      description: demoDesc,
      category: demoCat,
    });
    
    handleStartPipeline(demoTitle, demoDesc, demoCat);
  };

  const handlePipelineComplete = () => {
    setIsPipelineOpen(false);
    if (activeProjectId) {
      navigate({ to: "/dashboard", search: { project_id: activeProjectId } as any });
    } else {
      navigate({ to: "/dashboard" });
    }
  };

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8">
          <div className="max-w-2xl mx-auto space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-4xl font-bold text-foreground flex items-center gap-3">
                  <Rocket className="h-8 w-8 text-primary" />
                  Create New Project
                </h1>
                <p className="text-muted-foreground mt-2">
                  Launch an autonomous Web3 project with BuilderForge multi-agent crew
                </p>
              </div>

              {/* Fast Demo Run Button */}
              <button
                type="button"
                onClick={handleFillDemo}
                disabled={createProject.isPending}
                className="px-4 py-2.5 rounded-lg bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-xs flex items-center gap-2 shadow-lg hover:shadow-purple-500/25 transition-all cursor-pointer"
              >
                <Zap className="h-4 w-4 fill-amber-300 text-amber-300" />
                Run Demo Project (1-Click)
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="bg-card border border-border rounded-xl p-8 space-y-6 shadow-xl">
              {/* Title */}
              <div>
                <label htmlFor="title" className="block text-sm font-semibold text-foreground mb-2">
                  Project Title *
                </label>
                <input
                  id="title"
                  name="title"
                  type="text"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="e.g., DeAI Compute DAO"
                  className="w-full rounded-lg border border-input bg-background px-4 py-2.5 text-foreground placeholder:text-muted-foreground focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none"
                  required
                />
              </div>

              {/* Description */}
              <div>
                <label htmlFor="description" className="block text-sm font-semibold text-foreground mb-2">
                  Project Vision & Description *
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Describe what your Web3 project does, target market, and token utility..."
                  rows={4}
                  className="w-full rounded-lg border border-input bg-background px-4 py-2.5 text-foreground placeholder:text-muted-foreground focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none resize-none"
                  required
                />
              </div>

              {/* Category */}
              <div>
                <label htmlFor="category" className="block text-sm font-semibold text-foreground mb-2">
                  Category
                </label>
                <select
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  className="w-full rounded-lg border border-input bg-background px-4 py-2.5 text-foreground focus:border-primary focus:outline-none"
                >
                  <option value="General">General Web3</option>
                  <option value="DeAI Infrastructure">DeAI & AI Agents</option>
                  <option value="DeFi Protocol">DeFi Protocol</option>
                  <option value="Token Launch">Token Launch</option>
                  <option value="NFT Collection">NFT Collection</option>
                  <option value="DAO Governance">DAO Governance</option>
                </select>
              </div>

              {/* Actions */}
              <div className="flex gap-4 pt-4">
                <button
                  type="submit"
                  disabled={createProject.isPending || runPipeline.isPending}
                  className="flex-1 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground disabled:opacity-50 disabled:cursor-not-allowed hover:brightness-110 transition flex items-center justify-center gap-2 shadow-lg shadow-primary/20"
                >
                  {(createProject.isPending || runPipeline.isPending) ? (
                    <Loader className="h-4 w-4 animate-spin" />
                  ) : (
                    <Sparkles className="h-4 w-4" />
                  )}
                  {createProject.isPending ? "Creating..." : "Launch Multi-Agent Pipeline"}
                </button>
                <button
                  type="button"
                  onClick={() => navigate({ to: "/dashboard" })}
                  className="flex-1 rounded-lg border border-border bg-background px-6 py-3 text-sm font-semibold text-foreground hover:bg-secondary transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>

      {/* Execution Pipeline Modal */}
      <PipelineModal
        isOpen={isPipelineOpen}
        projectTitle={formData.title || "Project Pipeline"}
        progress={project?.progress ?? 0}
        phase={project?.phase ?? "IDEA_INPUT"}
        logs={logsData?.logs ?? []}
        onComplete={handlePipelineComplete}
      />
    </div>
  );
}
