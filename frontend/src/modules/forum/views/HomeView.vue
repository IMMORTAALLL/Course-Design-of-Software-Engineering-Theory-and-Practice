<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import { fetchHotPosts, fetchPosts, fetchSections } from "../api/forumApi";
import PostCard from "../components/PostCard.vue";
import SectionCard from "../components/SectionCard.vue";
import type { PostListItem, Section } from "../types/forum";

const sections = ref<Section[]>([]);
const latestPosts = ref<PostListItem[]>([]);
const hotPosts = ref<PostListItem[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const [sectionData, latestData, hotData] = await Promise.all([
      fetchSections(),
      fetchPosts({ page: 1, size: 5 }),
      fetchHotPosts(5)
    ]);
    sections.value = sectionData;
    latestPosts.value = latestData.items;
    hotPosts.value = hotData;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>智投社区</h1>
        <p>围绕股票、基金、宏观策略和量化交易的投资讨论社区。</p>
      </div>
      <RouterLink class="primary-button" to="/posts/create">发布讨论</RouterLink>
    </div>

    <div v-if="loading" class="empty">正在加载论坛内容...</div>

    <div v-else class="grid-2">
      <div class="stack">
        <section class="panel">
          <div class="section-heading">
            <h2>核心板块</h2>
            <RouterLink to="/sections">查看全部</RouterLink>
          </div>
          <div v-if="sections.length" class="section-grid">
            <SectionCard v-for="section in sections.slice(0, 4)" :key="section.id" :section="section" />
          </div>
          <div v-else class="empty compact-empty">暂无板块。</div>
        </section>

        <section class="stack">
          <div class="section-heading">
            <h2>最新帖子</h2>
          </div>
          <PostCard v-for="post in latestPosts" :key="post.id" :post="post" />
          <div v-if="!latestPosts.length" class="empty compact-empty">暂无帖子。</div>
        </section>
      </div>

      <aside class="panel">
        <div class="section-heading">
          <h2>热门讨论</h2>
          <RouterLink to="/hot">热榜</RouterLink>
        </div>
        <div class="stack">
          <PostCard v-for="(post, index) in hotPosts" :key="post.id" :post="post" :rank="index + 1" />
          <div v-if="!hotPosts.length" class="empty compact-empty">暂无热门讨论。</div>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.section-heading h2 {
  margin: 0;
  font-size: 20px;
}

.section-heading a {
  color: #157f5b;
  font-weight: 700;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.compact-empty {
  padding: 28px;
}

@media (max-width: 640px) {
  .section-grid {
    grid-template-columns: 1fr;
  }
}
</style>
