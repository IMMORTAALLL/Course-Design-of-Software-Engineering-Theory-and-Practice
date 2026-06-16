<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

import { createReply, reportComment, toggleCommentLike } from "../api/interactionApi";
import type { CommentItem } from "../types/interaction";
import CommentEditor from "./CommentEditor.vue";

const props = defineProps<{
  comments: CommentItem[];
}>();

const emit = defineEmits<{
  refresh: [];
}>();

const replyTarget = ref<number | null>(null);
const reportTarget = ref<number | null>(null);
const reportReason = ref("");
const reportMessage = ref("");
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

async function submitReport(commentId: number) {
  const reason = reportReason.value.trim();
  if (!reason) {
    errorMessage.value = "请填写举报原因。";
    return;
  }
  errorMessage.value = "";
  reportMessage.value = "";
  try {
    await reportComment(commentId, reason);
    reportTarget.value = null;
    reportReason.value = "";
    reportMessage.value = "举报已提交";
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "举报失败";
  }
}

function toggleReport(commentId: number) {
  reportTarget.value = reportTarget.value === commentId ? null : commentId;
  reportReason.value = "";
  reportMessage.value = "";
}
</script>

<template>
  <div class="comment-list">
    <p v-if="errorMessage" class="inline-error">{{ errorMessage }}</p>
    <p v-if="reportMessage" class="inline-success">{{ reportMessage }}</p>
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
        <button class="action-button" type="button" @click="toggleReport(comment.id)">举报</button>
      </div>

      <CommentEditor
        v-if="replyTarget === comment.id"
        placeholder="回复这条评论"
        submit-text="发布回复"
        @submit="submitReply(comment.id, $event)"
      />

      <form v-if="reportTarget === comment.id" class="report-form" @submit.prevent="submitReport(comment.id)">
        <input v-model="reportReason" maxlength="255" placeholder="举报原因" />
        <button class="action-button" type="submit">提交</button>
      </form>

      <div v-if="comment.replies.length" class="reply-list">
        <article v-for="reply in comment.replies" :key="reply.id" class="reply-item">
          <div class="comment-meta">
            <RouterLink :to="`/users/${reply.userId}`">{{ reply.authorNickname }}</RouterLink>
            <span>{{ new Date(reply.createdAt).toLocaleString() }}</span>
          </div>
          <p>{{ reply.content }}</p>
          <div class="comment-actions">
            <button class="action-button" type="button" @click="toggleReport(reply.id)">举报</button>
          </div>
          <form v-if="reportTarget === reply.id" class="report-form" @submit.prevent="submitReport(reply.id)">
            <input v-model="reportReason" maxlength="255" placeholder="举报原因" />
            <button class="action-button" type="submit">提交</button>
          </form>
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

.report-form {
  display: grid;
  grid-template-columns: minmax(160px, 1fr) auto;
  gap: 8px;
}

.report-form input {
  min-width: 0;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 8px 10px;
}

.inline-success {
  color: var(--green);
  font-size: 13px;
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

@media (max-width: 560px) {
  .report-form {
    grid-template-columns: 1fr;
  }
}
</style>
