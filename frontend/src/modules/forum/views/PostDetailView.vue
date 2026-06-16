<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink, useRoute } from "vue-router";

import CommentEditor from "@/modules/interaction/components/CommentEditor.vue";
import CommentList from "@/modules/interaction/components/CommentList.vue";
import FavoriteButton from "@/modules/interaction/components/FavoriteButton.vue";
import FollowButton from "@/modules/interaction/components/FollowButton.vue";
import LikeButton from "@/modules/interaction/components/LikeButton.vue";
import {
  createComment,
  fetchComments,
  fetchPostInteractionStatus,
  reportPost
} from "@/modules/interaction/api/interactionApi";
import { hasAuthToken } from "@/modules/auth/stores/authStore";
import type { CommentItem, InteractionStatus } from "@/modules/interaction/types/interaction";
import { fetchPost } from "../api/forumApi";
import TagBadge from "../components/TagBadge.vue";
import type { PostDetail } from "../types/forum";

const route = useRoute();
const postId = computed(() => Number(route.params.id));
const post = ref<PostDetail | null>(null);
const comments = ref<CommentItem[]>([]);
const loading = ref(true);
const commentError = ref("");
const reportReason = ref("");
const reportMessage = ref("");
const reportError = ref("");
const reporting = ref(false);
const interactionStatus = ref<InteractionStatus>({
  liked: false,
  favorited: false,
  followingAuthor: false
});

function resetInteractionStatus() {
  interactionStatus.value = {
    liked: false,
    favorited: false,
    followingAuthor: false
  };
}

async function loadPost() {
  loading.value = true;
  resetInteractionStatus();
  reportMessage.value = "";
  reportError.value = "";
  try {
    const [postData, commentData] = await Promise.all([
      fetchPost(postId.value),
      fetchComments(postId.value)
    ]);
    post.value = postData;
    comments.value = commentData;
    if (hasAuthToken()) {
      try {
        interactionStatus.value = await fetchPostInteractionStatus(postId.value);
      } catch {
        resetInteractionStatus();
      }
    }
  } finally {
    loading.value = false;
  }
}

async function submitComment(content: string) {
  commentError.value = "";
  try {
    await createComment(postId.value, content);
    const [postData, commentData] = await Promise.all([
      fetchPost(postId.value),
      fetchComments(postId.value)
    ]);
    post.value = postData;
    comments.value = commentData;
  } catch (error) {
    commentError.value = error instanceof Error ? error.message : "评论发布失败";
  }
}

async function submitPostReport() {
  const reason = reportReason.value.trim();
  if (!reason) {
    reportError.value = "请填写举报原因。";
    return;
  }
  reporting.value = true;
  reportError.value = "";
  reportMessage.value = "";
  try {
    await reportPost(postId.value, reason);
    reportReason.value = "";
    reportMessage.value = "举报已提交";
  } catch (error) {
    reportError.value = error instanceof Error ? error.message : "举报提交失败";
  } finally {
    reporting.value = false;
  }
}

onMounted(loadPost);
watch(postId, loadPost);
</script>

<template>
  <article class="page">
    <div v-if="loading" class="empty">正在加载帖子详情...</div>
    <template v-else-if="post">
      <div class="panel detail">
        <div class="meta">
          <RouterLink :to="`/sections/${post.section_id}`">{{ post.section_name }}</RouterLink>
          <RouterLink :to="`/users/${post.user_id}`">{{ post.author_nickname || "社区用户" }}</RouterLink>
          <span>{{ post.author_auth_level === 2 ? "专业认证" : post.author_auth_level === 1 ? "实名认证" : "基础用户" }}</span>
          <span v-if="post.post_type === 2">长文分析</span>
          <span v-if="post.is_elite">精华</span>
          <span>{{ new Date(post.created_at).toLocaleString() }}</span>
          <span>浏览 {{ post.view_count }}</span>
          <span>点赞 {{ post.like_count }}</span>
          <span>评论 {{ post.comment_count }}</span>
        </div>
        <h1>{{ post.title }}</h1>
        <div class="tag-row" v-if="post.tags.length">
          <TagBadge v-for="tag in post.tags" :key="tag.id" :tag="tag" />
        </div>
        <div class="risk">内容仅供交流，不构成投资建议。请结合自身风险承受能力独立判断。</div>
        <p class="content">{{ post.content }}</p>
      </div>

      <div class="panel action-panel">
        <div class="action-row">
          <LikeButton :post-id="post.id" :initial-count="post.like_count" :initial-active="interactionStatus.liked" />
          <FavoriteButton :post-id="post.id" :initial-active="interactionStatus.favorited" />
          <FollowButton :user-id="post.user_id" :initial-following="interactionStatus.followingAuthor" />
        </div>
        <form class="report-form" @submit.prevent="submitPostReport">
          <input v-model="reportReason" maxlength="255" placeholder="举报原因" />
          <button class="action-button" type="submit" :disabled="reporting">举报</button>
          <span v-if="reportMessage" class="inline-success">{{ reportMessage }}</span>
          <span v-if="reportError" class="inline-error">{{ reportError }}</span>
        </form>
      </div>

      <section class="panel comments">
        <div class="comment-heading">
          <h2>评论区</h2>
          <span>{{ post.comment_count }} 条评论</span>
        </div>
        <CommentEditor @submit="submitComment" />
        <p v-if="commentError" class="inline-error">{{ commentError }}</p>
        <CommentList :comments="comments" @refresh="loadPost" />
      </section>
    </template>
    <div v-else class="empty">帖子不存在或已删除。</div>
  </article>
</template>

<style scoped>
.detail {
  display: grid;
  gap: 18px;
}

h1 {
  margin: 0;
  font-size: 30px;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.risk {
  padding: 12px 14px;
  color: #7a4b00;
  background: #fff8e5;
  border: 1px solid #ffe2a3;
  border-radius: 8px;
}

.content {
  margin: 0;
  color: #28352f;
  line-height: 1.9;
  white-space: pre-wrap;
}

.action-panel,
.comments {
  margin-top: 18px;
}

.action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.report-form {
  display: grid;
  grid-template-columns: minmax(180px, 1fr) auto auto;
  gap: 10px;
  align-items: center;
  margin-top: 14px;
}

.report-form input {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 9px 12px;
}

.inline-success {
  color: var(--green);
  font-size: 13px;
}

.comment-heading {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.comment-heading h2 {
  margin: 0;
  font-size: 20px;
}

.comments {
  display: grid;
  gap: 16px;
}

@media (max-width: 640px) {
  .report-form {
    grid-template-columns: 1fr;
  }
}
</style>
