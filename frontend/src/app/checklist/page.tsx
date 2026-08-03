"use client";

import { useState } from "react";
import { useChecklist } from "@/lib/useChecklist";
import type { ChecklistCategory } from "@/lib/types";

const CATEGORY_LABELS: Record<ChecklistCategory, string> = {
  accesos: "Accesos",
  capacitaciones: "Capacitaciones",
  administrativo: "Administrativo",
  equipo: "Equipo",
};

const CATEGORY_COLORS: Record<ChecklistCategory, string> = {
  accesos: "bg-blue-50 text-blue-700",
  capacitaciones: "bg-green-50 text-green-700",
  administrativo: "bg-orange-50 text-orange-700",
  equipo: "bg-purple-50 text-purple-700",
};

export default function ChecklistPage() {
  const { items, toggle } = useChecklist();
  const [activeWeek, setActiveWeek] = useState<1 | 2>(1);

  const filtered = items.filter((i) => i.week === activeWeek);
  const done = filtered.filter((i) => i.completed).length;
  const total = filtered.length;

  return (
    <div className="p-8 max-w-2xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-gray-900">Checklist de onboarding</h1>
        <p className="text-gray-400 text-sm mt-1">Completá estas tareas durante tus primeras dos semanas</p>
      </div>

      {/* Selector semana */}
      <div className="flex gap-2 mb-6">
        {([1, 2] as const).map((w) => (
          <button
            key={w}
            onClick={() => setActiveWeek(w)}
            className="px-4 py-2 rounded-xl text-sm font-medium transition-all"
            style={
              activeWeek === w
                ? { background: "#A100FF", color: "white" }
                : { background: "white", color: "#6b7280", border: "1px solid #f0e6ff" }
            }
          >
            Semana {w}
          </button>
        ))}
        <span className="ml-auto self-center text-sm text-gray-400">
          {done}/{total} completadas
        </span>
      </div>

      {/* Lista */}
      <ul className="space-y-2">
        {filtered.map((item) => (
          <li
            key={item.id}
            onClick={() => toggle(item.id)}
            className={`card p-4 cursor-pointer transition-all hover:shadow-md ${
              item.completed ? "opacity-50" : ""
            }`}
          >
            <div className="flex items-start gap-3">
              <div
                className="mt-0.5 w-5 h-5 rounded border-2 flex-shrink-0 flex items-center justify-center transition-colors"
                style={
                  item.completed
                    ? { background: "#A100FF", borderColor: "#A100FF" }
                    : { borderColor: "#d8b4fe" }
                }
              >
                {item.completed && (
                  <svg className="w-3 h-3" viewBox="0 0 12 12" fill="none">
                    <path d="M2 6l3 3 5-5" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className={`text-sm font-medium ${item.completed ? "line-through text-gray-400" : "text-gray-800"}`}>
                  {item.title}
                </p>
                <p className="text-xs text-gray-400 mt-0.5">{item.description}</p>
                <div className="flex items-center gap-2 mt-2">
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${CATEGORY_COLORS[item.category]}`}>
                    {CATEGORY_LABELS[item.category]}
                  </span>
                  <span className="text-xs text-gray-400">Día {item.dueDay}</span>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
