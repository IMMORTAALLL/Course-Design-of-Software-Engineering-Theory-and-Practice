<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { GroupItem } from "../types/interaction";

defineProps<{
  group: GroupItem;
}>();
</script>

<template>
  <article class="group-card">
    <div>
      <RouterLink class="group-title" :to="`/groups/${group.id}`">{{ group.name }}</RouterLink>
      <p>{{ group.description || "暂无群组简介。" }}</p>
    </div>
    <div class="meta">
      <span>{{ group.permission === 1 ? "公开" : group.permission === 2 ? "需审核" : "私密" }}</span>
      <span>{{ group.memberCount }} 位成员</span>
      <span>群主 {{ group.creatorNickname }}</span>
      <span v-if="group.joined">已加入</span>
      <span v-else-if="group.pending">申请中</span>
    </div>
  </article>
</template>

<style scoped>
.group-card {
  display: grid;
  gap: 12px;
  padding: 18px;
  background: white;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.group-title {
  color: var(--ink);
  font-size: 18px;
  font-weight: 800;
}

p {
  margin: 8px 0 0;
  color: var(--muted);
  line-height: 1.7;
}
</style>
