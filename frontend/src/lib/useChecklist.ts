"use client";

import { useState, useEffect } from "react";
import { CHECKLIST_ITEMS } from "./mock-data";
import type { ChecklistItem } from "./types";

const STORAGE_KEY = "onboarding_checklist";

export function useChecklist() {
  const [items, setItems] = useState<ChecklistItem[]>(CHECKLIST_ITEMS);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const completedIds: string[] = JSON.parse(stored);
      setItems(
        CHECKLIST_ITEMS.map((item) => ({
          ...item,
          completed: completedIds.includes(item.id),
        }))
      );
    }
  }, []);

  function toggle(id: string) {
    setItems((prev) => {
      const updated = prev.map((item) =>
        item.id === id ? { ...item, completed: !item.completed } : item
      );
      const completedIds = updated.filter((i) => i.completed).map((i) => i.id);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(completedIds));
      return updated;
    });
  }

  return { items, toggle };
}
