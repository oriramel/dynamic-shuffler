# Implementation Plan for Arize Phoenix Starter Project

This document outlines the implementation details for our Arize Phoenix starter project with OpenAI integration.

## Project Structure

```
dynamic-shuffler/
├── backend/
│   ├── main.py             # FastAPI application with all routes
│   ├── openai_service.py   # OpenAI integration
│   ├── arize_service.py    # Arize Phoenix integration
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main application component
│   │   ├── ChatInterface.tsx # Chat UI component
│   │   ├── api.ts          # API client
│   │   └── index.tsx       # Entry point
│   ├── tsconfig.json       # TypeScript configuration
│   ├── package.json        # Frontend dependencies
│   └── .env.example        # Frontend environment variables
└── README.md               # Project documentation
```

## Backend Implementation

### requirements.txt
```
fastapi>=0.95.0
uvicorn>=0.21.0
python-dotenv>=1.0.0
openai>=1.0.0
pydantic>=2.0.0
arize-phoenix>=0.1.0
```

### .env.example
```
OPENAI_API_KEY=your_openai_api_key_here
ARIZE_API_KEY=your_arize_api_key_here
ARIZE_SPACE_KEY=your_arize_space_key_here
```

### main.py
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from openai_service import get_chat_completion
from arize_service import trace_llm_call

# Load environment variables
load_dotenv()

app = FastAPI(title="Chatbot API with Arize Phoenix Tracing")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-3.5-turbo"

class ChatResponse(BaseModel):
    message: Message
    trace_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Convert Pydantic models to dictionaries for the OpenAI API
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Get response from OpenAI
        response, trace_id = await get_chat_completion(messages, request.model)
        
        return ChatResponse(
            message=Message(role="assistant", content=response),
            trace_id=trace_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### openai_service.py
```python
import os
import openai
import uuid
from arize_service import trace_llm_call

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_chat_completion(messages, model="gpt-3.5-turbo"):
    # Generate a unique trace ID for this request
    trace_id = str(uuid.uuid4())
    
    try:
        # Call OpenAI API
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=messages
        )
        
        # Extract the response content
        content = response.choices[0].message.content
        
        # Trace the LLM call with Arize Phoenix
        trace_llm_call(
            trace_id=trace_id,
            model=model,
            prompt=messages,
            response=content,
            response_obj=response
        )
        
        return content, trace_id
    
    except Exception as e:
        # Log the error and re-raise
        print(f"Error calling OpenAI API: {str(e)}")
        raise
```

### arize_service.py
```python
import os
from typing import Dict, List, Any, Optional
import json

# Import Arize Phoenix SDK
try:
    from arize.phoenix.trace import trace
except ImportError:
    print("Arize Phoenix SDK not installed. Tracing will be disabled.")
    
    # Create a dummy trace function for when the SDK is not available
    def trace(*args, **kwargs):
        print("Arize Phoenix tracing disabled.")
        return None

def trace_llm_call(
    trace_id: str,
    model: str,
    prompt: List[Dict[str, str]],
    response: str,
    response_obj: Optional[Any] = None
):
    """
    Trace an LLM call to Arize Phoenix.
    
    Args:
        trace_id: A unique identifier for this trace
        model: The model name (e.g., "gpt-3.5-turbo")
        prompt: The list of messages sent to the model
        response: The text response from the model
        response_obj: The full response object from the API
    """
    try:
        # Convert prompt to string for easier viewing in Arize Phoenix
        prompt_str = json.dumps(prompt, indent=2)
        
        # Trace the LLM call
        trace(
            name=f"LLM Call - {model}",
            inputs={
                "prompt": prompt_str,
                "model": model
            },
            outputs={
                "response": response
            },
            span_id=trace_id
        )
        
        print(f"Traced LLM call with ID: {trace_id}")
    
    except Exception as e:
        print(f"Error tracing LLM call: {str(e)}")
```

## Frontend Implementation

### package.json
```json
{
  "name": "chatbot-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@types/node": "^16.18.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "axios": "^1.3.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.5"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": [
    "src"
  ]
}
```

### src/api.ts
```typescript
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
```

### src/App.tsx
```typescript
import React from 'react';
import ChatInterface from './ChatInterface';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Arize Phoenix Chatbot Demo</h1>
      </header>
      <main>
        <ChatInterface />
      </main>
      <footer>
        <p>Powered by OpenAI and Arize Phoenix</p>
      </footer>
    </div>
  );
}

export default App;
```

### src/ChatInterface.tsx
```typescript
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
```

### src/ChatInterface.css
```css
.chat-container {
  display: flex;
  flex-direction: column;
  height: 70vh;
  max-width: 800px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 12px;
  border-radius: 8px;
  word-break: break-word;
}

.message.user {
  align-self: flex-end;
  background-color: #0084ff;
  color: white;
}

.message.assistant {
  align-self: flex-start;
  background-color: #f1f0f0;
  color: #333;
}

.message.loading {
  background-color: #f1f0f0;
}

.loading-indicator {
  display: flex;
  justify-content: center;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #888;
  text-align: center;
}

.chat-input-form {
  display: flex;
  padding: 16px;
  border-top: 1px solid #ccc;
}

.chat-input-form input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 8px;
}

.chat-input-form button {
  padding: 12px 24px;
  background-color: #0084ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-input-form button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.trace-info {
  padding: 8px 16px;
  background-color: #f8f9fa;
  border-top: 1px solid #eee;
  font-size: 12px;
  color: #666;
}
```

### src/App.css
```css
.App {
  text-align: center;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}

main {
  flex: 1;
  padding: 20px;
}

footer {
  padding: 10px;
  background-color: #f8f9fa;
  border-top: 1px solid #eee;
}
```

## Next Steps

1. Create the directory structure
2. Implement the backend files
3. Implement the frontend files
4. Test the application
5. Document any additional setup or configuration steps

Once the implementation is complete, we can test the application by:
1. Starting the backend server
2. Starting the frontend development server
3. Sending messages through the chat interface
4. Verifying that the responses are received correctly
5. Checking that the traces are being sent to Arize Phoenix