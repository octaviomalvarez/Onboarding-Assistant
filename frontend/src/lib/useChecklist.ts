"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchChecklist, updateChecklistItem } from "./api";
import { useRole } from "@/contexts/RoleContext";
import type { ChecklistItem } from "./types";

export function useChecklist() {
  const { role } = useRole();
  const [items, setItems] = useState<ChecklistItem[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setItems(await fetchChecklist(role ?? undefined));
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [role]);

  useEffect(() => { load(); }, [load]);

  async function toggle(id: string) {
    const item = items.find((i) => i.id === id);
    if (!item) return;
    const newVal = !item.completed;
    setItems((prev) => prev.map((i) => (i.id === id ? { ...i, completed: newVal } : i)));
    try {
      await updateChecklistItem(id, newVal);
    } catch {
      setItems((prev) => prev.map((i) => (i.id === id ? { ...i, completed: item.completed } : i)));
    }
  }

  return { items, toggle, loading };
}
