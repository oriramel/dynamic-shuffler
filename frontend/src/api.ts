import axios from 'axios';

// API base URL - adjust as needed
const API_BASE_URL = 'http://localhost:8000';

// Message interface
export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

// Chat request interface
export interface ChatRequest {
  messages: Message[];
  model?: string;
}

// Chat response interface
export interface ChatResponse {
  message: Message;
  trace_id: string;
}

// Function to send a chat request to the backend
export const sendChatRequest = async (request: ChatRequest): Promise<ChatResponse> => {
  try {
    const response = await axios.post<ChatResponse>(`${API_BASE_URL}/chat`, request);
    return response.data;
  } catch (error) {
    console.error('Error sending chat request:', error);
    throw error;
  }
};