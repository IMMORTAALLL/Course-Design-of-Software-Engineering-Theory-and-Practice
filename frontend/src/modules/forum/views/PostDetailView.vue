<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink, useRoute } from "vue-router";

import { fetchPost } from "../api/forumApi";
import TagBadge from "../components/TagBadge.vue";
import type { PostDetail } from "../types/forum";

const route = useRoute();
const postId = computed(() => Number(route.params.id));
const post = ref<PostDetail | null>(null);
const loading = ref(true);

async function loadPost() {
  loading.value = true;
  try {
    post.value = await fetchPost(postId.value);
  } finally {
    loading.value = false;
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
</style>
