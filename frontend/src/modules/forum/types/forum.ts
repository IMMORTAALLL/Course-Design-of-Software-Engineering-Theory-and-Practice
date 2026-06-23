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
  author_nickname?: string | null;
  author_auth_level: number;
  title: string;
  summary: string;
  post_type: number;
  status: string;
  view_count: number;
  like_count: number;
  comment_count: number;
  is_elite: number;
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
  post_type?: number;
  tag_ids: number[];
}

export interface AttachmentItem {
  id: number;
  postId: number;
  fileUrl: string;
  fileType: string;
  createdAt: string;
}

export interface PollOptionItem {
  id: number;
  postId: number;
  optionText: string;
  voteCount: number;
}

export interface SearchSuggestion {
  type: string;
  label: string;
  value: string;
}

export interface HotTopic {
  id: number;
  name: string;
  tagType: string;
  postCount: number;
  hotScore: number;
}

export interface PageResult<T> {
  items: T[];
  page: number;
  size: number;
  total: number;
}
