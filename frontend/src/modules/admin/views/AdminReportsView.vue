<template>
  <AdminLayout title="举报处理">
    <section class="panel">
      <div class="panel-header">
        <h2>举报处理列表</h2>
        <span class="panel-note">用户举报入口</span>
      </div>

      <table>
        <thead>
          <tr>
            <th>目标内容</th>
            <th>举报人</th>
            <th>原因</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in reports" :key="item.id">
            <td>{{ item.target_title }}</td>
            <td>{{ item.reporter_name }}</td>
            <td>{{ item.reason }}</td>
            <td>{{ item.status }}</td>
            <td class="action-cell">
              <button class="ghost-button" @click="handleAction(item.id, 'dismissed')">驳回举报</button>
              <button class="ghost-button" @click="handleAction(item.id, 'warning_issued')">警告用户</button>
              <button class="ghost-button danger" @click="handleAction(item.id, 'banned')">封禁账号</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchReports, updateReportItem } from "../api/admin";
import type { ReportDecisionAction, ReportItem } from "../types/admin";
import AdminLayout from "../../../shared/layouts/AdminLayout.vue";

const reports = ref<ReportItem[]>([]);

async function loadData() {
  reports.value = await fetchReports();
}

async function handleAction(id: number, action: ReportDecisionAction) {
  await updateReportItem(id, action);
  await loadData();
}

onMounted(loadData);
</script>
