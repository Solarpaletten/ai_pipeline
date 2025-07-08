// frontend/src/components/chat/ChatWidget.tsx
import React, { useState } from 'react';

interface ChatWidgetProps {
  userId: string;
  projectId: string;
  agentId: string;
  onAgentChange?: (agentId: string) => void;
  onProjectChange?: (projectId: string) => void;
}

const ChatWidget: React.FC<ChatWidgetProps> = ({
  userId,
  projectId,
  agentId,
  onAgentChange,
  onProjectChange,
}) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [inputMessage, setInputMessage] = useState('');

  const handleSend = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');

    // Заглушка для ответа агента
    setTimeout(() => {
      const agentMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'agent',
        text: `${agentId}: Получил ваше сообщение "${inputMessage}". Обрабатываю...`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, agentMessage]);
    }, 1000);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-96 bg-white rounded-lg border shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-gray-50 rounded-t-lg">
        <div className="flex items-center space-x-4">
          <span className="text-sm font-medium">Agent: {agentId}</span>
          <span className="text-xs text-gray-500">Project: {projectId || 'None'}</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-green-500" />
          <span className="text-xs text-gray-500">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <div className="text-4xl mb-2">💬</div>
            <p>No messages yet. Start a conversation!</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.text}</div>
                <div
                  className={`text-xs mt-1 ${
                    message.sender === 'user'
                      ? 'text-blue-100'
                      : 'text-gray-500'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={`Message ${agentId}...`}
            className="flex-1 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSend}
            disabled={!inputMessage.trim()}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              !inputMessage.trim()
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            Send
          </button>
        </div>

        <div className="flex justify-between items-center mt-3">
          <div className="text-xs text-gray-500">
            {messages.length} message{messages.length !== 1 ? 's' : ''}
          </div>
          <button
            onClick={() => setMessages([])}
            className="text-xs text-red-600 hover:text-red-800 px-2 py-1 rounded"
            disabled={messages.length === 0}
          >
            🗑️ Clear
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatWidget;