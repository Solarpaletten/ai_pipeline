import React from 'react';
import { useWebSocket } from '../../hooks/useWebSocket';
import { AgentCard } from '../agents/AgentCard';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { connected, agents, delegations, lastUpdate, reconnect } = useWebSocket();

  const getAgentConfig = (agentName: string) => {
    const configs = {
      'Dashka': { color: '#00BCD4', icon: '🤖' },
      'Claude': { color: '#9C27B0', icon: '🧠' },
      'DeepSeek': { color: '#4CAF50', icon: '💻' }
    };
    return configs[agentName as keyof typeof configs] || { color: '#666', icon: '🔧' };
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-800 mb-2">
                AI Pipeline Dashboard
              </h1>
              <p className="text-gray-600">
                Real-time monitoring of Dashka, Claude & DeepSeek
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                connected ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
              }`}>
                {connected ? <Wifi className="w-5 h-5" /> : <WifiOff className="w-5 h-5" />}
                <span className="text-sm font-medium">
                  {connected ? 'Connected' : 'Demo Mode'}
                </span>
              </div>
              
              <button
                onClick={reconnect}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>

        {/* System Status */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">System Status</h3>
            <p className={`text-2xl font-bold ${connected ? 'text-green-600' : 'text-yellow-600'}`}>
              {connected ? 'Live' : 'Demo'}
            </p>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Active Agents</h3>
            <p className="text-2xl font-bold text-blue-600">
              {agents.filter(a => a.is_online).length}/{agents.length}
            </p>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Last Update</h3>
            <p className="text-sm text-gray-600">
              {lastUpdate.toLocaleTimeString()}
            </p>
          </div>
        </div>

        {/* Agent Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {agents.map((agent) => {
            const config = getAgentConfig(agent.name);
            return (
              <AgentCard
                key={agent.name}
                agent={agent}
                color={config.color}
                icon={config.icon}
              />
            );
          })}
        </div>

        {/* Live Activity */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Live Activity</h2>
          <div className="text-center text-gray-500 py-8">
            <p>Dashboard successfully loaded! 🚀</p>
            <p className="text-sm mt-2">
              {connected ? 'Connected to backend WebSocket' : 'Running in demo mode with mock data'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
