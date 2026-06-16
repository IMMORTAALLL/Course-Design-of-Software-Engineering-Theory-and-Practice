<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink, RouterView, useRoute, useRouter } from "vue-router";

import { authState, isAuthenticated, loadCurrentUser, logout } from "@/modules/auth/stores/authStore";

const route = useRoute();
const router = useRouter();
const keyword = ref("");
const isAdminRoute = computed(() => route.path.startsWith("/admin"));

onMounted(() => {
  loadCurrentUser();
});

function submitSearch() {
  const value = keyword.value.trim();
  if (!value) return;
  router.push({ path: "/search", query: { keyword: value } });
}

async function submitLogout() {
  await logout();
  router.push("/");
}
</script>

<template>
  <div :class="isAdminRoute ? 'admin-app' : 'app-shell'">
    <header v-if="!isAdminRoute" class="site-header">
      <RouterLink class="brand" to="/">
        <span class="brand-mark">智</span>
        <span>
          <strong>智投社区</strong>
          <small>股票基金投资论坛</small>
        </span>
      </RouterLink>

      <form class="search-bar" @submit.prevent="submitSearch">
        <input v-model="keyword" placeholder="搜索股票、基金、帖子关键词" />
        <button type="submit">搜索</button>
      </form>

      <nav class="site-nav">
        <RouterLink to="/sections">板块</RouterLink>
        <RouterLink to="/hot">热榜</RouterLink>
        <RouterLink to="/posts/create">发帖</RouterLink>
        <RouterLink to="/admin">后台</RouterLink>
        <template v-if="isAuthenticated">
          <RouterLink to="/me">{{ authState.user?.nickname || "个人中心" }}</RouterLink>
          <button class="nav-button" type="button" @click="submitLogout">退出</button>
        </template>
        <template v-else>
          <RouterLink to="/login">登录</RouterLink>
          <RouterLink to="/register">注册</RouterLink>
        </template>
      </nav>
    </header>

    <main v-if="!isAdminRoute">
      <RouterView />
    </main>
    <RouterView v-else />
  </div>
</template>

<style scoped>
.nav-button {
  border: 0;
  color: var(--muted);
  background: transparent;
  padding: 0;
  font: inherit;
}

.nav-button:hover {
  color: var(--green);
}
</style>
