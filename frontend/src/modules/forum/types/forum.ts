export interface Tag {
  id: number;
  name: string;
  tag_type: "STOCK" | "FUND" | "TOPIC" | string;
}

export interface Section {
  id: number;
  name: string;
  description?: string;
  sort_order: number;
  is_active: number;
  created_at: string;
}

export interface PostListItem {
  id: number;
  section_id: number;
  section_name: string;
  user_id: number;
  title: string;
  summary: string;
  status: string;
  view_count: number;
  like_count: number;
  comment_count: number;
  created_at: string;
  tags: Tag[];
}

export interface PostDetail extends PostListItem {
  content: string;
  updated_at: string;
}

export interface PostCreatePayload {
  section_id: number;
  title: string;
  content: string;
  tag_ids: number[];
}

export interface PageResult<T> {
  items: T[];
  page: number;
  size: number;
  total: number;
}
