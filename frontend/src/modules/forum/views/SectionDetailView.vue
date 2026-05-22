<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink, useRoute } from "vue-router";

import { fetchPosts, fetchSection } from "../api/forumApi";
import PostCard from "../components/PostCard.vue";
import type { PostListItem, Section } from "../types/forum";

const route = useRoute();
const sectionId = computed(() => Number(route.params.id));
const section = ref<Section | null>(null);
const posts = ref<PostListItem[]>([]);
const loading = ref(true);

async function loadData() {
  loading.value = true;
  try {
    const [sectionData, postsData] = await Promise.all([
      fetchSection(sectionId.value),
      fetchPosts({ section_id: sectionId.value, page: 1, size: 20 })
    ]);
    section.value = sectionData;
    posts.value = postsData.items;
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
watch(sectionId, loadData);
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>{{ section?.name || "板块详情" }}</h1>
        <p>{{ section?.description || "查看该板块下的公开帖子。" }}</p>
      </div>
      <RouterLink class="primary-button" to="/posts/create">发布帖子</RouterLink>
    </div>

    <div v-if="loading" class="empty">正在加载帖子...</div>
    <div v-else-if="!posts.length" class="empty">这个板块还没有帖子。</div>
    <div v-else class="stack">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
  </section>
</template>
