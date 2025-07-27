import React, { useState } from 'react';
import { Message, sendChatRequest } from './api';
import './ChatInterface.css';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [traceId, setTraceId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Add user message to the chat
    const userMessage: Message = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Send request to the backend
      const response = await sendChatRequest({
        messages: [...messages, userMessage],
        model: 'gpt-3.5-turbo'
      });
      
      // Add assistant response to the chat
      setMessages(prevMessages => [...prevMessages, response.message]);
      setTraceId(response.trace_id);
    } catch (error) {
      console.error('Error getting response:', error);
      // Add error message
      setMessages(prevMessages => [
        ...prevMessages, 
        { role: 'assistant', content: 'Sorry, there was an error processing your request.' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>Start a conversation by sending a message below.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">{message.content}</div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message assistant loading">
            <div className="loading-indicator">...</div>
          </div>
        )}
      </div>
      
      {traceId && (
        <div className="trace-info">
          <p>Last response trace ID: {traceId}</p>
        </div>
      )}
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;