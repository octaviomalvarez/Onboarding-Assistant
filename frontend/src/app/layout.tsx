import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Sidebar from "@/components/Sidebar";
import ChatWidget from "@/components/ChatWidget";
import { RoleProvider } from "@/contexts/RoleContext";
import RoleSelector from "@/components/RoleSelector";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Onboarding Assistant",
  description: "Tu guía de incorporación en Accenture",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={inter.className}>
      <body className="bg-gray-50 text-gray-900 antialiased flex">
        <RoleProvider>
          <RoleSelector />
          <Sidebar />
          <main className="flex-1 min-h-screen">{children}</main>
          <ChatWidget />
        </RoleProvider>
      </body>
    </html>
  );
}
