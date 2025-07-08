// frontend/src/components/dashboard/Dashboard.tsx
import React, { useState } from 'react';
import ChatWidget from '../chat/ChatWidget';
import { useWebSocket } from '../../hooks/useWebSocket';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';

export const Dashboard: React.FC = () => {
  // WebSocket connection для общей статистики
  const { connected, agents, delegations, lastUpdate, reconnect } = useWebSocket();

  // Состояние для чата
  const [selectedAgent, setSelectedAgent] = useState('claude');
  const [selectedProject, setSelectedProject] = useState('');
  const [showChat, setShowChat] = useState(false);

  // Простые карточки агентов без AgentCard компонента
  const agentCards = [
    {
      id: 'dashka',
      name: 'Dashka',
      description: 'Координатор и UI-специалист',
      emoji: '🤖',
      color: 'from-purple-500 to-pink-500',
      status: connected ? 'online' : 'offline'
    },
    {
      id: 'claude',
      name: 'Claude',
      description: 'Аналитик и архитектор',
      emoji: '🧠',
      color: 'from-blue-500 to-cyan-500',
      status: connected ? 'online' : 'offline'
    },
    {
      id: 'deepseek',
      name: 'DeepSeek',
      description: 'Инженер и разработчик',
      emoji: '💻',
      color: 'from-green-500 to-emerald-500',
      status: connected ? 'online' : 'offline'
    }
  ];

  const handleAgentClick = (agentId: string) => {
    setSelectedAgent(agentId);
    setShowChat(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">
              AI Pipeline Dashboard
            </h1>
            <p className="text-slate-300">
              Coordinate your AI agents and manage projects
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Connection Status */}
            <div className="flex items-center space-x-2 bg-white/10 rounded-lg px-4 py-2">
              {connected ? (
                <>
                  <Wifi className="w-4 h-4 text-green-400" />
                  <span className="text-green-400 text-sm">Connected</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-4 h-4 text-red-400" />
                  <span className="text-red-400 text-sm">Disconnected</span>
                  <button
                    onClick={reconnect}
                    className="ml-2 p-1 hover:bg-white/20 rounded"
                  >
                    <RefreshCw className="w-3 h-3" />
                  </button>
                </>
              )}
            </div>

            {/* Chat Toggle Button */}
            <button
              onClick={() => setShowChat(!showChat)}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                showChat
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
            >
              {showChat ? '❌ Close Chat' : '💬 Open Chat'}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Agent Cards & Stats */}
          <div className="space-y-6">
            {/* Simple Agent Cards */}
            <div className="grid grid-cols-1 gap-4">
              {agentCards.map((agent) => (
                <div
                  key={agent.id}
                  onClick={() => handleAgentClick(agent.id)}
                  className={`
                    cursor-pointer transition-all duration-300 hover:scale-105
                    bg-gradient-to-r ${agent.color} p-6 rounded-lg shadow-lg
                    border border-white/20 backdrop-blur-sm
                  `}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="text-3xl">{agent.emoji}</div>
                      <div>
                        <h3 className="text-xl font-bold text-white">
                          {agent.name}
                        </h3>
                        <p className="text-white/80 text-sm">
                          {agent.description}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className={`w-3 h-3 rounded-full ${
                        agent.status === 'online' ? 'bg-green-400' : 'bg-red-400'
                      }`} />
                      <span className="text-white/80 text-sm capitalize">
                        {agent.status}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* System Stats */}
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-white mb-4">
                System Overview
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">
                    {agentCards.filter(a => a.status === 'online').length}
                  </div>
                  <div className="text-sm text-slate-300">Active Agents</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">
                    {Array.isArray(agents) ? agents.length : 0}
                  </div>
                  <div className="text-sm text-slate-300">Total Agents</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-400">2m</div>
                  <div className="text-sm text-slate-300">Avg Response</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-400">
                    {connected ? '98%' : '0%'}
                  </div>
                  <div className="text-sm text-slate-300">Uptime</div>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-white mb-4">
                Recent Activity
              </h3>
              <div className="space-y-3">
                {delegations && Array.isArray(delegations) && delegations.length > 0 ? (
                  delegations.slice(0, 3).map((delegation, index) => (
                    <div key={index} className="flex items-center space-x-3 text-sm">
                      <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                      <span className="text-slate-300">
                        {delegation.message || 'Task completed'}
                      </span>
                      <span className="text-slate-500 ml-auto">
                        {delegation.timestamp ? new Date(delegation.timestamp).toLocaleTimeString() : 'now'}
                      </span>
                    </div>
                  ))
                ) : (
                  <div className="text-slate-400 text-sm">No recent activity</div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column: Chat Widget */}
          <div className="space-y-6">
            {showChat ? (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h3 className="text-xl font-semibold text-white mb-4">
                  AI Chat Interface
                </h3>
                <ChatWidget
                  userId="default_user"
                  projectId={selectedProject}
                  agentId={selectedAgent}
                  onAgentChange={setSelectedAgent}
                  onProjectChange={setSelectedProject}
                />
              </div>
            ) : (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                <div className="text-6xl mb-4">💬</div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  Start Chatting
                </h3>
                <p className="text-slate-300 mb-4">
                  Click "Open Chat" to start communicating with your AI agents
                </p>
                <div className="flex justify-center space-x-2 mb-4">
                  {agentCards.map((agent) => (
                    <button
                      key={agent.id}
                      onClick={() => handleAgentClick(agent.id)}
                      className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-colors"
                    >
                      {agent.emoji} {agent.name}
                    </button>
                  ))}
                </div>
                <button
                  onClick={() => setShowChat(true)}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  Open Chat Interface
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Last Update */}
        {lastUpdate && (
          <div className="mt-8 text-center text-slate-400 text-sm">
            Last update: {new Date(lastUpdate).toLocaleString()}
          </div>
        )}
      </div>
    </div>
  );
};