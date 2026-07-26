/**
 * React hooks for BuilderForge API calls
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { 
  projectsApi, 
  crewApi, 
  walletApi, 
  dealflowApi, 
  launchpadApi,
  aspApi,
  type Project,
  type CrewTask,
  type Deal,
  type Launch,
} from "../lib/api";

/**
 * Use projects query
 */
export const useProjects = () => {
  return useQuery({
    queryKey: ["projects"],
    queryFn: () => projectsApi.list().then(res => res.projects || []),
    staleTime: 5 * 1000, // 5 seconds
  });
};

/**
 * Use single project query
 */
export const useProject = (id: string | undefined) => {
  return useQuery({
    queryKey: ["project", id],
    queryFn: () => id ? projectsApi.get(id).then(res => res.project) : null,
    enabled: !!id,
    refetchInterval: (query) => {
      const data = query.state.data as Project | null;
      if (data && (data.phase === "IN_PROGRESS" || data.progress < 1.0)) {
        return 1000; // Poll every second while running
      }
      return false;
    },
  });
};

/**
 * Use create project mutation
 */
export const useCreateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { title: string; description: string; category?: string }) =>
      projectsApi.create(data).then(res => res.project),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
  });
};

/**
 * Use run multi-agent pipeline mutation
 */
export const useRunPipeline = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (projectId: string) =>
      projectsApi.run(projectId),
    onSuccess: (_, projectId) => {
      queryClient.invalidateQueries({ queryKey: ["project", projectId] });
    },
  });
};

/**
 * Use project logs query (with auto polling during pipeline execution)
 */
export const useProjectLogs = (projectId: string | undefined, enabled: boolean = true) => {
  return useQuery({
    queryKey: ["projectLogs", projectId],
    queryFn: () => projectId ? projectsApi.logs(projectId) : null,
    enabled: !!projectId && enabled,
    refetchInterval: 1000, // Poll every 1 second during run
  });
};

/**
 * Use crew run mutation
 */
export const useCrewRun = () => {
  return useMutation({
    mutationFn: (data: { projectId: string; phase?: string }) =>
      crewApi.run(data.projectId, data.phase).then(res => res.task_id),
  });
};

/**
 * Use crew status query (with polling)
 */
export const useCrewStatus = (taskId: string | undefined) => {
  return useQuery({
    queryKey: ["crew", taskId],
    queryFn: () => taskId ? crewApi.status(taskId).then(res => res.task) : null,
    enabled: !!taskId,
    refetchInterval: 1500,
  });
};

/**
 * Use wallet query
 */
export const useWallet = () => {
  return useQuery({
    queryKey: ["wallet"],
    queryFn: () => walletApi.get(),
    staleTime: 30 * 1000,
  });
};

/**
 * Use connect wallet mutation
 */
export const useConnectWallet = () => {
  return useMutation({
    mutationFn: (data: { address: string; chain?: string }) =>
      walletApi.connect(data.address, data.chain).then(res => res.wallet),
  });
};

/**
 * Use wallet simulate mutation
 */
export const useSimulateTransaction = () => {
  return useMutation({
    mutationFn: (data: { to: string; value: string; data?: string }) =>
      walletApi.simulate(data.to, data.value, data.data).then(res => res.simulation),
  });
};

/**
 * ASP Manifest queries & mutations
 */
export const useASPManifest = () => {
  return useQuery({
    queryKey: ["aspManifest"],
    queryFn: () => aspApi.getManifest().then(res => res.manifest),
  });
};

export const useValidateManifest = () => {
  return useMutation({
    mutationFn: (manifest: any) => aspApi.validate(manifest),
  });
};

export const useDeals = (statusFilter?: string) => {
  return useQuery({
    queryKey: ["deals", statusFilter],
    queryFn: () => dealflowApi.list(statusFilter).then(res => res.deals || []),
    staleTime: 5 * 1000,
  });
};

export const useDiscoverDeals = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (query?: string) => dealflowApi.discover(query).then(res => res.deals),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["deals"] });
    },
  });
};

export const useLaunches = (statusFilter?: string) => {
  return useQuery({
    queryKey: ["launches", statusFilter],
    queryFn: () => launchpadApi.list(statusFilter).then(res => res.launches || []),
  });
};

export const useSimulateContractDeployment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: { project_id?: string; title?: string; token_symbol?: string; wallet_address?: string }) =>
      launchpadApi.simulate(payload).then(res => res.simulation),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      if (variables.project_id) {
        queryClient.invalidateQueries({ queryKey: ["project", variables.project_id] });
      }
    },
  });
};
