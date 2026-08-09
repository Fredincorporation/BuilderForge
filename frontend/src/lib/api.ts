/**
 * BuilderForge API Client
 * 
 * Typed fetch wrapper for calling FastAPI backend endpoints.
 */

function getApiBaseUrl(): string {
  try {
    if (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL) {
      return import.meta.env.VITE_API_URL as string;
    }
  } catch {}
  try {
    if (typeof process !== "undefined" && process.env?.REACT_APP_API_URL) {
      return process.env.REACT_APP_API_URL as string;
    }
  } catch {}

  // Default to live Render backend origin for deployed frontend if no env variable is configured.
  const defaultRemoteOrigin = "https://builderforge.onrender.com";

  if (typeof window !== "undefined") {
    const origin = window.location.origin;
    const isLocalhost = /localhost|127\.0\.0\.1/.test(origin);
    return isLocalhost ? "http://localhost:8000" : defaultRemoteOrigin;
  }

  return defaultRemoteOrigin;
}

export const API_BASE_URL = getApiBaseUrl();

export interface ApiResponse<T = unknown> {
  status: string;
  data?: T;
  error?: string;
  detail?: string;
  message?: string;
}

export interface Project {
  id: string;
  title: string;
  description: string;
  phase: string;
  progress: number;
  category?: string;
  created_at?: string;
  opportunity_report?: any;
  launch_assets?: any;
  deployment_plan?: any;
  metrics_report?: any;
  logs?: string[];
}

export interface CrewTask {
  task_id: string;
  project_id: string;
  phase: string;
  status: "running" | "completed" | "cancelled" | "error";
  progress: number;
  created_at: string;
}

export interface Wallet {
  address: string;
  chain: string;
  connected: boolean;
  balance?: number;
  connected_at?: string;
}

export interface Deal {
  id: string;
  title: string;
  description: string;
  status: "active" | "upcoming" | "closed";
  funding_stage: string;
  category?: string;
  match_score?: number;
  tags: string[];
  why_it_matches?: string;
  recommended_action?: string;
  apply_url?: string;
  project_id?: string;
}

export interface Launch {
  id: string;
  title: string;
  description: string;
  launch_date: string;
  status: "upcoming" | "live" | "completed";
  category: string;
  tags: string[];
}

/**
 * Generic API request handler with error handling
 */
async function apiCall<T = unknown>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Ensure we always call the backend under the /api prefix regardless of how API_BASE_URL was set.
  const base = API_BASE_URL.replace(/\/$/, "");
  const ep = endpoint.startsWith("/api") ? endpoint : `/api${endpoint}`;
  const url = `${base}${ep}`;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      error: `HTTP ${response.status}`,
    }));
    throw new Error(error.detail || error.error || error.message || "API request failed");
  }

  return response.json() as Promise<T>;
}

/**
 * Project endpoints
 */
