import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [status, setStatus] = useState('offline');

  const toggleBot = (newStatus) => {
    axios.post('http://127.0.0.1:8000/api/toggle-bot/', { status: newStatus })
      .then((response) => {
        console.log(response.data);
        if (response.data.status === 'Bot started') {
          setStatus('online');
        } else if (response.data.status === 'Bot stopped') {
          setStatus('offline');
        }
      })
      .catch((error) => {
        console.error('Error toggling bot:', error);
      });
  };

  return (
    <div className="App">
      <h1>Discord Bot Status: {status}</h1>
      <button onClick={() => toggleBot('start')}>Start Bot</button>
      <button onClick={() => toggleBot('stop')}>Stop Bot</button>
    </div>
  );
}

export default App;