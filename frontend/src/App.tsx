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