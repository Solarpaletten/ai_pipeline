import React, { useState, useEffect } from 'react';

interface DelegationResult {
  task: string;
  complexity: string;
  recommended_chain: string[];
  reasoning: string;
  estimated_time: number;
  level: number;
  status: string;
}

const DelegationDashboard: React.FC = () => {
  const [task, setTask] = useState('');
  const [result, setResult] = useState<DelegationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [level7Status, setLevel7Status] = useState<any>(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002/api';

  useEffect(() => {
    fetchLevel7Status();
  }, []);

  const fetchLevel7Status = async () => {
    try {
      const response = await fetch(`${API_URL}/delegation/status`);
      if (response.ok) {
        const data = await response.json();
        setLevel7Status(data);
      }
    } catch (error) {
      console.error('Failed to fetch Level 7 status:', error);
    }
  };

  const handleDelegateTask = async () => {
    if (!task.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/delegation/route`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task: task,
          user_id: 'frontend_user'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        console.error('Delegation failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error during delegation:', error);
    } finally {
      setLoading(false);
    }
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'SIMPLE': return 'text-green-400';
      case 'MEDIUM': return 'text-yellow-400';
      case 'COMPLEX': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">🚀 Level 7: AI Delegation System</h1>
          <p className="text-slate-400">Умная маршрутизация задач между AI агентами</p>
        </div>

        {level7Status && (
          <div className="bg-slate-800 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">📊 System Status</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-sm text-slate-400">Level 7 Status</div>
                <div className={level7Status.level7_enabled ? 'text-green-400' : 'text-red-400'}>
                  {level7Status.level7_enabled ? '🟢 Enabled' : '🔴 Disabled'}
                </div>
              </div>
              <div>
                <div className="text-sm text-slate-400">Version</div>
                <div className="text-white">{level7Status.version}</div>
              </div>
              <div>
                <div className="text-sm text-slate-400">Engine Status</div>
                <div className="text-green-400">{level7Status.engine_status}</div>
              </div>
              <div>
                <div className="text-sm text-slate-400">Available Agents</div>
                <div className="text-white">{level7Status.agents_available?.length || 0}</div>
              </div>
            </div>
          </div>
        )}

        <div className="bg-slate-800 rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">🎯 Task Delegation</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Описание задачи:
              </label>
              <textarea
                value={task}
                onChange={(e) => setTask(e.target.value)}
                placeholder="Например: Создать систему регистрации пользователей с валидацией"
                className="w-full bg-slate-700 border border-slate-600 rounded-md p-3 text-white placeholder-slate-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
              />
            </div>
            <button
              onClick={handleDelegateTask}
              disabled={loading || !task.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 px-6 py-2 rounded-md font-medium transition-colors"
            >
              {loading ? '🔄 Analyzing...' : '🚀 Delegate Task'}
            </button>
          </div>
        </div>

        {result && (
          <div className="bg-slate-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">🎯 Delegation Result</h2>
            <div className="space-y-4">
              <div>
                <div className="text-sm text-slate-400">Task</div>
                <div className="text-white">{result.task}</div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <div className="text-sm text-slate-400">Complexity</div>
                  <div className={`font-medium ${getComplexityColor(result.complexity)}`}>
                    {result.complexity}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Estimated Time</div>
                  <div className="text-white">{result.estimated_time} minutes</div>
                </div>
                <div>
                  <div className="text-sm text-slate-400">Status</div>
                  <div className="text-green-400">{result.status}</div>
                </div>
              </div>

              <div>
                <div className="text-sm text-slate-400 mb-2">Recommended Agent Chain</div>
                <div className="flex space-x-2">
                  {result.recommended_chain.map((agent, index) => (
                    <div key={index} className="flex items-center">
                      <div className="bg-blue-600 px-3 py-1 rounded-md text-sm font-medium">
                        {agent}
                      </div>
                      {index < result.recommended_chain.length - 1 && (
                        <div className="mx-2 text-slate-400">→</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <div className="text-sm text-slate-400">Reasoning</div>
                <div className="text-slate-300">{result.reasoning}</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DelegationDashboard;
