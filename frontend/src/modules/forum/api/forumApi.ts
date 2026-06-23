import request from "@/shared/api/request";
import type {
  AttachmentItem,
  HotTopic,
  PageResult,
  PollOptionItem,
  PostCreatePayload,
  PostDetail,
  PostListItem,
  SearchSuggestion,
  Section,
  Tag
} from "../types/forum";

export function fetchSections() {
  return request.get<Section[]>("/sections");
}

export function fetchSection(id: number) {
  return request.get<Section>(`/sections/${id}`);
}

export function fetchPosts(params?: {
  section_id?: number;
  keyword?: string;
  tag_id?: number;
  is_elite?: number;
  sort?: "latest" | "hot";
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

export function createAnalysisPost(payload: PostCreatePayload) {
  return request.post<PostDetail>("/posts/analysis", payload);
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

export function fetchHotTopics(period: "daily" | "weekly" = "daily", limit = 10) {
  return request.get<HotTopic[]>("/hot-topics", { params: { period, limit } });
}

export function fetchSearchSuggestions(keyword: string, limit = 8) {
  return request.get<SearchSuggestion[]>("/search/suggestions", { params: { keyword, limit } });
}

export function fetchPostAttachments(postId: number) {
  return request.get<AttachmentItem[]>(`/posts/${postId}/attachments`);
}

export function addPostAttachment(postId: number, payload: { fileUrl: string; fileType: string }) {
  return request.post<AttachmentItem>(`/posts/${postId}/attachments`, payload);
}

export function fetchPostPoll(postId: number) {
  return request.get<PollOptionItem[]>(`/posts/${postId}/poll`);
}

export function addPostPollOption(postId: number, optionText: string) {
  return request.post<PollOptionItem>(`/posts/${postId}/poll-options`, { optionText });
}

export function votePollOption(optionId: number) {
  return request.post<{ postId: number; selectedOptionId: number; options: PollOptionItem[] }>(
    `/poll-options/${optionId}/vote`
  );
}
