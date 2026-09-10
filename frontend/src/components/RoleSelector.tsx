"use client";

import { useRole } from "@/contexts/RoleContext";

const ROLES = [
  { id: "Junior", label: "Junior", desc: "Primeros años en la industria" },
  { id: "Senior", label: "Senior", desc: "Experiencia consolidada" },
  { id: "Lead", label: "Lead / Manager", desc: "Liderazgo de equipo" },
  { id: "Data Engineer", label: "Data Engineer", desc: "Pipelines y arquitectura de datos" },
  { id: "Data Scientist", label: "Data Scientist", desc: "Modelos y análisis avanzado" },
];

export default function RoleSelector() {
  const { role, setRole } = useRole();

  if (role) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4">
        <div className="mb-6 text-center">
          <p className="text-xs font-bold tracking-widest uppercase mb-1" style={{ color: "#A100FF" }}>
            Accenture · Torre de Data
          </p>
          <h2 className="text-xl font-semibold text-gray-900">¿Cuál es tu rol?</h2>
          <p className="text-sm text-gray-400 mt-1">
            Personalizamos tu onboarding según tu perfil
          </p>
        </div>
        <div className="space-y-2">
          {ROLES.map((r) => (
            <button
              key={r.id}
              onClick={() => setRole(r.id)}
              className="w-full text-left px-4 py-3 rounded-xl border-2 transition-all hover:shadow-sm"
              style={{ borderColor: "#f0e6ff" }}
              onMouseEnter={(e) => (e.currentTarget.style.borderColor = "#A100FF")}
              onMouseLeave={(e) => (e.currentTarget.style.borderColor = "#f0e6ff")}
            >
              <p className="text-sm font-medium text-gray-800">{r.label}</p>
              <p className="text-xs text-gray-400">{r.desc}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
