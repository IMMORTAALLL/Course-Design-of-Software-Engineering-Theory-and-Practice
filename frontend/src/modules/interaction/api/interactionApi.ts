import request from "@/shared/api/request";
import type {
  CommentItem,
  FavoritePage,
  FollowResult,
  FollowingFeedPage,
  GroupCreatePayload,
  GroupItem,
  InteractionStatus,
  NotificationItem,
  ReportResult,
  ToggleResult,
  UserBrief
} from "../types/interaction";

export function fetchComments(postId: number) {
  return request.get<CommentItem[]>(`/posts/${postId}/comments`);
}

export function createComment(postId: number, content: string) {
  return request.post<CommentItem>(`/posts/${postId}/comments`, { content });
}

export function createReply(commentId: number, content: string) {
  return request.post<CommentItem>(`/comments/${commentId}/replies`, { content });
}

export function deleteComment(commentId: number) {
  return request.delete<{ id: number }>(`/comments/${commentId}`);
}

export function togglePostLike(postId: number) {
  return request.post<ToggleResult>(`/posts/${postId}/like`);
}

export function fetchPostInteractionStatus(postId: number) {
  return request.get<InteractionStatus>(`/posts/${postId}/interaction-status`);
}

export function toggleCommentLike(commentId: number) {
  return request.post<ToggleResult>(`/comments/${commentId}/like`);
}

export function reportPost(postId: number, reason: string) {
  return request.post<ReportResult>(`/posts/${postId}/report`, { reason });
}

export function reportComment(commentId: number, reason: string) {
  return request.post<ReportResult>(`/comments/${commentId}/report`, { reason });
}

export function togglePostFavorite(postId: number) {
  return request.post<ToggleResult>(`/posts/${postId}/favorite`);
}

export function fetchFavorites(page = 1, size = 10) {
  return request.get<FavoritePage>("/me/favorites", { params: { page, size } });
}

export function toggleFollow(userId: number) {
  return request.post<FollowResult>(`/users/${userId}/follow`);
}

export function fetchFollowers(userId: number) {
  return request.get<UserBrief[]>(`/users/${userId}/followers`);
}

export function fetchFollowing(userId: number) {
  return request.get<UserBrief[]>(`/users/${userId}/following`);
}

export function fetchFollowingFeed(page = 1, size = 10) {
  return request.get<FollowingFeedPage>("/feed/following", { params: { page, size } });
}

export function fetchNotifications() {
  return request.get<NotificationItem[]>("/me/notifications");
}

export function markNotificationRead(id: number) {
  return request.put<NotificationItem>(`/me/notifications/${id}/read`);
}

export function fetchGroups() {
  return request.get<GroupItem[]>("/groups");
}

export function createGroup(payload: GroupCreatePayload) {
  return request.post<GroupItem>("/groups", payload);
}

export function fetchGroup(id: number) {
  return request.get<GroupItem>(`/groups/${id}`);
}

export function joinGroup(id: number) {
  return request.post<GroupItem>(`/groups/${id}/join`);
}

export function leaveGroup(id: number) {
  return request.delete<GroupItem>(`/groups/${id}/members/me`);
}
