// ================== Payments Start ===================
export type PaymentMethod = {
  id: string;
  name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  image_url: string;
};

// ================== Payments End ====================
// ================== Catalog Start ===================
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

// ================== Catalog End ====================

// ================== Vendor Start ====================
export type SubscriptionPlan = {
  id: string;
  name: string;
  monthly_price: number;
  yearly_price: number;
  description: string;
  features: string[];
  button_text: string;
  href: string;
  is_popular: boolean;
};

export type Vendor = {
  id: string;
  name: string;
  email: string;
  phone: string;
  address: string;
};
// ================== Vendor End ====================
