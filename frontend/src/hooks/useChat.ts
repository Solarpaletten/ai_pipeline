// frontend/src/hooks/useChat.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { Message, Agent, Project, WebSocketMessage } from '../types/chat';

interface UseChatProps {
  userId: string;
  projectId: string;
  agentId: string;
}

interface UseChatReturn {
  messages: Message[];
  agents: Agent[];
  projects: Project[];
  currentAgent: Agent | null;
  currentProject: Project | null;
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
  sendMessage: (text: string) => Promise<void>;
  switchAgent: (agentId: string) => void;
  switchProject: (projectId: string) => void;
  clearMessages: () => void;
  exportMessages: () => string;
}

const useChat = ({ userId, projectId, agentId }: UseChatProps): UseChatReturn => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentAgent, setCurrentAgent] = useState<Agent | null>(null);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);

  // WebSocket URL
  const wsUrl = `ws://localhost:8002/api/chat/ws/${userId}`;

  // Инициализация WebSocket соединения
  const connectWebSocket = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      wsRef.current = new WebSocket(wsUrl);

      wsRef.current.onopen = () => {
        setIsConnected(true);
        setError(null);
        console.log('WebSocket connected');
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data: WebSocketMessage = JSON.parse(event.data);
          
          switch (data.type) {
            case 'message_received':
              // Сообщение получено сервером
              break;
              
            case 'agent_response':
              if (data.message) {
                setMessages(prev => [...prev, {
                  ...data.message!,
                  timestamp: new Date(data.message!.timestamp)
                }]);
              }
              break;
              
            case 'error':
              setError(data.error || 'Unknown error');
              break;
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
        }
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
        console.log('WebSocket disconnected');
        
        // Переподключение через 3 секунды
        setTimeout(connectWebSocket, 3000);
      };

      wsRef.current.onerror = (err) => {
        console.error('WebSocket error:', err);
        setError('Connection error');
      };

    } catch (err) {
      console.error('Failed to connect WebSocket:', err);
      setError('Failed to connect');
    }
  }, [wsUrl]);

  // Загрузка агентов
  const loadAgents = useCallback(async () => {
    try {
      const response = await fetch('/api/chat/agents');
      const data = await response.json();
      setAgents(data.agents);
      
      // Находим текущего агента
      const agent = data.agents.find((a: Agent) => a.id === agentId);
      setCurrentAgent(agent || null);
    } catch (err) {
      console.error('Failed to load agents:', err);
    }
  }, [agentId]);

  // Загрузка проектов
  const loadProjects = useCallback(async () => {
    try {
      const response = await fetch('/api/chat/projects');
      const data = await response.json();
      setProjects(data.projects);
      
      // Находим текущий проект
      const project = data.projects.find((p: Project) => p.id === projectId);
      setCurrentProject(project || null);
    } catch (err) {
      console.error('Failed to load projects:', err);
    }
  }, [projectId]);

  // Загрузка сообщений проекта
  const loadMessages = useCallback(async () => {
    if (!projectId) return;
    
    setIsLoading(true);
    try {
      const response = await fetch(`/api/chat/projects/${projectId}/messages`);
      const data = await response.json();
      
      const formattedMessages = data.messages.map((msg: any) => ({
        ...msg,
        timestamp: new Date(msg.timestamp)
      }));
      
      setMessages(formattedMessages);
    } catch (err) {
      console.error('Failed to load messages:', err);
      setError('Failed to load messages');
    } finally {
      setIsLoading(false);
    }
  }, [projectId]);

  // Отправка сообщения
  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || !isConnected || !currentAgent || !currentProject) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: text.trim(),
      timestamp: new Date(),
      agent_id: currentAgent.id,
      project_id: currentProject.id
    };

    // Добавляем сообщение пользователя в локальный стейт
    setMessages(prev => [...prev, userMessage]);

    try {
      // Отправляем через WebSocket
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          message: text.trim(),
          agent_id: currentAgent.id,
          project_id: currentProject.id,
          user_id: userId
        }));
      } else {
        // Fallback на REST API
        const response = await fetch('/api/chat/send', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: text.trim(),
            agent_id: currentAgent.id,
            project_id: currentProject.id,
            user_id: userId
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to send message');
        }

        const data = await response.json();
        
        // Добавляем ответ агента
        const agentMessage: Message = {
          id: data.message_id,
          sender: 'agent',
          text: data.response,
          timestamp: new Date(data.timestamp),
          agent_id: data.agent_id,
          agent_name: data.agent_name,
          project_id: currentProject.id
        };

        setMessages(prev => [...prev, agentMessage]);
      }
    } catch (err) {
      console.error('Failed to send message:', err);
      setError('Failed to send message');
    }
  }, [isConnected, currentAgent, currentProject, userId]);

  // Переключение агента
  const switchAgent = useCallback((newAgentId: string) => {
    const agent = agents.find(a => a.id === newAgentId);
    if (agent) {
      setCurrentAgent(agent);
    }
  }, [agents]);

  // Переключение проекта
  const switchProject = useCallback((newProjectId: string) => {
    const project = projects.find(p => p.id === newProjectId);
    if (project) {
      setCurrentProject(project);
      // Загружаем сообщения нового проекта
      // loadMessages() будет вызван через useEffect
    }
  }, [projects]);

  // Очистка сообщений
  const clearMessages = useCallback(async () => {
    if (!currentProject) return;

    try {
      await fetch(`/api/chat/projects/${currentProject.id}/messages`, {
        method: 'DELETE',
      });
      setMessages([]);
    } catch (err) {
      console.error('Failed to clear messages:', err);
      setError('Failed to clear messages');
    }
  }, [currentProject]);

  // Экспорт сообщений в TXT
  const exportMessages = useCallback(() => {
    if (!currentProject || messages.length === 0) return '';

    const exportData = [
      `Project: ${currentProject.name}`,
      `Exported: ${new Date().toLocaleString()}`,
      '=' .repeat(50),
      '',
      ...messages.map(msg => 
        `[${msg.timestamp.toLocaleString()}] ${msg.sender === 'user' ? 'You' : msg.agent_name}: ${msg.text}`
      )
    ].join('\n');

    // Создаем и скачиваем файл
    const blob = new Blob([exportData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentProject.name}_chat_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);

    return exportData;
  }, [currentProject, messages]);

  // Эффекты
  useEffect(() => {
    loadAgents();
    loadProjects();
  }, [loadAgents, loadProjects]);

  useEffect(() => {
    connectWebSocket();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connectWebSocket]);

  useEffect(() => {
    loadMessages();
  }, [loadMessages]);

  return {
    messages,
    agents,
    projects,
    currentAgent,
    currentProject,
    isConnected,
    isLoading,
    error,
    sendMessage,
    switchAgent,
    switchProject,
    clearMessages,
    exportMessages,
  };
};

export default useChat;