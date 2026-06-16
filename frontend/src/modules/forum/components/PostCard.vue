<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { PostListItem } from "../types/forum";
import TagBadge from "./TagBadge.vue";

defineProps<{
  post: PostListItem;
  rank?: number;
}>();
</script>

<template>
  <article class="post-card">
    <div v-if="rank" class="rank">{{ rank }}</div>
    <div class="post-body">
      <RouterLink class="title" :to="`/posts/${post.id}`">{{ post.title }}</RouterLink>
      <p>{{ post.summary }}</p>
      <div class="tag-row" v-if="post.tags.length">
        <TagBadge v-for="tag in post.tags" :key="tag.id" :tag="tag" />
      </div>
      <div class="meta">
        <RouterLink :to="`/sections/${post.section_id}`">{{ post.section_name }}</RouterLink>
        <RouterLink :to="`/users/${post.user_id}`">{{ post.author_nickname || "社区用户" }}</RouterLink>
        <span v-if="post.post_type === 2">长文分析</span>
        <span v-if="post.is_elite">精华</span>
        <span>{{ new Date(post.created_at).toLocaleString() }}</span>
        <span>浏览 {{ post.view_count }}</span>
        <span>点赞 {{ post.like_count }}</span>
        <span>评论 {{ post.comment_count }}</span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.post-card {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  padding: 18px;
  background: linear-gradient(180deg, #ffffff, #fbfdfc);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow-soft);
  transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
}

.post-card:hover {
  transform: translateY(-2px);
  border-color: rgba(15, 123, 95, 0.34);
  box-shadow: var(--shadow);
}

.rank {
  display: grid;
  width: 32px;
  height: 32px;
  place-items: center;
  color: white;
  background: linear-gradient(135deg, var(--green), var(--green-strong));
  border-radius: 6px;
  box-shadow: 0 8px 18px rgba(15, 123, 95, 0.2);
  font-weight: 800;
}

.post-body {
  display: grid;
  gap: 9px;
}

.title {
  color: var(--ink);
  font-size: 18px;
  line-height: 1.35;
  font-weight: 800;
}

.title:hover {
  color: var(--green);
}

p {
  margin: 0;
  color: var(--ink-soft);
  line-height: 1.65;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
