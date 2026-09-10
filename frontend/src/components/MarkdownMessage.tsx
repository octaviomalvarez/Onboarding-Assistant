"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Props = {
  content: string;
  role: "user" | "assistant";
  sources?: string[];
};

export default function MarkdownMessage({ content, role, sources }: Props) {
  const isUser = role === "user";

  return (
    <div>
      <div
        className={`max-w-[85%] rounded-2xl px-3 py-2.5 text-sm ${isUser ? "ml-auto" : ""}`}
        style={
          isUser
            ? { background: "#A100FF", color: "white", borderBottomRightRadius: "4px" }
            : { background: "#F5E6FF", color: "#3b0764", borderBottomLeftRadius: "4px" }
        }
      >
        <div
          className="prose prose-sm max-w-none"
          style={{ color: "inherit" }}
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
              strong: ({ children }) => (
                <strong style={{ color: "inherit", fontWeight: 600 }}>{children}</strong>
              ),
              ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-0.5">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-0.5">{children}</ol>,
              li: ({ children }) => <li className="leading-snug">{children}</li>,
              table: ({ children }) => (
                <div className="overflow-x-auto my-2">
                  <table className="text-xs border-collapse w-full">{children}</table>
                </div>
              ),
              th: ({ children }) => (
                <th
                  className="px-2 py-1 text-left font-semibold border"
                  style={{ borderColor: isUser ? "rgba(255,255,255,0.3)" : "#d8b4fe" }}
                >
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td
                  className="px-2 py-1 border"
                  style={{ borderColor: isUser ? "rgba(255,255,255,0.3)" : "#d8b4fe" }}
                >
                  {children}
                </td>
              ),
              code: ({ children }) => (
                <code
                  className="px-1 rounded text-xs"
                  style={{
                    background: isUser ? "rgba(255,255,255,0.2)" : "#e9d5ff",
                    color: "inherit",
                  }}
                >
                  {children}
                </code>
              ),
              hr: () => (
                <hr style={{ borderColor: isUser ? "rgba(255,255,255,0.3)" : "#d8b4fe", margin: "8px 0" }} />
              ),
              a: ({ href, children }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: isUser ? "rgba(255,255,255,0.9)" : "#7c3aed", textDecoration: "underline" }}
                >
                  {children}
                </a>
              ),
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
      </div>
      {sources && sources.length > 0 && (
        <div className="mt-1 flex flex-wrap gap-1">
          {sources.map((s) => (
            <span
              key={s}
              className="text-xs px-2 py-0.5 rounded-full"
              style={{ background: "#ede9fe", color: "#7c3aed" }}
            >
              📄 {s}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
