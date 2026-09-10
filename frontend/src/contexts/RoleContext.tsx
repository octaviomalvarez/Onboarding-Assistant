"use client";

import { createContext, useContext, useState, useEffect } from "react";

type RoleContextType = {
  role: string | null;
  setRole: (role: string) => void;
};

const RoleContext = createContext<RoleContextType>({ role: null, setRole: () => {} });

export function RoleProvider({ children }: { children: React.ReactNode }) {
  const [role, setRoleState] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("onboarding_role");
    if (stored) setRoleState(stored);
  }, []);

  function setRole(r: string) {
    localStorage.setItem("onboarding_role", r);
    setRoleState(r);
  }

  return (
    <RoleContext.Provider value={{ role, setRole }}>
      {children}
    </RoleContext.Provider>
  );
}

export function useRole() {
  return useContext(RoleContext);
}
