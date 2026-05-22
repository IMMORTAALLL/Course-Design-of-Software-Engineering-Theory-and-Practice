<template>
  <AdminLayout title="用户处罚">
    <section class="panel">
      <div class="panel-header">
        <h2>处罚记录</h2>
        <span class="panel-note">警告 / 禁言 / 封号</span>
      </div>

      <table>
        <thead>
          <tr>
            <th>用户</th>
            <th>动作</th>
            <th>原因</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in records" :key="item.id">
            <td>{{ item.user_name }}</td>
            <td>{{ item.action }}</td>
            <td>{{ item.reason }}</td>
            <td>{{ item.status }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchUserModerationRecords } from "../api/admin";
import type { UserModerationRecord } from "../types/admin";
import AdminLayout from "../../../shared/layouts/AdminLayout.vue";

const records = ref<UserModerationRecord[]>([]);

async function loadData() {
  records.value = await fetchUserModerationRecords();
}

onMounted(loadData);
</script>
