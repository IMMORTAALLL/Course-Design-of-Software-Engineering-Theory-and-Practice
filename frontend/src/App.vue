<script setup lang="ts">
import { ref } from "vue";
import { RouterLink, RouterView, useRouter } from "vue-router";

const router = useRouter();
const keyword = ref("");

function submitSearch() {
  const value = keyword.value.trim();
  if (!value) return;
  router.push({ path: "/search", query: { keyword: value } });
}
</script>

<template>
  <div class="app-shell">
    <header class="site-header">
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
      </nav>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>
