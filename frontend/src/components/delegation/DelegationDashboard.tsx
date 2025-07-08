// frontend/src/components/delegation/DelegationDashboard.tsx
import React, { useState } from 'react';

interface DelegationResponse {
  task: string;
  recommended_chain: string[];
  status: string;
}

export const DelegationDashboard: React.FC = () => {
  const [task, setTask] = useState('');
  const [result, setResult] = useState<DelegationResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleDelegate = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/delegation/route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task, user_id: 'test' })
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Delegation failed:', error);
    }
    setLoading(false);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">🚀 Level 7: AI Delegation</h1>
      
      <div className="mb-6">
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Опишите задачу для делегирования..."
          className="w-full p-3 border rounded-lg h-32"
        />
        <button
          onClick={handleDelegate}
          disabled={loading || !task}
          className="mt-3 px-6 py-2 bg-blue-500 text-white rounded-lg disabled:opacity-50"
        >
          {loading ? 'Анализируем...' : 'Делегировать задачу'}
        </button>
      </div>

      {result && (
        <div className="bg-gray-100 p-4 rounded-lg">
          <h3 className="font-bold mb-2">Рекомендуемая цепочка:</h3>
          <div className="flex gap-2">
            {result.recommended_chain.map((agent, index) => (
              <span key={index} className="px-3 py-1 bg-blue-200 rounded">
                {agent}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DelegationDashboard;