"use client";

import { useState, useRef, useEffect } from "react";
import { sendMessage } from "@/lib/api";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    function handleOpen() { setOpen(true); }
    window.addEventListener("open-chat-widget", handleOpen);
    return () => window.removeEventListener("open-chat-widget", handleOpen);
  }, []);
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hola! Soy tu asistente de onboarding. ¿En qué te puedo ayudar hoy?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open) bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

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

  function formatMessage(text: string): string {
    return text
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br/>");
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">

      {/* Panel de chat */}
      {open && (
        <div
          className="card flex flex-col transition-all duration-200"
          style={{
            boxShadow: "0 8px 32px rgba(161,0,255,0.18)",
            width: expanded ? "520px" : "320px",
            height: expanded ? "540px" : "460px",
          }}
        >
          {/* Header del panel */}
          <div
            className="flex items-center justify-between px-4 py-3 rounded-t-2xl"
            style={{ background: "#A100FF" }}
          >
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-white opacity-80" />
              <p className="text-sm font-medium text-white">Asistente de Onboarding</p>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setExpanded((v) => !v)}
                className="text-white opacity-70 hover:opacity-100 transition-opacity"
                aria-label={expanded ? "Reducir" : "Expandir"}
              >
                {expanded ? (
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M9 1h4v4M5 13H1V9M13 9v4H9M1 5V1h4" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                ) : (
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M1 5V1h4M9 1h4v4M13 9v4H9M5 13H1V9" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
              <button
                onClick={() => setOpen(false)}
                className="text-white opacity-70 hover:opacity-100 transition-opacity text-lg leading-none"
              >
                ×
              </button>
            </div>
          </div>

          {/* Mensajes */}
          <div className="flex-1 overflow-y-auto p-3 space-y-3">
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className="max-w-[85%] rounded-2xl px-3 py-2 text-sm whitespace-pre-wrap"
                  style={
                    msg.role === "user"
                      ? { background: "#A100FF", color: "white", borderBottomRightRadius: "4px" }
                      : { background: "#F5E6FF", color: "#3b0764", borderBottomLeftRadius: "4px" }
                  }
                  dangerouslySetInnerHTML={{ __html: formatMessage(msg.content) }}
                />
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div
                  className="rounded-2xl px-3 py-2 text-sm"
                  style={{ background: "#F5E6FF", color: "#A100FF", borderBottomLeftRadius: "4px" }}
                >
                  Escribiendo...
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <form
            onSubmit={handleSubmit}
            className="p-3 flex gap-2"
            style={{ borderTop: "1px solid #f0e6ff" }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribí tu pregunta..."
              disabled={loading}
              className="flex-1 rounded-xl px-3 py-1.5 text-sm focus:outline-none disabled:opacity-50"
              style={{ border: "1px solid #f0e6ff" }}
              onFocus={(e) => (e.target.style.borderColor = "#A100FF")}
              onBlur={(e) => (e.target.style.borderColor = "#f0e6ff")}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="text-white rounded-xl px-3 py-1.5 text-sm font-medium transition-opacity hover:opacity-90 disabled:opacity-40"
              style={{ background: "#A100FF" }}
            >
              →
            </button>
          </form>
        </div>
      )}

      {/* Botón flotante */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-13 h-13 rounded-full flex items-center justify-center text-white transition-transform hover:scale-105 active:scale-95"
        style={{
          background: "#A100FF",
          boxShadow: "0 4px 20px rgba(161,0,255,0.35)",
          width: "52px",
          height: "52px",
        }}
        aria-label="Abrir asistente"
      >
        {open ? (
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M5 5l10 10M15 5L5 15" stroke="white" strokeWidth="2" strokeLinecap="round" />
          </svg>
        ) : (
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M17 11.667A1.667 1.667 0 0 1 15.333 13.333H5.833L3 16.667V4.333A1.667 1.667 0 0 1 4.667 2.667h10.666A1.667 1.667 0 0 1 17 4.333v7.334z" stroke="white" strokeWidth="1.5" strokeLinejoin="round"/>
          </svg>
        )}
      </button>

    </div>
  );
}
