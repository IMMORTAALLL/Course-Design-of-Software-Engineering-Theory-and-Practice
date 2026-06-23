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

export interface InteractionStatus {
  liked: boolean;
  favorited: boolean;
  followingAuthor: boolean;
}

export interface ReportResult {
  id: number;
  status: string;
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
  level?: number;
  badgeTitle?: string | null;
  isStarred?: boolean;
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
  pending: boolean;
  createdAt: string;
}

export interface GroupCreatePayload {
  name: string;
  description?: string;
  permission: 1 | 2 | 3;
}

export interface StarFollowResult {
  following: boolean;
  starred: boolean;
}

export interface PrivateMessageItem {
  id: number;
  senderId: number;
  senderNickname: string;
  receiverId: number;
  receiverNickname: string;
  content: string;
  isRead: boolean;
  createdAt: string;
}

export interface GroupPostItem {
  id: number;
  groupId: number;
  userId: number;
  authorNickname: string;
  content: string;
  createdAt: string;
}

export interface GroupResourceItem {
  id: number;
  groupId: number;
  userId: number;
  authorNickname: string;
  title: string;
  resourceUrl: string;
  description?: string | null;
  createdAt: string;
}

export type FavoritePage = PageResult<PostListItem>;
export type FollowingFeedPage = PageResult<PostListItem>;
