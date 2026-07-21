/**
 * React hooks for BuilderForge API calls
 */

import { useQuery, useMutation } from "@tanstack/react-query";
import { 
  projectsApi, 
  crewApi, 
  walletApi, 
  dealflowApi, 
  launchpadApi,
  type Project,
  type CrewTask,
  type Deal,
  type Launch,
} from "./api";

/**
 * Use projects query
 */
export const useProjects = () => {
  return useQuery({
    queryKey: ["projects"],
    queryFn: () => projectsApi.list().then(res => res.projects || []),
    staleTime: 5 * 60 * 1000, // 5 minutes
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
    staleTime: 5 * 60 * 1000,
  });
};

/**
 * Use create project mutation
 */
export const useCreateProject = () => {
  return useMutation({
    mutationFn: (data: { title: string; description: string; category?: string }) =>
      projectsApi.create(data).then(res => res.project),
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
    refetchInterval: 2000, // Poll every 2 seconds
  });
};

/**
 * Use wallet query
 */
export const useWallet = () => {
  return useQuery({
    queryKey: ["wallet"],
    queryFn: () => walletApi.get(),
    staleTime: 30 * 1000, // 30 seconds
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
 * Use deals query
 */
export const useDeals = (statusFilter?: string) => {
  return useQuery({
    queryKey: ["deals", statusFilter],
    queryFn: () => dealflowApi.list(statusFilter).then(res => res.deals || []),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

/**
 * Use launches query
 */
export const useLaunches = (statusFilter?: string) => {
  return useQuery({
    queryKey: ["launches", statusFilter],
    queryFn: () => launchpadApi.list(statusFilter).then(res => res.launches || []),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};
