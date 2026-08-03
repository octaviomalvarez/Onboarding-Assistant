"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  {
    href: "/",
    label: "Inicio",
    icon: (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M2 6.5L8 2l6 4.5V14a.5.5 0 0 1-.5.5h-3.75v-3.25h-3.5V14.5H2.5A.5.5 0 0 1 2 14V6.5z" stroke="currentColor" strokeWidth="1.25" strokeLinejoin="round"/>
      </svg>
    ),
  },
  {
    href: "/checklist",
    label: "Checklist",
    icon: (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <rect x="2" y="2" width="12" height="12" rx="2" stroke="currentColor" strokeWidth="1.25"/>
        <path d="M5 8l2 2 4-4" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round"/>
      </svg>
    ),
  },
  {
    href: "/contactos",
    label: "Contactos",
    icon: (
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="5.5" r="2.5" stroke="currentColor" strokeWidth="1.25"/>
        <path d="M2.5 13.5c0-2.485 2.462-4.5 5.5-4.5s5.5 2.015 5.5 4.5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round"/>
      </svg>
    ),
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 bg-white flex flex-col min-h-screen" style={{ borderRight: "1px solid #f0e6ff", boxShadow: "1px 0 8px rgba(161,0,255,0.05)" }}>
      {/* Header */}
      <div className="px-5 py-5" style={{ borderBottom: "1px solid #f0e6ff" }}>
        <p className="text-xs font-bold tracking-widest uppercase" style={{ color: "#A100FF" }}>
          Accenture
        </p>
        <p className="text-sm font-semibold text-gray-800 mt-0.5">Onboarding Assistant</p>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-3 space-y-0.5">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-xl text-sm transition-colors ${
                active ? "font-medium" : "text-gray-500 hover:bg-gray-50 hover:text-gray-800"
              }`}
              style={
                active
                  ? { background: "#F5E6FF", color: "#A100FF" }
                  : undefined
              }
            >
              <span className={active ? "" : "text-gray-400"}>{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* User */}
      <div className="p-4" style={{ borderTop: "1px solid #f0e6ff" }}>
        <div className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
            style={{ background: "#A100FF" }}
          >
            OA
          </div>
          <div className="min-w-0">
            <p className="text-xs font-medium text-gray-700 truncate">Octavio Alvarez</p>
            <p className="text-xs text-gray-400 truncate">Torre de Data</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
