import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Dashboard } from './components/dashboard/Dashboard';
import DelegationDashboard from './components/delegation/DelegationDashboard';
import AgentStatusProvider from './contexts/AgentStatusContext';
import WebSocketProvider from './contexts/WebSocketContext';

function App() {
  return (
    <AgentStatusProvider>
      <WebSocketProvider>
        <Router>
          <div className="App">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/delegation" element={<DelegationDashboard />} />
            </Routes>
          </div>
        </Router>
      </WebSocketProvider>
    </AgentStatusProvider>
  );
}

export default App;
