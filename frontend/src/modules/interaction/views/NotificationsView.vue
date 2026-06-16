<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";

import { fetchNotifications, markNotificationRead } from "../api/interactionApi";
import type { NotificationItem } from "../types/interaction";

const notifications = ref<NotificationItem[]>([]);
const loading = ref(true);
const errorMessage = ref("");

async function loadData() {
  loading.value = true;
  errorMessage.value = "";
  try {
    notifications.value = await fetchNotifications();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "通知加载失败";
  } finally {
    loading.value = false;
  }
}

async function readItem(item: NotificationItem) {
  if (item.isRead) return;
  const updated = await markNotificationRead(item.id);
  item.isRead = updated.isRead;
}

function targetPath(item: NotificationItem) {
  if (item.targetType === "post" && item.targetId) return `/posts/${item.targetId}`;
  if (item.targetType === "user" && item.targetId) return `/users/${item.targetId}`;
  if (item.targetType === "group" && item.targetId) return `/groups/${item.targetId}`;
  return "/me/notifications";
}

onMounted(loadData);
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>通知中心</h1>
        <p>查看评论、关注、群组和系统审核相关通知。</p>
      </div>
    </div>

    <div v-if="loading" class="empty">正在加载通知...</div>
    <div v-else-if="errorMessage" class="empty">{{ errorMessage }}</div>
    <div v-else-if="!notifications.length" class="empty">暂无通知。</div>

    <div v-else class="stack">
      <article v-for="item in notifications" :key="item.id" class="panel notification" :class="{ unread: !item.isRead }">
        <div>
          <h2>{{ item.title }}</h2>
          <p>{{ item.content }}</p>
          <div class="meta">
            <span>{{ item.notificationType }}</span>
            <span>{{ new Date(item.createdAt).toLocaleString() }}</span>
            <span>{{ item.isRead ? "已读" : "未读" }}</span>
          </div>
        </div>
        <RouterLink class="action-button" :to="targetPath(item)" @click="readItem(item)">查看</RouterLink>
      </article>
    </div>
  </section>
</template>

<style scoped>
.notification {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.notification.unread {
  border-left: 4px solid var(--green);
}

h2 {
  margin: 0 0 8px;
  font-size: 18px;
}

p {
  margin: 0 0 10px;
  color: var(--muted);
}
</style>
