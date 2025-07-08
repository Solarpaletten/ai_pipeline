import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Dashboard } from './components/dashboard/Dashboard';
import DelegationDashboard from './components/delegation/DelegationDashboard';
import AgentStatusProvider from './contexts/AgentStatusContext';
import WebSocketProvider from './contexts/WebSocketContext';

function App() {
  return (
    <WebSocketProvider>
      <AgentStatusProvider>
        <Router>
          <Routes>
            {/* Основной дашборд */}
            <Route path="/" element={<Dashboard />} />
            
            {/* Панель делегирования задач */}
            <Route path="/delegation" element={<DelegationDashboard />} />
            
            {/* Дополнительные маршруты можно добавить здесь */}
          </Routes>
        </Router>
      </AgentStatusProvider>
    </WebSocketProvider>
  );
}

export default App;