"use client";
import { useState } from 'react';
import { askQuestion } from '../lib/api';

export default function Chat() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question) return;

    const response = await askQuestion(question);
    setHistory([...history, { question, response }]);
    setQuestion('');
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="flex items-baseline mb-4">
        <h1 className="text-3xl mr-2">🤖 RAG Demo Devoteam</h1>
        <span className="text-sm">par Leonardo Basbous</span>
      </div>

      <form onSubmit={handleSubmit}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
          placeholder="Pose ta question ici..."
        />
        <button className="mt-2 bg-blue-500 text-white px-4 py-2 rounded" type="submit">
          Envoyer
        </button>
      </form>

      <div className="mt-6">
        {history.map((item, idx) => (
          <div key={idx} className="mb-4">
            <div className="font-bold">🧑: {item.question}</div>
            <div className="text-gray-400">🤖: {item.response}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
