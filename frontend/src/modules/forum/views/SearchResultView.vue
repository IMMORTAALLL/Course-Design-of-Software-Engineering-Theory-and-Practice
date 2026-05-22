<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { searchPosts } from "../api/forumApi";
import PostCard from "../components/PostCard.vue";
import type { PostListItem } from "../types/forum";

const route = useRoute();
const keyword = computed(() => String(route.query.keyword || "").trim());
const posts = ref<PostListItem[]>([]);
const total = ref(0);
const loading = ref(false);

async function loadResults() {
  if (!keyword.value) {
    posts.value = [];
    total.value = 0;
    return;
  }
  loading.value = true;
  try {
    const data = await searchPosts(keyword.value);
    posts.value = data.items;
    total.value = data.total;
  } finally {
    loading.value = false;
  }
}

onMounted(loadResults);
watch(keyword, loadResults);
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>搜索结果</h1>
        <p>关键词：{{ keyword || "未输入" }}，共 {{ total }} 条结果。</p>
      </div>
    </div>

    <div v-if="loading" class="empty">正在搜索...</div>
    <div v-else-if="!posts.length" class="empty">暂无相关内容，可以尝试更换关键词。</div>
    <div v-else class="stack">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </section>
</template>
