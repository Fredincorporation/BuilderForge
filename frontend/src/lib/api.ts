/**
 * BuilderForge API Client
 * 
 * Typed fetch wrapper for calling FastAPI backend endpoints.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

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
  status: "active" | "closed";
  funding_stage: string;
  tags: string[];
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
  const url = `${API_BASE_URL}${endpoint}`;
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
    apiCall<{ project: Project }>("/projects", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  list: () =>
    apiCall<{ projects: Project[]; count: number }>("/projects", {
      method: "GET",
    }),

  get: (id: string) =>
    apiCall<{ project: Project }>(`/projects/${id}`, {
      method: "GET",
    }),

  update: (id: string, data: Partial<Project>) =>
    apiCall<{ project: Project }>(`/projects/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    apiCall<{ message: string }>(`/projects/${id}`, {
      method: "DELETE",
    }),
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
  healthCheck,
};
