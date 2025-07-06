export interface AgentStatus {
  name: string;
  is_online: boolean;
  token_valid: boolean;
  response_time_ms: number;
  last_check: string;
  success_rate: number;
}

export interface DelegationEvent {
  id: string;
  timestamp: string;
  from_agent: string;
  to_agent: string;
  user_id: number;
  message: string;
  response?: string;
  status: 'pending' | 'completed' | 'failed';
  response_time_ms?: number;
}

export interface SystemMetrics {
  total_agents: number;
  online_agents: number;
  timestamp: string;
}

export interface WebSocketMessage {
  type: 'agent_status_update' | 'new_delegation' | 'initial_data' | 'pong';
  data?: any;
}
