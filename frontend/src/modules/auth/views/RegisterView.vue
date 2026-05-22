<script setup lang="ts">
import { computed, ref } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { register, sendVerifyCode } from "../api/authApi";
import type { AccountType } from "../types/auth";

const router = useRouter();

const accountType = ref<AccountType>("phone");
const accountValue = ref("");
const nickname = ref("");
const password = ref("");
const verifyCode = ref("");
const loading = ref(false);
const sending = ref(false);
const errorMessage = ref("");
const infoMessage = ref("");

const accountLabel = computed(() => (accountType.value === "phone" ? "手机号" : "邮箱"));

async function requestVerifyCode() {
  if (!accountValue.value.trim()) {
    errorMessage.value = `请输入${accountLabel.value}。`;
    return;
  }
  sending.value = true;
  errorMessage.value = "";
  infoMessage.value = "";
  try {
    const result = await sendVerifyCode({
      accountType: accountType.value,
      target: accountValue.value.trim()
    });
    infoMessage.value = `${result.message}：${result.code}`;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "验证码发送失败";
  } finally {
    sending.value = false;
  }
}

async function submitRegister() {
  if (!accountValue.value.trim() || !nickname.value.trim() || !password.value || !verifyCode.value.trim()) {
    errorMessage.value = "请完整填写注册信息。";
    return;
  }

  loading.value = true;
  errorMessage.value = "";
  try {
    await register({
      accountType: accountType.value,
      phone: accountType.value === "phone" ? accountValue.value.trim() : undefined,
      email: accountType.value === "email" ? accountValue.value.trim() : undefined,
      password: password.value,
      nickname: nickname.value.trim(),
      verifyCode: verifyCode.value.trim()
    });
    router.push({ path: "/login", query: { registered: "1" } });
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "注册失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section class="page auth-page">
    <div class="panel auth-panel">
      <div class="auth-heading">
        <h1>创建账号</h1>
        <p>注册后即可参与股票基金讨论，发布观点并管理个人资料。</p>
      </div>

      <form class="form-grid" @submit.prevent="submitRegister">
        <div class="field">
          <label>注册方式</label>
          <select v-model="accountType">
            <option value="phone">手机号注册</option>
            <option value="email">邮箱注册</option>
          </select>
        </div>

        <div class="field">
          <label>{{ accountLabel }}</label>
          <div class="inline-field">
            <input v-model="accountValue" :placeholder="`请输入${accountLabel}`" />
            <button type="button" @click="requestVerifyCode" :disabled="sending">
              {{ sending ? "发送中..." : "获取验证码" }}
            </button>
          </div>
        </div>

        <div class="field">
          <label>验证码</label>
          <input v-model="verifyCode" placeholder="请输入验证码" />
        </div>

        <div class="field">
          <label>昵称</label>
          <input v-model="nickname" maxlength="20" placeholder="2-20个字符" />
        </div>

        <div class="field">
          <label>密码</label>
          <input v-model="password" type="password" autocomplete="new-password" placeholder="至少8位，包含字母和数字" />
        </div>

        <p v-if="infoMessage" class="info">{{ infoMessage }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          {{ loading ? "注册中..." : "注册" }}
        </button>
      </form>

      <p class="auth-switch">
        已有账号？
        <RouterLink to="/login">去登录</RouterLink>
      </p>
    </div>
  </section>
</template>

<style scoped>
.auth-page {
  display: grid;
  place-items: start center;
}

.auth-panel {
  width: min(520px, 100%);
}

.auth-heading {
  margin-bottom: 20px;
}

.auth-heading h1 {
  margin: 0;
  font-size: 28px;
}

.auth-heading p,
.auth-switch {
  color: var(--muted);
}

.auth-switch a {
  color: var(--green);
  font-weight: 700;
}

.inline-field {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
}

.inline-field button {
  border: 1px solid var(--green);
  color: var(--green);
  background: white;
  border-radius: 8px;
  padding: 0 14px;
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

button:disabled {
  cursor: wait;
  opacity: 0.72;
}

@media (max-width: 520px) {
  .inline-field {
    grid-template-columns: 1fr;
  }

  .inline-field button {
    min-height: 42px;
  }
}
</style>
