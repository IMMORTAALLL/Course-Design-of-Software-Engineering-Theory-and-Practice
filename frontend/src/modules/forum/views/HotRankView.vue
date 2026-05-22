<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchHotPosts } from "../api/forumApi";
import PostCard from "../components/PostCard.vue";
import type { PostListItem } from "../types/forum";

const posts = ref<PostListItem[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    posts.value = await fetchHotPosts(20);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>热门帖子</h1>
        <p>按浏览、点赞和评论综合热度排序。</p>
      </div>
    </div>

    <div v-if="loading" class="empty">正在加载热榜...</div>
    <div v-else-if="!posts.length" class="empty">暂无热门帖子。</div>
    <div v-else class="stack">
      <PostCard v-for="(post, index) in posts" :key="post.id" :post="post" :rank="index + 1" />
    </div>
  </section>
</template>
