<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import PostCard from "@/modules/forum/components/PostCard.vue";
import type { PostListItem } from "@/modules/forum/types/forum";
import { fetchFollowingFeed } from "../api/interactionApi";

const posts = ref<PostListItem[]>([]);
const total = ref(0);
const loading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
  try {
    const result = await fetchFollowingFeed(1, 20);
    posts.value = result.items;
    total.value = result.total;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "关注动态加载失败";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>关注动态</h1>
        <p>查看已关注用户发布的新讨论和长文分析，共 {{ total }} 条。</p>
      </div>
      <RouterLink class="secondary-link" to="/search">发现更多内容</RouterLink>
    </div>

    <div v-if="loading" class="empty">正在加载关注动态...</div>
    <div v-else-if="errorMessage" class="empty">{{ errorMessage }}</div>
    <div v-else-if="!posts.length" class="empty">暂时没有关注动态，可以先去用户主页关注感兴趣的作者。</div>
    <div v-else class="stack">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </section>
</template>

<style scoped>
.secondary-link {
  color: var(--green);
  font-weight: 700;
}
</style>
