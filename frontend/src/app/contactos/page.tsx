import { CONTACTS } from "@/lib/mock-data";

export default function ContactosPage() {
  return (
    <div className="p-8 max-w-2xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-gray-900">Contactos clave</h1>
        <p className="text-gray-400 text-sm mt-1">Las personas que te van a ayudar durante el onboarding</p>
      </div>

      <ul className="space-y-3">
        {CONTACTS.map((contact) => (
          <li key={contact.id} className="card p-4 flex items-center gap-4">
            <div
              className="w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
              style={{ background: "#A100FF" }}
            >
              {contact.name.split(" ").map((n) => n[0]).join("").slice(0, 2)}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900">{contact.name}</p>
              <p className="text-xs text-gray-500">{contact.role}</p>
              <p className="text-xs text-gray-400">{contact.area}</p>
            </div>
            <a
              href={`mailto:${contact.email}`}
              className="text-xs hover:underline whitespace-nowrap"
              style={{ color: "#A100FF" }}
            >
              {contact.email}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
