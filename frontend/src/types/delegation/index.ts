export interface DelegationTask {
  id: string;
  task: string;
  status: string;
}

export interface AgentChain {
  agents: string[];
  currentAgent: number;
}

export {};
