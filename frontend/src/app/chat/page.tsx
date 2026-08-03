import Chat from "@/components/Chat";

export default function ChatPage() {
  return (
    <div className="p-8 max-w-2xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-gray-900">Asistente</h1>
        <p className="text-gray-500 text-sm mt-1">Hacé preguntas sobre accesos, capacitaciones, procesos y más</p>
      </div>
      <Chat />
    </div>
  );
}
