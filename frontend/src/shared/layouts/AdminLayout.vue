<template>
  <div class="admin-shell">
    <aside class="admin-sidebar">
      <div class="sidebar-brand">
        <span class="sidebar-kicker">智投社区</span>
        <strong>后台管理台</strong>
      </div>

      <nav class="sidebar-nav">
        <RouterLink to="/admin" class="nav-item">后台首页</RouterLink>
        <RouterLink to="/admin/audits" class="nav-item">内容审核</RouterLink>
        <RouterLink to="/admin/reports" class="nav-item">举报处理</RouterLink>
        <RouterLink to="/admin/sensitive-words" class="nav-item">敏感词管理</RouterLink>
        <RouterLink to="/admin/users" class="nav-item">用户处罚</RouterLink>
        <RouterLink to="/admin/statistics" class="nav-item">运营统计</RouterLink>
      </nav>
    </aside>

    <div class="admin-content">
      <header class="admin-topbar">
        <div>
          <p class="topbar-kicker">成员 D / 审核与后台模块</p>
          <h1>{{ title }}</h1>
        </div>
        <div class="topbar-meta">
          <span>FastAPI + SQLAlchemy</span>
          <span>Vue 3 + Vite + TypeScript</span>
        </div>
      </header>

      <section class="admin-body">
        <slot />
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
}>();
</script>
