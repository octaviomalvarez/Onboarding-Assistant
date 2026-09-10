"use client";

import { useChatMessages } from "@/hooks/useChatMessages";
import MarkdownMessage from "./MarkdownMessage";

export default function Chat() {
  const { messages, input, setInput, loading, handleSubmit, bottomRef } = useChatMessages();

  return (
    <div className="card flex flex-col h-[600px]">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <MarkdownMessage content={msg.content} role={msg.role} sources={msg.sources} />
          </div>
        ))}
        {loading && messages[messages.length - 1]?.content === "" && (
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
          style={{ border: "1px solid #f0e6ff" }}
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
