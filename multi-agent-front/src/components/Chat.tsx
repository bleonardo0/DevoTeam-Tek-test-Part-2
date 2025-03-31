import { useState } from "react";

interface Message {
  sender: "user" | "bot";
  text: string;
}

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const newMessages: Message[] = [
      ...messages,
      { sender: "user", text: question }
    ];
    setMessages(newMessages);
    setLoading(true);
    setQuestion("");

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      const data = await res.json();
      setMessages([...newMessages, { sender: "bot", text: data.response }]);
    } catch (err) {
      setMessages([...newMessages, { sender: "bot", text: "❌ Erreur lors de la réponse." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 font-sans">
      <div className="max-w-2xl mx-auto">
        <div className="mb-6 flex items-center gap-3">
          <div className="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center text-white text-xl">🧠</div>
          <h1 className="text-2xl font-bold">Multi-Agent Devoteam</h1>
        </div>

        <div className="space-y-4 mb-6">
          {messages.map((msg, idx) => (
            <div key={idx} className={`p-3 rounded-lg max-w-[80%] ${msg.sender === "user" ? "ml-auto bg-red-700" : "bg-gray-700"}`}>
              {msg.text}
            </div>
          ))}
          {loading && <div className="text-sm text-gray-400">🤖 Le bot réfléchit...</div>}
        </div>

        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="flex-1 px-4 py-2 rounded bg-gray-800 border border-gray-600 focus:outline-none"
            placeholder="Pose ta question ici..."
          />
          <button className="bg-red-600 hover:bg-red-500 px-4 py-2 rounded text-white" type="submit">
            Envoyer
          </button>
        </form>
      </div>
    </div>
  );
}
