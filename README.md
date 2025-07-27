# Dynamic Shuffler - Arize Phoenix Starter Project

A simple chatbot application that demonstrates integration with OpenAI and Arize Phoenix for LLM observability.

## Overview

This project provides a starter template for building applications with LLM observability using Arize Phoenix. It includes:

- A FastAPI backend that integrates with OpenAI's API
- Arize Phoenix tracing for monitoring and analyzing LLM calls
- A React frontend with TypeScript for user interaction
- A simple chat interface to demonstrate the functionality

## Project Structure

```
dynamic-shuffler/
├── backend/               # FastAPI backend
│   ├── main.py            # Main FastAPI application
│   ├── openai_service.py  # OpenAI integration
│   ├── arize_service.py   # Arize Phoenix integration
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment variables template
├── frontend/              # React frontend
│   ├── src/               # Source code
│   │   ├── App.tsx        # Main application component
│   │   ├── ChatInterface.tsx # Chat UI component
│   │   ├── api.ts         # API client
│   │   └── ...            # Other components and styles
│   ├── package.json       # Frontend dependencies
│   └── .env.example       # Frontend environment variables
└── README.md              # Project documentation
```

## Prerequisites

- Node.js (v14 or later)
- Python (v3.8 or later)
- OpenAI API key
- Arize Phoenix account (optional for cloud instance)

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

6. Edit the `.env` file and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ARIZE_API_KEY=your_arize_api_key_here  # Optional for cloud instance
   ARIZE_SPACE_KEY=your_arize_space_key_here  # Optional for cloud instance
   ```

7. Run the backend:
   ```
   uvicorn main:app --reload
   ```

   The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file based on `.env.example` if you need to customize the API URL:
   ```
   cp .env.example .env
   ```

4. Start the development server:
   ```
   npm start
   ```

   The application will be available at http://localhost:3000

## Using the Application

1. Open the application in your browser at http://localhost:3000
2. Type a message in the input field and press Enter or click Send
3. The application will send your message to the OpenAI API via the backend
4. The response will be displayed in the chat interface
5. Each interaction is traced with Arize Phoenix for observability

## Arize Phoenix Integration

This starter project demonstrates how to integrate Arize Phoenix for LLM observability:

1. Each LLM call is traced with a unique ID
2. The trace includes the prompt, model, and response
3. The trace ID is returned to the frontend and displayed
4. You can view the traces in the Arize Phoenix UI

## Customization

- **Backend**: Modify `main.py`, `openai_service.py`, and `arize_service.py` to customize the backend functionality
- **Frontend**: Modify the React components in the `frontend/src` directory to customize the UI
- **Models**: Change the model parameter in `ChatInterface.tsx` to use different OpenAI models

## Troubleshooting

- **Backend errors**: Check the terminal where the backend is running for error messages
- **Frontend errors**: Check the browser console for error messages
- **API key issues**: Ensure your API keys are correctly set in the `.env` file
- **CORS issues**: The backend is configured to allow requests from any origin. In production, you should restrict this to specific origins.

## License

MIT