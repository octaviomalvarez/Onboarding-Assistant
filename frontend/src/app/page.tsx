"use client";

import Link from "next/link";
import { useChecklist } from "@/lib/useChecklist";

function openChatWidget() {
  window.dispatchEvent(new CustomEvent("open-chat-widget"));
}

const CATEGORY_LABELS: Record<string, string> = {
  accesos: "Accesos",
  capacitaciones: "Capacitaciones",
  administrativo: "Administrativo",
  equipo: "Equipo",
};

function SectionLabel({ label }: { label: string }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <span className="w-1 h-4 rounded-full inline-block" style={{ background: "#A100FF" }} />
      <p className="text-xs font-semibold uppercase tracking-widest" style={{ color: "#A100FF" }}>
        {label}
      </p>
    </div>
  );
}

export default function Dashboard() {
  const { items } = useChecklist();

  const total = items.length;
  const completed = items.filter((i) => i.completed).length;
  const percent = Math.round((completed / total) * 100);

  const week1 = items.filter((i) => i.week === 1);
  const week2 = items.filter((i) => i.week === 2);
  const week1Done = week1.filter((i) => i.completed).length;
  const week2Done = week2.filter((i) => i.completed).length;

  const pending = items.filter((i) => !i.completed).slice(0, 3);

  return (
    <div className="p-8 max-w-3xl">

      {/* Bienvenida */}
      <div
        className="card p-6 flex items-center justify-between mb-8"
        style={{ background: "linear-gradient(135deg, #ffffff 60%, #F5E6FF 100%)" }}
      >
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Bienvenido, Octavio</h1>
          <p className="text-gray-400 text-sm mt-1">Torre de Data · Semana 1 de incorporación</p>
        </div>
        <div
          className="w-12 h-12 rounded-full flex items-center justify-center text-sm font-bold text-white flex-shrink-0"
          style={{ background: "#A100FF" }}
        >
          OA
        </div>
      </div>

      {/* Progreso */}
      <section className="mb-6">
        <SectionLabel label="Tu progreso" />
        <div className="card p-6 mb-4" style={{ borderLeft: "3px solid #A100FF" }}>
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-medium text-gray-700">Progreso general</p>
            <p className="text-sm font-semibold" style={{ color: "#A100FF" }}>{percent}%</p>
          </div>
          <div className="w-full rounded-full h-2.5" style={{ background: "#EDD9FF" }}>
            <div
              className="h-2.5 rounded-full transition-all duration-500"
              style={{ width: `${percent}%`, background: "#A100FF" }}
            />
          </div>
          <p className="text-xs text-gray-400 mt-2">{completed} de {total} tareas completadas</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          {[
            { label: "Semana 1", done: week1Done, total: week1.length, color: "#A100FF" },
            { label: "Semana 2", done: week2Done, total: week2.length, color: "#7C00CC" },
          ].map((w) => (
            <div key={w.label} className="card p-5" style={{ borderLeft: `3px solid ${w.color}` }}>
              <p className="text-xs font-semibold uppercase tracking-widest" style={{ color: w.color }}>{w.label}</p>
              <p className="text-2xl font-semibold text-gray-900 mt-1">
                {w.done}<span className="text-gray-200 font-normal">/{w.total}</span>
              </p>
              <p className="text-xs text-gray-400 mt-0.5">tareas completadas</p>
            </div>
          ))}
        </div>
      </section>

      {/* Próximas tareas */}
      <section className="mb-4">
        <SectionLabel label="Próximas tareas" />
        <div className="card p-6" style={{ borderLeft: "3px solid #EDD9FF" }}>
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm font-medium text-gray-700">Pendientes</p>
            <Link href="/checklist" className="text-xs hover:underline" style={{ color: "#A100FF" }}>
              Ver todas →
            </Link>
          </div>
          {pending.length === 0 ? (
            <p className="text-sm text-gray-400">Completaste todas las tareas. ¡Excelente!</p>
          ) : (
            <ul className="space-y-3">
              {pending.map((item) => (
                <li key={item.id} className="flex items-start gap-3">
                  <span className="mt-0.5 w-4 h-4 rounded border flex-shrink-0" style={{ borderColor: "#d8b4fe" }} />
                  <div>
                    <p className="text-sm text-gray-800">{item.title}</p>
                    <p className="text-xs text-gray-400 mt-0.5">
                      {CATEGORY_LABELS[item.category]} · Día {item.dueDay}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </section>

      {/* CTA */}
      <section>
        <SectionLabel label="Asistente" />
        <div className="card p-5 flex items-center justify-between" style={{ background: "#F5E6FF", border: "1px solid #EDD9FF", borderLeft: "3px solid #A100FF" }}>
          <div>
            <p className="text-sm font-medium" style={{ color: "#7C00CC" }}>¿Tenés alguna pregunta?</p>
            <p className="text-xs mt-0.5" style={{ color: "#A100FF" }}>El asistente puede ayudarte con accesos, capacitaciones y más</p>
          </div>
          <button
            onClick={openChatWidget}
            className="text-sm px-4 py-2 rounded-xl text-white transition-opacity hover:opacity-90 whitespace-nowrap"
            style={{ background: "#A100FF" }}
          >
            Abrir chat
          </button>
        </div>
      </section>

    </div>
  );
}
