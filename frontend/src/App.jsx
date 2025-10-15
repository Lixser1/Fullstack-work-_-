import { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [mode, setMode] = useState('sentiment');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const API_BASE = 'http://localhost:8000';
  const API_KEY = 'my_secret_api_key_12345'; // Из .env

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(
        `${API_BASE}/analyze`,
        { text: input, mode: mode },
        { headers: { 'X-API-Key': API_KEY } }
      );

      const botReply = mode === 'sentiment'
        ? `Тональность: ${response.data.result} (уверенность: ${response.data.score})`
        : `Эмоция: ${response.data.result} (уверенность: ${response.data.score})`;

      setMessages((prev) => [...prev, { role: 'bot', content: botReply }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'bot', content: 'Ошибка: не удалось проанализировать текст.' }]);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h1>Чат для анализа тональности и эмоций</h1>
      
      <div className="mode-buttons">
        <button
          className={`mode-button ${mode === 'sentiment' ? 'active' : ''}`}
          onClick={() => setMode('sentiment')}
        >
          Тональность (RU)
        </button>
        <button
          className={`mode-button ${mode === 'emotion' ? 'active' : ''}`}
          onClick={() => setMode('emotion')}
        >
          Эмоции (EN)
        </button>
      </div>
      
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <span>{msg.content}</span>
          </div>
        ))}
        {loading && <div className="loading">Анализирую...</div>}
      </div>
      
      <div className="input-container">
        <input
          placeholder="Введите текст..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend} disabled={loading}>
          Отправить
        </button>
      </div>
    </div>
  );
}

export default App;