import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { useCreateProject } from "../hooks/useApi";
import { Loader } from "lucide-react";

import { AuthGuard } from "../components/AuthGuard";

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
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    category: "General",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!formData.title.trim() || !formData.description.trim()) {
      alert("Please fill in all required fields");
      return;
    }

    try {
      await createProject.mutateAsync(formData);
      // Navigate to dashboard on success
      navigate({ to: "/dashboard" });
    } catch (error) {
      console.error("Error creating project:", error);
      alert(`Error creating project: ${error}`);
    }
  };

  return (
    <div className="flex min-h-screen bg-background">
      <main className="flex-1">
        <div className="px-6 py-8">
          <div className="max-w-2xl mx-auto">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-foreground">Create New Project</h1>
              <p className="text-muted-foreground mt-2">
                Start your BuilderForge journey with a new idea
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="bg-card border border-border rounded-lg p-8 space-y-6">
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
                  placeholder="e.g., AI-Powered Token Launcher"
                  className="w-full rounded-lg border border-input bg-background px-4 py-2 text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none"
                  required
                />
              </div>

              {/* Description */}
              <div>
                <label htmlFor="description" className="block text-sm font-semibold text-foreground mb-2">
                  Project Description *
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Describe your project vision and goals..."
                  rows={4}
                  className="w-full rounded-lg border border-input bg-background px-4 py-2 text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none resize-none"
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
                  className="w-full rounded-lg border border-input bg-background px-4 py-2 text-foreground focus:border-primary focus:outline-none"
                >
                  <option>General</option>
                  <option>Token Launch</option>
                  <option>DeFi Protocol</option>
                  <option>NFT Collection</option>
                  <option>DAO Governance</option>
                </select>
              </div>

              {/* Actions */}
              <div className="flex gap-4 pt-4">
                <button
                  type="submit"
                  disabled={createProject.isPending}
                  className="flex-1 rounded-md bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground disabled:opacity-50 disabled:cursor-not-allowed hover:brightness-110 transition flex items-center justify-center gap-2"
                >
                  {createProject.isPending && <Loader className="h-4 w-4 animate-spin" />}
                  {createProject.isPending ? "Creating..." : "Create Project"}
                </button>
                <button
                  type="button"
                  onClick={() => navigate({ to: "/dashboard" })}
                  className="flex-1 rounded-md border border-border bg-background px-6 py-3 text-sm font-semibold text-foreground hover:bg-secondary transition"
                >
                  Cancel
                </button>
              </div>

              {createProject.isError && (
                <div className="bg-destructive/10 border border-destructive rounded-lg p-4 text-destructive text-sm">
                  {String(createProject.error)}
                </div>
              )}
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
