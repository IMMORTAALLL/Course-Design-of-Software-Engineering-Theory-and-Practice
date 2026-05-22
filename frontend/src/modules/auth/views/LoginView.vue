<script setup lang="ts">
import { ref } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";

import { login } from "../stores/authStore";

const route = useRoute();
const router = useRouter();

const account = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");

async function submitLogin() {
  if (!account.value.trim() || !password.value) {
    errorMessage.value = "请输入手机号/邮箱和密码。";
    return;
  }

  loading.value = true;
  errorMessage.value = "";
  try {
    await login({ account: account.value.trim(), password: password.value });
    const redirect = typeof route.query.redirect === "string" ? route.query.redirect : "/";
    router.push(redirect);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "登录失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section class="page auth-page">
    <div class="panel auth-panel">
      <div class="auth-heading">
        <h1>登录智投社区</h1>
        <p>登录后可以发布帖子、参与评论、收藏内容和提交认证。</p>
      </div>

      <form class="form-grid" @submit.prevent="submitLogin">
        <div class="field">
          <label>手机号或邮箱</label>
          <input v-model="account" autocomplete="username" placeholder="请输入手机号或邮箱" />
        </div>

        <div class="field">
          <label>密码</label>
          <input v-model="password" autocomplete="current-password" type="password" placeholder="请输入密码" />
        </div>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          {{ loading ? "登录中..." : "登录" }}
        </button>
      </form>

      <p class="auth-switch">
        还没有账号？
        <RouterLink to="/register">去注册</RouterLink>
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
  width: min(460px, 100%);
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

.error {
  margin: 0;
  color: var(--red);
  font-weight: 700;
}

button:disabled {
  cursor: wait;
  opacity: 0.72;
}
</style>
