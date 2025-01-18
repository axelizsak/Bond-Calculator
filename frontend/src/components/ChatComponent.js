import React, { useState, useEffect, useRef } from 'react';

const ChatComponent = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [wsConnected, setWsConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const connectWebSocket = () => {
      ws.current = new WebSocket('ws://localhost:8000/chat');
      
      ws.current.onopen = () => {
        console.log('WebSocket Connected');
        setWsConnected(true);
      };
      
      ws.current.onmessage = (event) => {
        setMessages(prev => [...prev, { role: 'assistant', content: event.data }]);
        setLoading(false);
      };
      
      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setWsConnected(false);
      };
      
      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setWsConnected(false);
        // Tentative de reconnexion après 3 secondes
        setTimeout(connectWebSocket, 3000);
      };
    };

    connectWebSocket();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || !wsConnected || loading) return;
    
    // Ajouter le message de l'utilisateur à l'historique
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setLoading(true);
    
    // Envoyer le message au serveur
    if (ws.current && wsConnected) {
      ws.current.send(input);
    }
    
    setInput('');
  };
  
  return (
    <div className="w-full max-w-2xl mx-auto p-4 space-y-4">
      <h2 className="text-xl font-bold text-center text-gray-800">Expert en Obligations</h2>
      <div className="h-96 overflow-y-auto bg-white rounded-lg shadow p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg ${
              msg.role === 'user' 
                ? 'bg-blue-100 ml-auto max-w-[80%]' 
                : 'bg-gray-100 mr-auto max-w-[80%]'
            }`}
          >
            <p className="text-sm font-semibold mb-1">
              {msg.role === 'user' ? 'Vous' : 'Expert'}
            </p>
            <p className="text-gray-800 whitespace-pre-wrap">{msg.content}</p>
          </div>
        ))}
        {loading && (
          <div className="bg-gray-100 mr-auto max-w-[80%] p-3 rounded-lg">
            <p className="text-gray-600">En train de répondre...</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
          placeholder="Posez une question sur les obligations..."
          disabled={!wsConnected || loading}
        />
        <button 
          type="submit"
          disabled={!wsConnected || loading || !input.trim()}
          className={`px-4 py-2 rounded-lg text-white ${
            wsConnected && !loading && input.trim()
              ? 'bg-blue-500 hover:bg-blue-600' 
              : 'bg-gray-400 cursor-not-allowed'
          }`}
        >
          {loading ? 'Envoi...' : 'Envoyer'}
        </button>
      </form>
      {!wsConnected && (
        <p className="text-center text-red-500">
          Connexion au serveur perdue. Tentative de reconnexion...
        </p>
      )}
    </div>
  );
};

export default ChatComponent;