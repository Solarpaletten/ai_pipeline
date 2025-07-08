// frontend/src/types/chat.ts

export interface Message {
    id: string;
    sender: 'user' | 'agent';
    text: string;
    timestamp: Date;
    agent_id?: string;
    agent_name?: string;
    project_id?: string;
  }
  
  export interface Project {
    id: string;
    name: string;
    description?: string;
    created_at: Date;
    updated_at: Date;
    is_active: boolean;
    chat_count: number;
  }
  
  export interface Agent {
    id: string;
    name: string;
    description: string;
    emoji: string;
    color: string;
    is_online: boolean;
    capabilities: string[];
  }
  
  export interface ChatSession {
    id: string;
    project_id: string;
    agent_id: string;
    agent_name: string;
    created_at: Date;
    messages: Message[];
    is_active: boolean;
  }
  
  export interface ChatRequest {
    message: string;
    agent_id: string;
    project_id: string;
    user_id?: string;
  }
  
  export interface ChatResponse {
    message_id: string;
    response: string;
    agent_id: string;
    agent_name: string;
    timestamp: Date;
    success: boolean;
    error?: string;
  }
  
  export interface WebSocketMessage {
    type: 'message_received' | 'agent_response' | 'error' | 'typing' | 'connected';
    message?: Message;
    error?: string;
    data?: any;
  }