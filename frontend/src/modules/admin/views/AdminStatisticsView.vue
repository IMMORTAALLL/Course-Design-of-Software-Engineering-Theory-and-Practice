<template>
  <AdminLayout title="运营统计">
    <section class="panel">
      <div class="panel-header">
        <h2>热门话题</h2>
        <span class="panel-note">近期开启讨论最多的主题</span>
      </div>
      <div class="topic-list">
        <span v-for="topic in statistics?.hot_topics ?? []" :key="topic" class="topic-chip">{{ topic }}</span>
      </div>
    </section>

    <section class="panel">
      <div class="panel-header">
        <h2>活跃板块</h2>
        <span class="panel-note">按当前演示数据统计</span>
      </div>
      <div class="section-bars">
        <div v-for="section in statistics?.active_sections ?? []" :key="section.name" class="section-row">
          <span>{{ section.name }}</span>
          <div class="bar-track">
            <div class="bar-fill" :style="{ width: `${section.value / 1.4}%` }"></div>
          </div>
          <strong>{{ section.value }}</strong>
        </div>
      </div>
    </section>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchAdminStatistics } from "../api/admin";
import type { AdminStatistics } from "../types/admin";
import AdminLayout from "../../../shared/layouts/AdminLayout.vue";

const statistics = ref<AdminStatistics | null>(null);

async function loadData() {
  statistics.value = await fetchAdminStatistics();
}

onMounted(loadData);
</script>
