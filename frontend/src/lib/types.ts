export type ChecklistCategory = "accesos" | "capacitaciones" | "administrativo" | "equipo";

export type ChecklistItem = {
  id: string;
  title: string;
  description: string;
  category: ChecklistCategory;
  week: 1 | 2;
  completed: boolean;
  dueDay: number;
  roles?: string;
};

export type Contact = {
  id: string;
  name: string;
  role: string;
  email: string;
  area: string;
};

export type ChatApiResponse = {
  response: string;
  has_context: boolean;
  provider: string;
  sources: string[];
};
