<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchCertificationStatus, submitCertification } from "../api/authApi";
import type { CertificationType } from "../types/auth";

const certificationType = ref<CertificationType>("REAL_NAME");
const realName = ref("");
const materialText = ref("");
const statusText = ref("加载中...");
const loading = ref(false);
const message = ref("");
const errorMessage = ref("");

async function loadStatus() {
  try {
    const status = await fetchCertificationStatus();
    statusText.value = status.status;
  } catch (error) {
    statusText.value = error instanceof Error ? error.message : "认证状态获取失败";
  }
}

onMounted(loadStatus);

async function submitForm() {
  if (!realName.value.trim()) {
    errorMessage.value = "请填写真实姓名。";
    return;
  }
  loading.value = true;
  message.value = "";
  errorMessage.value = "";
  try {
    const materialUrls = materialText.value
      .split("\n")
      .map((item) => item.trim())
      .filter(Boolean);
    const result = await submitCertification({
      certificationType: certificationType.value,
      realName: realName.value.trim(),
      materialUrls
    });
    message.value = result.message;
    await loadStatus();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "提交失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>认证申请</h1>
        <p>提交实名或专业认证信息，提升社区内容可信度。</p>
      </div>
    </div>

    <div class="grid-2">
      <form class="panel form-grid" @submit.prevent="submitForm">
        <div class="field">
          <label>认证类型</label>
          <select v-model="certificationType">
            <option value="REAL_NAME">实名认证</option>
            <option value="PROFESSIONAL">专业认证</option>
          </select>
        </div>

        <div class="field">
          <label>真实姓名</label>
          <input v-model="realName" placeholder="请输入真实姓名" />
        </div>

        <div class="field">
          <label>材料链接</label>
          <textarea v-model="materialText" placeholder="每行填写一个证明材料链接，可暂留空。"></textarea>
        </div>

        <p v-if="message" class="info">{{ message }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          {{ loading ? "提交中..." : "提交认证" }}
        </button>
      </form>

      <aside class="panel">
        <h2>当前认证状态</h2>
        <p class="status-text">{{ statusText }}</p>
        <p class="muted">课程阶段认证接口采用模拟通过，用于展示认证流程和前后端联调。</p>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.field textarea {
  min-height: 160px;
}

.status-text {
  color: var(--green);
  font-size: 22px;
  font-weight: 800;
}

.info,
.error {
  margin: 0;
  font-weight: 700;
}

.info {
  color: var(--green);
}

.error {
  color: var(--red);
}
</style>
