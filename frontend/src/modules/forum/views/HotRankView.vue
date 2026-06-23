<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchHotPosts, fetchHotTopics } from "../api/forumApi";
import PostCard from "../components/PostCard.vue";
import type { HotTopic, PostListItem } from "../types/forum";

const posts = ref<PostListItem[]>([]);
const topics = ref<HotTopic[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const [postData, topicData] = await Promise.all([fetchHotPosts(20), fetchHotTopics("weekly", 12)]);
    posts.value = postData;
    topics.value = topicData;
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
    <section v-if="!loading && topics.length" class="panel topic-grid">
      <RouterLink
        v-for="topic in topics"
        :key="topic.id"
        class="topic-chip"
        :to="`/search?keyword=${encodeURIComponent(topic.name)}`"
      >
        <span>{{ topic.name }}</span>
        <small>{{ topic.postCount }} posts · {{ topic.hotScore }}</small>
      </RouterLink>
    </section>
  </section>
</template>

<style scoped>
.topic-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 10px;
  margin-top: 18px;
}

.topic-chip {
  display: grid;
  gap: 4px;
  padding: 12px;
  color: var(--ink);
  border: 1px solid var(--line);
  border-radius: 8px;
}

.topic-chip span {
  font-weight: 800;
}

.topic-chip small {
  color: var(--muted);
}
</style>
