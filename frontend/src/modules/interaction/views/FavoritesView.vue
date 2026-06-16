<script setup lang="ts">
import { onMounted, ref } from "vue";

import PostCard from "@/modules/forum/components/PostCard.vue";
import type { PostListItem } from "@/modules/forum/types/forum";
import { fetchFavorites } from "../api/interactionApi";

const posts = ref<PostListItem[]>([]);
const total = ref(0);
const loading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    const result = await fetchFavorites(1, 20);
    posts.value = result.items;
    total.value = result.total;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "收藏加载失败";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>我的收藏</h1>
        <p>集中查看已收藏的股票基金讨论内容，共 {{ total }} 条。</p>
      </div>
    </div>

    <div v-if="loading" class="empty">正在加载收藏...</div>
    <div v-else-if="errorMessage" class="empty">{{ errorMessage }}</div>
    <div v-else-if="!posts.length" class="empty">还没有收藏帖子。</div>
    <div v-else class="stack">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </section>
</template>
