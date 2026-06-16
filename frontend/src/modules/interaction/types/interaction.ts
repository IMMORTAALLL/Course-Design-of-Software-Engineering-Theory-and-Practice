import type { PageResult, PostListItem } from "@/modules/forum/types/forum";

export interface CommentItem {
  id: number;
  postId: number;
  userId: number;
  parentId?: number | null;
  authorNickname: string;
  authorAuthLevel: number;
  content: string;
  likeCount: number;
  createdAt: string;
  replies: CommentItem[];
}

export interface ToggleResult {
  active: boolean;
  count: number;
}

export interface FollowResult {
  following: boolean;
  followerCount: number;
}

export interface UserBrief {
  id: number;
  nickname?: string | null;
  avatarUrl?: string | null;
  authLevel: number;
  influenceScore: number;
}

export interface NotificationItem {
  id: number;
  title: string;
  content: string;
  notificationType: string;
  targetType?: string | null;
  targetId?: number | null;
  isRead: boolean;
  createdAt: string;
}

export interface GroupItem {
  id: number;
  name: string;
  description?: string | null;
  permission: number;
  creatorId: number;
  creatorNickname: string;
  memberCount: number;
  joined: boolean;
  createdAt: string;
}

export interface GroupCreatePayload {
  name: string;
  description?: string;
  permission: 1 | 2 | 3;
}

export type FavoritePage = PageResult<PostListItem>;
export type FollowingFeedPage = PageResult<PostListItem>;
