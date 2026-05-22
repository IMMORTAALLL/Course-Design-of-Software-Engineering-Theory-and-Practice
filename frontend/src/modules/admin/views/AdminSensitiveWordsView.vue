<template>
  <AdminLayout title="敏感词管理">
    <section class="panel">
      <div class="panel-header">
        <h2>风险规则列表</h2>
        <span class="panel-note">命中词与处理动作</span>
      </div>

      <div class="token-list">
        <div v-for="word in sensitiveWords" :key="word.id" class="token-card">
          <div class="token-top">
            <strong>{{ word.keyword }}</strong>
            <span class="badge">{{ word.risk_level }}</span>
          </div>
          <p>{{ word.category }} / {{ word.action }}</p>
          <small>{{ word.note || "无备注" }}</small>
          <button class="toggle-button" @click="handleToggle(word.id, !word.enabled)">
            {{ word.enabled ? "停用规则" : "启用规则" }}
          </button>
        </div>
      </div>
    </section>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchSensitiveWords, toggleSensitiveWord } from "../api/admin";
import type { SensitiveWord } from "../types/admin";
import AdminLayout from "../../../shared/layouts/AdminLayout.vue";

const sensitiveWords = ref<SensitiveWord[]>([]);

async function loadData() {
  sensitiveWords.value = await fetchSensitiveWords();
}

async function handleToggle(id: number, enabled: boolean) {
  await toggleSensitiveWord(id, enabled);
  await loadData();
}

onMounted(loadData);
</script>
