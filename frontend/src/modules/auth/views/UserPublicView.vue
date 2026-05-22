<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import { fetchPublicUser } from "../api/authApi";
import type { PublicUser } from "../types/auth";

const route = useRoute();
const user = ref<PublicUser | null>(null);
const loading = ref(true);
const errorMessage = ref("");

async function loadUser() {
  const id = Number(route.params.id);
  if (!Number.isFinite(id)) {
    errorMessage.value = "用户 ID 不合法。";
    loading.value = false;
    return;
  }

  loading.value = true;
  errorMessage.value = "";
  try {
    user.value = await fetchPublicUser(id);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "用户信息加载失败";
  } finally {
    loading.value = false;
  }
}

onMounted(loadUser);
watch(() => route.params.id, loadUser);
</script>

<template>
  <section class="page">
    <div v-if="loading" class="empty">正在加载用户主页...</div>
    <div v-else-if="errorMessage" class="empty">{{ errorMessage }}</div>

    <div v-else-if="user" class="panel public-card">
      <div class="avatar">
        <img v-if="user.avatarUrl" :src="user.avatarUrl" alt="用户头像" />
        <span v-else>{{ user.nickname?.slice(0, 1) || "用" }}</span>
      </div>

      <div>
        <h1>{{ user.nickname || "未命名用户" }}</h1>
        <div class="meta">
          <span>{{ user.authLevel === 2 ? "专业认证" : user.authLevel === 1 ? "实名认证" : "基础用户" }}</span>
          <span>影响力值 {{ user.influenceScore }}</span>
        </div>
        <p class="bio">{{ user.bio || "这个用户还没有填写简介。" }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.public-card {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

.avatar {
  display: grid;
  width: 86px;
  height: 86px;
  place-items: center;
  overflow: hidden;
  color: white;
  background: var(--green);
  border-radius: 8px;
  font-size: 30px;
  font-weight: 800;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h1 {
  margin: 0 0 10px;
}

.bio {
  margin-top: 18px;
  color: var(--ink);
  line-height: 1.8;
}

@media (max-width: 560px) {
  .public-card {
    grid-template-columns: 1fr;
  }
}
</style>
