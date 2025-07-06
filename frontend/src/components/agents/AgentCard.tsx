import React from 'react';
import { AgentStatus } from '../../types';
import { CheckCircle, XCircle, Clock } from 'lucide-react';

interface AgentCardProps {
  agent: AgentStatus;
  color: string;
  icon: string;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, color, icon }) => {
  const isOnline = agent.is_online && agent.token_valid;
  
  const getStatusColor = () => {
    if (!agent.is_online) return 'text-red-500';
    if (!agent.token_valid) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getStatusIcon = () => {
    if (!agent.is_online) return <XCircle className="w-5 h-5" />;
    if (!agent.token_valid) return <Clock className="w-5 h-5" />;
    return <CheckCircle className="w-5 h-5" />;
  };

  return (
    <div className="agent-card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div 
            className="text-3xl p-2 rounded-lg"
            style={{ backgroundColor: `${color}20` }}
          >
            {icon}
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{agent.name}</h3>
            <div className={`flex items-center space-x-1 ${getStatusColor()}`}>
              {getStatusIcon()}
              <span className="text-sm font-medium">
                {isOnline ? 'Online' : 'Offline'}
              </span>
            </div>
          </div>
        </div>
        
        <div className={`w-4 h-4 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'} ${isOnline ? 'animate-pulse-slow' : ''}`} />
      </div>

      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Response Time</span>
          <span className="text-sm font-medium text-gray-800">
            {agent.response_time_ms.toFixed(1)}ms
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Token Status</span>
          <span className={`text-sm font-medium ${agent.token_valid ? 'text-green-600' : 'text-red-600'}`}>
            {agent.token_valid ? 'Valid' : 'Invalid'}
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Success Rate</span>
          <span className="text-sm font-medium text-gray-800">
            {agent.success_rate.toFixed(1)}%
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Last Check</span>
          <span className="text-xs text-gray-500">
            {new Date(agent.last_check).toLocaleTimeString()}
          </span>
        </div>
      </div>

      <div className="mt-4">
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-gray-500">Performance</span>
          <span className="text-xs text-gray-500">{agent.success_rate.toFixed(0)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="h-2 rounded-full transition-all duration-300"
            style={{ 
              width: `${agent.success_rate}%`,
              backgroundColor: color 
            }}
          />
        </div>
      </div>
    </div>
  );
};
