<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { fetchGroup, joinGroup, leaveGroup } from "../api/interactionApi";
import type { GroupItem } from "../types/interaction";

const route = useRoute();
const groupId = computed(() => Number(route.params.id));
const group = ref<GroupItem | null>(null);
const loading = ref(true);
const acting = ref(false);
const errorMessage = ref("");

const membershipButtonText = computed(() => {
  if (!group.value) return "";
  if (group.value.pending) return "申请中";
  if (group.value.joined) return "退出群组";
  return group.value.permission === 2 ? "申请加入" : "加入群组";
});

async function loadData() {
  loading.value = true;
  errorMessage.value = "";
  try {
    group.value = await fetchGroup(groupId.value);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "群组加载失败";
  } finally {
    loading.value = false;
  }
}

async function toggleMembership() {
  if (!group.value || group.value.pending) return;
  acting.value = true;
  errorMessage.value = "";
  try {
    group.value = group.value.joined ? await leaveGroup(group.value.id) : await joinGroup(group.value.id);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "操作失败";
  } finally {
    acting.value = false;
  }
}

onMounted(loadData);
watch(groupId, loadData);
</script>

<template>
  <section class="page">
    <div v-if="loading" class="empty">正在加载群组...</div>
    <div v-else-if="errorMessage && !group" class="empty">{{ errorMessage }}</div>

    <template v-else-if="group">
      <div class="panel group-hero">
        <div>
          <p class="muted">{{ group.permission === 1 ? "公开群组" : group.permission === 2 ? "需审核群组" : "私密群组" }}</p>
          <h1>{{ group.name }}</h1>
          <p>{{ group.description || "暂无群组简介。" }}</p>
          <div class="meta">
            <span>群主 {{ group.creatorNickname }}</span>
            <span>{{ group.memberCount }} 位成员</span>
            <span>{{ new Date(group.createdAt).toLocaleString() }}</span>
          </div>
        </div>
        <button class="primary-button" type="button" :disabled="acting || group.pending" @click="toggleMembership">
          {{ membershipButtonText }}
        </button>
      </div>

      <p v-if="errorMessage" class="inline-error">{{ errorMessage }}</p>

      <section class="panel stack">
        <h2>群内讨论</h2>
        <p class="muted">群内暂时还没有公开讨论内容。</p>
      </section>
    </template>
  </section>
</template>

<style scoped>
.group-hero {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
}

h1,
h2 {
  margin: 0;
}

.group-hero p {
  line-height: 1.8;
}

@media (max-width: 640px) {
  .group-hero {
    flex-direction: column;
  }
}
</style>
