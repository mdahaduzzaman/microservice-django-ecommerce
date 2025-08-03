export type Category = {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  parent: null | Category;
  subcategories_count: number;
};

export type Product = {
  id: string;
  category: string;
  title: string;
  slug: string;
  description: string | null;
  price: number;
};
