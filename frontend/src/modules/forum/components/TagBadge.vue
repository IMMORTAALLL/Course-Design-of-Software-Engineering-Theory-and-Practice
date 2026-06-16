<script setup lang="ts">
import type { Tag } from "../types/forum";

defineProps<{
  tag: Tag;
}>();
</script>

<template>
  <span class="tag-badge" :class="tag.tag_type.toLowerCase()">
    {{ tag.name }}
  </span>
</template>

<style scoped>
.tag-badge {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 3px 9px;
  border: 1px solid #d9e4df;
  border-radius: 999px;
  color: #315346;
  background: var(--green-soft);
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}

.stock {
  color: #b42318;
  background: var(--red-soft);
  border-color: #ffd6d0;
}

.fund {
  color: var(--blue);
  background: var(--blue-soft);
  border-color: #bfdbfe;
}

.topic {
  color: var(--gold);
  background: var(--gold-soft);
  border-color: #ffe2a3;
}
</style>
