"use client";

import { useState, useRef, useEffect } from "react";
import { streamMessage } from "@/lib/api";

export type Message = {
  role: "user" | "assistant";
  content: string;
  hasContext?: boolean;
  sources?: string[];
};

export function useChatMessages() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hola! Soy tu asistente de onboarding. ¿En qué te puedo ayudar hoy?" },
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

    const history = messages
      .slice(1) // skip welcome message
      .map(({ role, content }) => ({ role, content }));

    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    // Add empty assistant bubble for streaming
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);
    const assistantIdx = messages.length + 1;

    try {
      await streamMessage(
        userMessage,
        history,
        (chunk) => {
          setMessages((prev) =>
            prev.map((m, i) =>
              i === assistantIdx ? { ...m, content: m.content + chunk } : m
            )
          );
        },
        (meta) => {
          setMessages((prev) =>
            prev.map((m, i) =>
              i === assistantIdx
                ? { ...m, hasContext: meta.hasContext, sources: meta.sources }
                : m
            )
          );
        }
      );
    } catch {
      setMessages((prev) =>
        prev.map((m, i) =>
          i === assistantIdx
            ? { ...m, content: "Hubo un error al procesar tu consulta. Intentá de nuevo." }
            : m
        )
      );
    } finally {
      setLoading(false);
    }
  }

  return { messages, input, setInput, loading, handleSubmit, bottomRef };
}
