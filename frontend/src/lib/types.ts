export type ChecklistCategory = "accesos" | "capacitaciones" | "administrativo" | "equipo";

export type ChecklistItem = {
  id: string;
  title: string;
  description: string;
  category: ChecklistCategory;
  week: 1 | 2;
  completed: boolean;
  dueDay: number;
};

export type Contact = {
  id: string;
  name: string;
  role: string;
  email: string;
  area: string;
};
