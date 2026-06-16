<template>
  <AdminLayout title="内容审核">
    <section class="panel">
      <div class="panel-header">
        <h2>待审核内容</h2>
        <span class="panel-note">帖子 / 评论 / 附件</span>
      </div>

      <table>
        <thead>
          <tr>
            <th>内容</th>
            <th>作者</th>
            <th>原因</th>
            <th>风险</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in auditQueue" :key="item.id">
            <td>{{ item.title }}</td>
            <td>{{ item.author_name }}</td>
            <td>{{ item.reason }}</td>
            <td><span class="badge">{{ item.risk_level }}</span></td>
            <td><span class="badge">{{ item.status }}</span></td>
            <td class="action-cell">
              <button class="ghost-button" @click="handleAction(item.id, 'approve')">通过</button>
              <button class="ghost-button danger" @click="handleAction(item.id, 'reject')">驳回</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchAuditQueue, updateAuditQueueItem } from "../api/admin";
import type { AuditDecisionAction, AuditQueueItem } from "../types/admin";
import AdminLayout from "../../../shared/layouts/AdminLayout.vue";

const auditQueue = ref<AuditQueueItem[]>([]);

async function loadData() {
  auditQueue.value = await fetchAuditQueue();
}

async function handleAction(id: number, action: AuditDecisionAction) {
  await updateAuditQueueItem(id, action);
  await loadData();
}

onMounted(loadData);
</script>
