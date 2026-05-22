import request from "@/shared/api/request";
import type { PageResult, PostCreatePayload, PostDetail, PostListItem, Section, Tag } from "../types/forum";

export function fetchSections() {
  return request.get<Section[]>("/sections");
}

export function fetchSection(id: number) {
  return request.get<Section>(`/sections/${id}`);
}

export function fetchPosts(params?: {
  section_id?: number;
  keyword?: string;
  page?: number;
  size?: number;
}) {
  return request.get<PageResult<PostListItem>>("/posts", { params });
}

export function fetchPost(id: number) {
  return request.get<PostDetail>(`/posts/${id}`);
}

export function createPost(payload: PostCreatePayload) {
  return request.post<PostDetail>("/posts", payload);
}

export function fetchTags(tagType?: string) {
  return request.get<Tag[]>("/tags", { params: tagType ? { tag_type: tagType } : undefined });
}

export function searchPosts(keyword: string, page = 1, size = 10) {
  return request.get<PageResult<PostListItem>>("/search/posts", {
    params: { keyword, page, size }
  });
}

export function fetchHotPosts(limit = 10) {
  return request.get<PostListItem[]>("/posts/hot", { params: { limit } });
}
