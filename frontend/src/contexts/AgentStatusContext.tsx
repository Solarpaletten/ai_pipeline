import React, { createContext, useContext, useState, ReactNode } from 'react';

interface Agent {
  name: string;
  is_online: boolean;
  token_valid: boolean;
  response_time_ms: number;
  last_check: string;
  success_rate: number;
}

interface AgentStatusContextType {
  agents: Agent[];
  setAgents: (agents: Agent[]) => void;
  updateAgent: (name: string, status: Partial<Agent>) => void;
}

const AgentStatusContext = createContext<AgentStatusContextType | undefined>(undefined);

export const useAgentStatus = () => {
  const context = useContext(AgentStatusContext);
  if (!context) {
    throw new Error('useAgentStatus must be used within AgentStatusProvider');
  }
  return context;
};

interface AgentStatusProviderProps {
  children: ReactNode;
}

const AgentStatusProvider: React.FC<AgentStatusProviderProps> = ({ children }) => {
  const [agents, setAgents] = useState<Agent[]>([
    {
      name: 'dashka',
      is_online: true,
      token_valid: true,
      response_time_ms: 150,
      last_check: new Date().toISOString(),
      success_rate: 98.5
    },
    {
      name: 'claude',
      is_online: true,
      token_valid: true,
      response_time_ms: 200,
      last_check: new Date().toISOString(),
      success_rate: 97.8
    },
    {
      name: 'deepseek',
      is_online: true,
      token_valid: true,
      response_time_ms: 180,
      last_check: new Date().toISOString(),
      success_rate: 96.2
    }
  ]);

  const updateAgent = (name: string, status: Partial<Agent>) => {
    setAgents(prevAgents =>
      prevAgents.map(agent =>
        agent.name === name ? { ...agent, ...status } : agent
      )
    );
  };

  return (
    <AgentStatusContext.Provider value={{ agents, setAgents, updateAgent }}>
      {children}
    </AgentStatusContext.Provider>
  );
};

export default AgentStatusProvider;
