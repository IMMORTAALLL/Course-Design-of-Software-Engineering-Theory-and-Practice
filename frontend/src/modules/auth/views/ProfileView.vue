<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink, useRouter } from "vue-router";

import { updateProfile } from "../api/authApi";
import { authState, loadCurrentUser, logout } from "../stores/authStore";
import type { CurrentUser } from "../types/auth";

const router = useRouter();

const nickname = ref("");
const avatarUrl = ref("");
const bio = ref("");
const riskPreference = ref<number | "">("");
const experienceTags = ref("");
const interestMarkets = ref("");
const privacyLevel = ref<number>(0);
const loading = ref(false);
const message = ref("");
const errorMessage = ref("");
const currentUser = computed(() => authState.user as Partial<CurrentUser> | null);

function fillForm() {
  const user = authState.user as Partial<CurrentUser> | null;
  nickname.value = user?.nickname ?? "";
  avatarUrl.value = user?.avatarUrl ?? "";
  bio.value = user?.bio ?? "";
  riskPreference.value = user?.riskPreference ? user.riskPreference : "";
  experienceTags.value = user?.experienceTags?.join(", ") ?? "";
  interestMarkets.value = user?.interestMarkets?.join(", ") ?? "";
  privacyLevel.value = user?.privacyLevel ?? 0;
}

onMounted(async () => {
  if (!authState.user) {
    await loadCurrentUser();
  }
  fillForm();
});

watch(() => authState.user, fillForm);

async function saveProfile() {
  loading.value = true;
  message.value = "";
  errorMessage.value = "";
  try {
    await updateProfile({
      nickname: nickname.value.trim(),
      avatarUrl: avatarUrl.value.trim() || undefined,
      bio: bio.value.trim() || undefined,
      riskPreference: riskPreference.value === "" ? undefined : Number(riskPreference.value),
      experienceTags: experienceTags.value.split(",").map((item) => item.trim()).filter(Boolean),
      interestMarkets: interestMarkets.value.split(",").map((item) => item.trim()).filter(Boolean),
      privacyLevel: privacyLevel.value
    });
    await loadCurrentUser();
    message.value = "个人资料已更新。";
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "保存失败";
  } finally {
    loading.value = false;
  }
}

async function submitLogout() {
  await logout();
  router.push("/");
}
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>个人中心</h1>
        <p>管理你的公开资料、认证状态和风险偏好。</p>
      </div>
      <button class="secondary-button" type="button" @click="submitLogout">退出登录</button>
    </div>

    <div class="grid-2 profile-layout">
      <form class="panel form-grid" @submit.prevent="saveProfile">
        <div class="field">
          <label>昵称</label>
          <input v-model="nickname" maxlength="20" placeholder="请输入昵称" />
        </div>

        <div class="field">
          <label>头像地址</label>
          <input v-model="avatarUrl" placeholder="可填写图片 URL" />
        </div>

        <div class="field">
          <label>个人简介</label>
          <textarea v-model="bio" maxlength="255" placeholder="介绍你的投资经验、关注方向或交流偏好。"></textarea>
        </div>

        <div class="field">
          <label>风险偏好</label>
          <select v-model="riskPreference">
            <option value="">暂不设置</option>
            <option :value="1">保守型</option>
            <option :value="2">稳健型</option>
            <option :value="3">进取型</option>
          </select>
        </div>

        <div class="field">
          <label>投资经验</label>
          <input v-model="experienceTags" placeholder="例如：基金定投, A股, 量化" />
        </div>

        <div class="field">
          <label>关注市场</label>
          <input v-model="interestMarkets" placeholder="例如：沪深300, 港股, 美股" />
        </div>

        <div class="field">
          <label>隐私设置</label>
          <select v-model.number="privacyLevel">
            <option :value="0">公开</option>
            <option :value="1">部分隐藏</option>
            <option :value="2">隐藏简介和标签</option>
          </select>
        </div>

        <p v-if="message" class="info">{{ message }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="primary-button" type="submit" :disabled="loading">
          {{ loading ? "保存中..." : "保存资料" }}
        </button>
      </form>

      <aside class="panel stack">
        <div>
          <h2>{{ authState.user?.nickname || "当前用户" }}</h2>
          <p class="muted">账号状态：{{ authState.user?.status === 0 ? "正常" : authState.user?.status === 1 ? "禁言" : "封禁" }}</p>
          <p class="muted">认证等级：{{ authState.user?.authLevel === 2 ? "专业认证" : authState.user?.authLevel === 1 ? "实名认证" : "基础用户" }}</p>
          <p class="muted">等级：Lv.{{ currentUser?.level || 1 }} · 积分 {{ currentUser?.points || 0 }}</p>
          <p class="muted">发帖 {{ currentUser?.postCount || 0 }} · 加精 {{ currentUser?.eliteCount || 0 }}</p>
        </div>

        <RouterLink class="action-link" to="/me/certification">认证申请</RouterLink>
        <RouterLink class="action-link" to="/me/risk-assessment">风险测评</RouterLink>
        <RouterLink class="action-link" to="/me/notifications">通知中心</RouterLink>
        <RouterLink class="action-link" to="/me/favorites">我的收藏</RouterLink>
        <RouterLink class="action-link" to="/feed/following">Following Feed</RouterLink>
        <RouterLink class="action-link" to="/me/messages">Private Messages</RouterLink>
        <RouterLink class="action-link" to="/groups">Groups</RouterLink>
        <RouterLink v-if="authState.user?.id" class="action-link" :to="`/users/${authState.user.id}`">查看公开主页</RouterLink>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.profile-layout {
  align-items: start;
}

.field textarea {
  min-height: 150px;
}

.secondary-button {
  border: 1px solid var(--line);
  color: var(--ink);
  background: white;
  border-radius: 6px;
  padding: 10px 16px;
}

.action-link {
  display: block;
  padding: 12px 14px;
  color: var(--green);
  border: 1px solid var(--line);
  border-radius: 8px;
  font-weight: 700;
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
