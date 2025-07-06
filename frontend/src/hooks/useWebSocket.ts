import { useEffect, useState, useCallback } from 'react';
import io, { Socket } from 'socket.io-client';
import { AgentStatus, DelegationEvent, WebSocketMessage } from '../types';

const WEBSOCKET_URL = process.env.REACT_APP_WS_URL || 'ws://aisolar.swapoil.de:8000/ws/dashboard';
const API_URL = process.env.REACT_APP_API_URL || 'http://aisolar.swapoil.de:8000/api'\;

export const useWebSocket = () => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  const [agents, setAgents] = useState<AgentStatus[]>([]);
  const [delegations, setDelegations] = useState<DelegationEvent[]>([]);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const connect = useCallback(() => {
    try {
      console.log('🔌 Connecting to WebSocket:', WEBSOCKET_URL);
      
      const newSocket = io(WEBSOCKET_URL, {
        transports: ['websocket', 'polling'],
        timeout: 5000,
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 2000,
        forceNew: true,
      });

      newSocket.on('connect', () => {
        console.log('✅ WebSocket connected to backend:', WEBSOCKET_URL);
        setConnected(true);
        newSocket.emit('ping');
      });

      newSocket.on('disconnect', (reason) => {
        console.log('🔌 WebSocket disconnected:', reason);
        setConnected(false);
      });

      newSocket.on('connect_error', (error) => {
        console.error('❌ WebSocket connection error:', error);
        setConnected(false);
      });

      newSocket.on('message', (data: WebSocketMessage) => {
        console.log('📨 WebSocket message received:', data);
        
        switch (data.type) {
          case 'agent_status_update':
            if (data.data?.agents) {
              setAgents(data.data.agents);
              setLastUpdate(new Date());
            }
            break;
            
          case 'new_delegation':
            if (data.data) {
              setDelegations(prev => [data.data, ...prev.slice(0, 49)]);
            }
            break;
            
          case 'initial_data':
            if (data.data?.agents) {
              setAgents(data.data.agents);
            }
            if (data.data?.recent_delegations) {
              setDelegations(data.data.recent_delegations);
            }
            setLastUpdate(new Date());
            break;
        }
      });

      setSocket(newSocket);
      
    } catch (error) {
      console.error('❌ WebSocket setup failed:', error);
      setConnected(false);
    }
  }, []);

  const disconnect = useCallback(() => {
    if (socket) {
      socket.disconnect();
      setSocket(null);
      setConnected(false);
    }
  }, [socket]);

  // Fallback: загружаем данные через REST API если WebSocket не работает
  useEffect(() => {
    if (!connected) {
      const fetchAgentStatus = async () => {
        try {
          console.log('📡 Fetching agent status from API:', API_URL);
          const response = await fetch(`${API_URL}/agents/status`);
          if (response.ok) {
            const data = await response.json();
            if (data.agents) {
              setAgents(data.agents);
              setLastUpdate(new Date());
              console.log('✅ Agent status loaded from API');
            }
          }
        } catch (error) {
          console.error('❌ Failed to fetch agent status:', error);
          
          // Используем mock данные как последний резерв
          const mockAgents: AgentStatus[] = [
            {
              name: 'Dashka',
              is_online: true,
              token_valid: true,
              response_time_ms: 245.6,
              last_check: new Date().toISOString(),
              success_rate: 97.8
            },
            {
              name: 'Claude',
              is_online: true,
              token_valid: true,
              response_time_ms: 189.3,
              last_check: new Date().toISOString(),
              success_rate: 99.2
            },
            {
              name: 'DeepSeek',
              is_online: true,
              token_valid: true,
              response_time_ms: 312.7,
              last_check: new Date().toISOString(),
              success_rate: 95.4
            }
          ];
          
          setAgents(mockAgents);
          setLastUpdate(new Date());
          console.log('📊 Using mock data');
        }
      };

      const timer = setTimeout(fetchAgentStatus, 2000);
      return () => clearTimeout(timer);
    }
  }, [connected]);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    connected,
    agents,
    delegations,
    lastUpdate,
    reconnect: connect,
  };
};
