<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { Section } from "../types/forum";

defineProps<{
  section: Section;
}>();
</script>

<template>
  <RouterLink class="section-card" :to="`/sections/${section.id}`">
    <strong>{{ section.name }}</strong>
    <p>{{ section.description || "暂无板块简介" }}</p>
    <span>排序权重 {{ section.sort_order }}</span>
  </RouterLink>
</template>

<style scoped>
.section-card {
  display: grid;
  gap: 10px;
  padding: 18px;
  min-height: 138px;
  background: linear-gradient(180deg, #ffffff, #fbfdfc);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow-soft);
  transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
}

.section-card:hover {
  transform: translateY(-2px);
  border-color: rgba(15, 123, 95, 0.38);
  box-shadow: var(--shadow);
}

strong {
  font-size: 18px;
  color: var(--ink);
}

p {
  margin: 0;
  color: var(--ink-soft);
  line-height: 1.55;
}

span {
  margin-top: auto;
  color: #667085;
  font-size: 13px;
}
</style>
