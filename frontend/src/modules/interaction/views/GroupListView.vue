<script setup lang="ts">
import { onMounted, ref } from "vue";

import { createGroup, fetchGroups } from "../api/interactionApi";
import GroupCard from "../components/GroupCard.vue";
import type { GroupItem } from "../types/interaction";

const groups = ref<GroupItem[]>([]);
const loading = ref(true);
const saving = ref(false);
const errorMessage = ref("");
const name = ref("");
const description = ref("");
const permission = ref<1 | 2 | 3>(1);

async function loadData() {
  loading.value = true;
  try {
    groups.value = await fetchGroups();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "群组加载失败";
  } finally {
    loading.value = false;
  }
}

async function submitGroup() {
  const groupName = name.value.trim();
  if (!groupName) {
    errorMessage.value = "群组名称不能为空。";
    return;
  }
  saving.value = true;
  errorMessage.value = "";
  try {
    await createGroup({
      name: groupName,
      description: description.value.trim() || undefined,
      permission: permission.value
    });
    name.value = "";
    description.value = "";
    permission.value = 1;
    await loadData();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "创建群组失败";
  } finally {
    saving.value = false;
  }
}

onMounted(loadData);
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>投资群组</h1>
        <p>按投资主题建立私域交流圈，沉淀策略讨论和资料分享。</p>
      </div>
    </div>

    <div class="grid-2">
      <div class="stack">
        <div v-if="loading" class="empty">正在加载群组...</div>
        <div v-else-if="!groups.length" class="empty">暂无群组。</div>
        <GroupCard v-for="group in groups" v-else :key="group.id" :group="group" />
      </div>

      <aside class="panel">
        <h2>创建群组</h2>
        <form class="form-grid" @submit.prevent="submitGroup">
          <div class="field">
            <label>群组名称</label>
            <input v-model="name" maxlength="50" placeholder="例如：量化策略研究小组" />
          </div>
          <div class="field">
            <label>群组简介</label>
            <textarea v-model="description" maxlength="255" placeholder="说明群组主题和交流边界。"></textarea>
          </div>
          <div class="field">
            <label>权限类型</label>
            <select v-model.number="permission">
              <option :value="1">公开</option>
              <option :value="2">需审核</option>
              <option :value="3">私密</option>
            </select>
          </div>
          <p v-if="errorMessage" class="inline-error">{{ errorMessage }}</p>
          <button class="primary-button" type="submit" :disabled="saving">{{ saving ? "创建中..." : "创建群组" }}</button>
        </form>
      </aside>
    </div>
  </section>
</template>

<style scoped>
h2 {
  margin: 0 0 16px;
  font-size: 20px;
}

.field textarea {
  min-height: 120px;
}
</style>