export const projectsApi = {
  create: (data: { title: string; description: string; category?: string }) =>
    apiCall<{ status: string; project: Project }>("/projects", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  run: (projectId: string) =>
    apiCall<{ status: string; project_id: string; message: string }>(`/projects/${projectId}/run`, {
      method: "POST",
    }),

  list: () =>
    apiCall<{ projects: Project[]; count: number }>("/projects", {
      method: "GET",
    }),

  get: (id: string) =>
    apiCall<{ status: string; project: Project }>(`/projects/${id}`, {
      method: "GET",
    }),

  logs: (id: string) =>
    apiCall<{ status: string; project_id: string; progress: number; phase: string; logs: string[] }>(`/projects/${id}/logs`, {
      method: "GET",
    }),

  update: (id: string, data: Partial<Project>) =>
    apiCall<{ status: string; project: Project }>(`/projects/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    apiCall<{ status: string; message: string }>(`/projects/${id}`, {
      method: "DELETE",
    }),

  getExportUrl: (id: string) => `${API_BASE_URL}/projects/${id}/export`,
};

/**
 * Crew execution endpoints
 */
export const crewApi = {
  run: (projectId: string, phase?: string) =>
    apiCall<{ task_id: string; message: string }>("/crew/run", {
      method: "POST",
      body: JSON.stringify({ project_id: projectId, phase }),
    }),

  status: (taskId: string) =>
    apiCall<{ task: CrewTask; result?: unknown }>(`/crew/${taskId}`, {
      method: "GET",
    }),

  logs: (taskId: string, limit?: number) =>
    apiCall<{ logs: string[]; log_count: number }>(`/crew/${taskId}/logs`, {
      method: "GET",
      ...((limit !== undefined) && {
        body: JSON.stringify({ limit }),
      }),
    }),

  cancel: (taskId: string) =>
    apiCall<{ message: string }>(`/crew/${taskId}/cancel`, {
      method: "POST",
    }),
};

/**
 * Wallet endpoints
 */
export const walletApi = {
  connect: (address: string, chain?: string) =>
    apiCall<{ wallet: Wallet; message: string }>("/wallet/connect", {
      method: "POST",
      body: JSON.stringify({ address, chain }),
    }),

  get: () =>
    apiCall<{ wallet?: Wallet; connected: boolean }>("/wallet", {
      method: "GET",
    }),

  disconnect: () =>
    apiCall<{ message: string }>("/wallet/disconnect", {
      method: "POST",
    }),

  simulate: (to: string, value: string, data?: string) =>
    apiCall<{ simulation: any }>("/wallet/simulate", {
      method: "POST",
      body: JSON.stringify({ to, value, data }),
    }),

  estimateGas: (to?: string, value?: string) => {
    const params = new URLSearchParams();
    if (to) params.set("to", to);
    if (value) params.set("value", value);
    return apiCall<{ estimate: any }>(`/wallet/gas-estimate?${params}`, {
      method: "GET",
    });
  },
};

/**
 * DealFlow endpoints
 */
export const dealflowApi = {
  list: (statusFilter?: string) => {
    const params = new URLSearchParams();
    if (statusFilter) params.set("status_filter", statusFilter);
    return apiCall<{ deals: Deal[]; count: number }>(`/dealflow?${params}`, {
      method: "GET",
    });
  },

  get: (id: string) =>
    apiCall<{ deal: Deal }>(`/dealflow/${id}`, {
      method: "GET",
    }),

  discover: (query?: string) =>
    apiCall<{ status: string; discovered_count: number; deals: Deal[] }>("/dealflow/discover", {
      method: "POST",
      body: JSON.stringify({ query }),
    }),
};

/**
 * LaunchPad endpoints
 */
export const launchpadApi = {
  list: (statusFilter?: string) => {
    const params = new URLSearchParams();
    if (statusFilter) params.set("status_filter", statusFilter);
    return apiCall<{ launches: Launch[]; count: number }>(`/launchpad?${params}`, {
      method: "GET",
    });
  },

  get: (id: string) =>
    apiCall<{ launch: Launch }>(`/launchpad/${id}`, {
      method: "GET",
    }),

  simulate: (payload: { project_id?: string; title?: string; token_symbol?: string; wallet_address?: string }) =>
    apiCall<{ status: string; simulation: any }>("/launchpad/simulate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};

export const aspApi = {
  getManifest: () =>
    apiCall<{ status: string; manifest: any }>("/asp/manifest", {
      method: "GET",
    }),

  validate: (manifest: any) =>
    apiCall<{ valid: boolean; status: string; message?: string; errors?: string[] }>("/asp/validate", {
      method: "POST",
      body: JSON.stringify({ manifest }),
    }),

  getPricing: () =>
    apiCall<{ status: string; pricing_models: any[] }>("/asp/pricing", {
      method: "GET",
    }),

  submit: (manifest: any) =>
    apiCall<{ status: string; submission_id: string; message: string; marketplace_url: string }>("/asp/submit", {
      method: "POST",
      body: JSON.stringify({ manifest }),
    }),
};

/**
 * Health check
 */
export const healthCheck = () =>
  apiCall<{ status: string; service: string }>("/health", {
    method: "GET",
  });

export default {
  projectsApi,
  crewApi,
  walletApi,
  dealflowApi,
  launchpadApi,
  aspApi,
  healthCheck,
};
