<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { fetchSearchSuggestions, searchPosts } from "../api/forumApi";
import PostCard from "../components/PostCard.vue";
import type { PostListItem, SearchSuggestion } from "../types/forum";

const route = useRoute();
const keyword = computed(() => String(route.query.keyword || "").trim());
const posts = ref<PostListItem[]>([]);
const suggestions = ref<SearchSuggestion[]>([]);
const total = ref(0);
const loading = ref(false);

async function loadResults() {
  if (!keyword.value) {
    posts.value = [];
    suggestions.value = [];
    total.value = 0;
    return;
  }
  loading.value = true;
  try {
    const [data, suggestionData] = await Promise.all([
      searchPosts(keyword.value),
      fetchSearchSuggestions(keyword.value)
    ]);
    posts.value = data.items;
    suggestions.value = suggestionData;
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
    <div v-if="!loading && suggestions.length" class="suggestion-row">
      <RouterLink
        v-for="item in suggestions"
        :key="`${item.type}-${item.value}`"
        class="suggestion-chip"
        :to="item.type === 'user' ? `/users/${item.value}` : item.type === 'post' ? `/posts/${item.value}` : `/search?keyword=${encodeURIComponent(item.label)}`"
      >
        {{ item.label }} · {{ item.type }}
      </RouterLink>
    </div>
    <div v-if="!loading && !suggestions.length && !posts.length" class="empty">暂无相关内容，可以尝试更换关键词。</div>
    <div v-if="!loading && posts.length" class="stack">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </section>
</template>

<style scoped>
.suggestion-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}

.suggestion-chip {
  padding: 7px 10px;
  color: var(--green);
  border: 1px solid var(--line);
  border-radius: 8px;
  font-weight: 700;
}
</style>
