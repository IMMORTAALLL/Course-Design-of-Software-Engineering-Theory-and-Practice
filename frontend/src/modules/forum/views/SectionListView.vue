<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchSections } from "../api/forumApi";
import SectionCard from "../components/SectionCard.vue";
import type { Section } from "../types/forum";

const sections = ref<Section[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    sections.value = await fetchSections();
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>论坛板块</h1>
        <p>按市场、产品和策略主题进入不同讨论区。</p>
      </div>
    </div>

    <div v-if="loading" class="empty">正在加载板块...</div>
    <div v-else class="section-grid">
      <SectionCard v-for="section in sections" :key="section.id" :section="section" />
    </div>
  </section>
</template>

<style scoped>
.section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
</style>
