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
  background: white;
  border: 1px solid #d8e0dc;
  border-radius: 8px;
  transition: transform 0.16s ease, border-color 0.16s ease;
}

.section-card:hover {
  transform: translateY(-2px);
  border-color: #157f5b;
}

strong {
  font-size: 18px;
}

p {
  margin: 0;
  color: #52605a;
  line-height: 1.55;
}

span {
  margin-top: auto;
  color: #667085;
  font-size: 13px;
}
</style>
