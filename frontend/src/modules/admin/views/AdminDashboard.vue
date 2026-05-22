<template>
  <AdminLayout title="后台首页">
    <section class="hero">
      <div>
        <p class="eyebrow">成员 D / 后台审核模块</p>
        <h2 class="hero-title">先把审核、举报、敏感词和统计这条管理链路跑通</h2>
        <p class="hero-copy">这版首页聚焦管理员日常最常打开的概览信息，你后面继续扩展页面时可以直接沿着左侧菜单拆模块，不用再把所有内容塞进一个文件。</p>
      </div>
      <button class="refresh-button" @click="loadAll">刷新数据</button>
    </section>

    <section class="metric-grid">
      <article class="metric-card">
        <span class="metric-label">今日发帖</span>
        <strong class="metric-value">{{ overview?.today_posts ?? "--" }}</strong>
      </article>
      <article class="metric-card">
        <span class="metric-label">待审核内容</span>
        <strong class="metric-value">{{ overview?.pending_audits ?? "--" }}</strong>
      </article>
      <article class="metric-card">
        <span class="metric-label">待处理举报</span>
        <strong class="metric-value">{{ overview?.pending_reports ?? "--" }}</strong>
      </article>
      <article class="metric-card">
        <span class="metric-label">启用敏感词</span>
        <strong class="metric-value">{{ overview?.active_sensitive_words ?? "--" }}</strong>
      </article>
    </section>

    <section class="quick-grid">
      <RouterLink to="/admin/audits" class="quick-card">
        <strong>内容审核</strong>
        <span>查看待审核帖子、评论和附件</span>
      </RouterLink>
      <RouterLink to="/admin/reports" class="quick-card">
        <strong>举报处理</strong>
        <span>集中处理违规举报和风险内容</span>
      </RouterLink>
      <RouterLink to="/admin/sensitive-words" class="quick-card">
        <strong>敏感词规则</strong>
        <span>维护命中词、风险等级和处理动作</span>
      </RouterLink>
      <RouterLink to="/admin/statistics" class="quick-card">
        <strong>运营统计</strong>
        <span>查看热门话题和活跃板块情况</span>
      </RouterLink>
    </section>

    <section class="panel-grid">
      <article class="panel">
        <div class="panel-header">
          <h2>当前待办</h2>
          <span class="panel-note">管理员优先处理项</span>
        </div>
        <ul class="todo-list">
          <li>待审核内容：{{ overview?.pending_audits ?? 0 }} 条</li>
          <li>待处理举报：{{ overview?.pending_reports ?? 0 }} 条</li>
          <li>启用敏感词：{{ overview?.active_sensitive_words ?? 0 }} 条</li>
        </ul>
      </article>

      <article class="panel">
        <div class="panel-header">
          <h2>最近热点</h2>
          <span class="panel-note">用于首页和答辩展示</span>
        </div>
        <div class="topic-list">
          <span v-for="topic in statistics?.hot_topics ?? []" :key="topic" class="topic-chip">{{ topic }}</span>
        </div>
      </article>
    </section>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import {
  fetchAdminStatistics,
  fetchOverview,
  fetchUserModerationRecords
} from "../api/admin";
import type {
  AdminStatistics,
  AdminOverview,
  UserModerationRecord
} from "../types/admin";
import AdminLayout from "../../../shared/layouts/AdminLayout.vue";

const overview = ref<AdminOverview | null>(null);
const moderationRecords = ref<UserModerationRecord[]>([]);
const statistics = ref<AdminStatistics | null>(null);
const errorMessage = ref("");

async function loadAll() {
  errorMessage.value = "";
  try {
    const [overviewResult, moderationResult, statisticsResult] = await Promise.all([
      fetchOverview(),
      fetchUserModerationRecords(),
      fetchAdminStatistics()
    ]);

    overview.value = overviewResult;
    moderationRecords.value = moderationResult;
    statistics.value = statisticsResult;
  } catch (error) {
    errorMessage.value = "后台数据加载失败，请确认 FastAPI 服务和数据库已启动。";
    console.error(error);
  }
}

onMounted(loadAll);
</script>
