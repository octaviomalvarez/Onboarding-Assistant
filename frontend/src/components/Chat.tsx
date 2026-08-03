"use client";

import { useState, useRef, useEffect } from "react";
import { sendMessage } from "@/lib/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hola! Soy tu asistente de onboarding. ¿En qué te puedo ayudar hoy?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const response = await sendMessage(userMessage);
      setMessages((prev) => [...prev, { role: "assistant", content: response }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Hubo un error al procesar tu consulta. Intentá de nuevo." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card flex flex-col h-[600px]">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className="max-w-[80%] rounded-2xl px-4 py-2.5 text-sm"
              style={
                msg.role === "user"
                  ? { background: "#A100FF", color: "white", borderBottomRightRadius: "4px" }
                  : { background: "#F5E6FF", color: "#3b0764", borderBottomLeftRadius: "4px" }
              }
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="rounded-2xl px-4 py-2.5 text-sm" style={{ background: "#F5E6FF", color: "#A100FF", borderBottomLeftRadius: "4px" }}>
              Escribiendo...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-3 flex gap-2" style={{ borderTop: "1px solid #f0e6ff" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribí tu pregunta..."
          disabled={loading}
          className="flex-1 rounded-xl px-4 py-2 text-sm focus:outline-none disabled:opacity-50"
          style={{ border: "1px solid #f0e6ff", outline: "none" }}
          onFocus={(e) => (e.target.style.borderColor = "#A100FF")}
          onBlur={(e) => (e.target.style.borderColor = "#f0e6ff")}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="text-white rounded-xl px-4 py-2 text-sm font-medium transition-opacity hover:opacity-90 disabled:opacity-40"
          style={{ background: "#A100FF" }}
        >
          Enviar
        </button>
      </form>
    </div>
  );
}
