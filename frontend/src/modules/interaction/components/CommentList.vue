<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

import { createReply, toggleCommentLike } from "../api/interactionApi";
import type { CommentItem } from "../types/interaction";
import CommentEditor from "./CommentEditor.vue";

const props = defineProps<{
  comments: CommentItem[];
}>();

const emit = defineEmits<{
  refresh: [];
}>();

const replyTarget = ref<number | null>(null);
const errorMessage = ref("");

async function likeComment(comment: CommentItem) {
  errorMessage.value = "";
  try {
    const result = await toggleCommentLike(comment.id);
    comment.likeCount = result.count;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "操作失败";
  }
}

async function submitReply(commentId: number, content: string) {
  errorMessage.value = "";
  try {
    await createReply(commentId, content);
    replyTarget.value = null;
    emit("refresh");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "回复失败";
  }
}
</script>

<template>
  <div class="comment-list">
    <p v-if="errorMessage" class="inline-error">{{ errorMessage }}</p>
    <div v-if="!props.comments.length" class="empty">还没有评论，来发表第一条讨论。</div>

    <article v-for="comment in props.comments" :key="comment.id" class="comment-item">
      <div class="comment-meta">
        <RouterLink :to="`/users/${comment.userId}`">{{ comment.authorNickname }}</RouterLink>
        <span>{{ comment.authorAuthLevel === 2 ? "专业认证" : comment.authorAuthLevel === 1 ? "实名认证" : "基础用户" }}</span>
        <span>{{ new Date(comment.createdAt).toLocaleString() }}</span>
      </div>
      <p>{{ comment.content }}</p>
      <div class="comment-actions">
        <button class="action-button" type="button" @click="likeComment(comment)">点赞 {{ comment.likeCount }}</button>
        <button class="action-button" type="button" @click="replyTarget = replyTarget === comment.id ? null : comment.id">
          回复
        </button>
      </div>

      <CommentEditor
        v-if="replyTarget === comment.id"
        placeholder="回复这条评论"
        submit-text="发布回复"
        @submit="submitReply(comment.id, $event)"
      />

      <div v-if="comment.replies.length" class="reply-list">
        <article v-for="reply in comment.replies" :key="reply.id" class="reply-item">
          <div class="comment-meta">
            <RouterLink :to="`/users/${reply.userId}`">{{ reply.authorNickname }}</RouterLink>
            <span>{{ new Date(reply.createdAt).toLocaleString() }}</span>
          </div>
          <p>{{ reply.content }}</p>
        </article>
      </div>
    </article>
  </div>
</template>

<style scoped>
.comment-list {
  display: grid;
  gap: 14px;
}

.comment-item,
.reply-item {
  display: grid;
  gap: 10px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fbfdfc;
}

.comment-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  color: var(--muted);
  font-size: 13px;
}

.comment-meta a {
  color: var(--green);
  font-weight: 700;
}

p {
  margin: 0;
  line-height: 1.75;
}

.comment-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.reply-list {
  display: grid;
  gap: 10px;
  padding-left: 22px;
  border-left: 3px solid #dbe8e3;
}

.reply-item {
  background: white;
}
</style>
