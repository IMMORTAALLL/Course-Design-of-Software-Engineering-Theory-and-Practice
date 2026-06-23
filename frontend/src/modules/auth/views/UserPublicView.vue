<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import FollowButton from "@/modules/interaction/components/FollowButton.vue";
import { fetchFollowers, fetchFollowing, setStarredFollow } from "@/modules/interaction/api/interactionApi";
import type { UserBrief } from "@/modules/interaction/types/interaction";
import { fetchPublicUser } from "../api/authApi";
import type { PublicUser } from "../types/auth";

const route = useRoute();
const user = ref<PublicUser | null>(null);
const followers = ref<UserBrief[]>([]);
const following = ref<UserBrief[]>([]);
const loading = ref(true);
const errorMessage = ref("");
const starMessage = ref("");

async function loadUser() {
  const id = Number(route.params.id);
  if (!Number.isFinite(id)) {
    errorMessage.value = "用户 ID 不合法。";
    loading.value = false;
    return;
  }

  loading.value = true;
  errorMessage.value = "";
  try {
    const [userData, followerData, followingData] = await Promise.all([
      fetchPublicUser(id),
      fetchFollowers(id),
      fetchFollowing(id)
    ]);
    user.value = userData;
    followers.value = followerData;
    following.value = followingData;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "用户信息加载失败";
  } finally {
    loading.value = false;
  }
}

async function submitStarredFollow() {
  if (!user.value) return;
  starMessage.value = "";
  try {
    await setStarredFollow(user.value.id, true);
    starMessage.value = "Special follow enabled.";
  } catch (error) {
    starMessage.value = error instanceof Error ? error.message : "Special follow failed.";
  }
}

onMounted(loadUser);
watch(() => route.params.id, loadUser);
</script>

<template>
  <section class="page">
    <div v-if="loading" class="empty">正在加载用户主页...</div>
    <div v-else-if="errorMessage" class="empty">{{ errorMessage }}</div>

    <div v-else-if="user" class="panel public-card">
      <div class="avatar">
        <img v-if="user.avatarUrl" :src="user.avatarUrl" alt="用户头像" />
        <span v-else>{{ user.nickname?.slice(0, 1) || "用" }}</span>
      </div>

      <div>
        <h1>{{ user.nickname || "未命名用户" }}</h1>
        <div class="meta">
          <span>{{ user.authLevel === 2 ? "专业认证" : user.authLevel === 1 ? "实名认证" : "基础用户" }}</span>
          <span>影响力值 {{ user.influenceScore }}</span>
          <span>粉丝 {{ followers.length }}</span>
          <span>关注 {{ following.length }}</span>
        </div>
        <p class="bio">{{ user.bio || "这个用户还没有填写简介。" }}</p>
        <div class="profile-tags">
          <span>Lv.{{ user.level }}</span>
          <span>{{ user.postCount }} posts</span>
          <span v-for="item in user.experienceTags" :key="`exp-${item}`">{{ item }}</span>
          <span v-for="item in user.interestMarkets" :key="`market-${item}`">{{ item }}</span>
        </div>
        <FollowButton :user-id="user.id" />
        <button class="secondary-button star-button" type="button" @click="submitStarredFollow">Special Follow</button>
        <p v-if="starMessage" class="muted">{{ starMessage }}</p>
      </div>
    </div>

    <div v-if="user" class="grid-2 social-grid">
      <section class="panel stack">
        <h2>粉丝</h2>
        <div v-if="!followers.length" class="empty">暂无粉丝。</div>
        <RouterLink v-for="item in followers" v-else :key="item.id" class="user-row" :to="`/users/${item.id}`">
          <span>{{ item.nickname || "社区用户" }}</span>
          <small>{{ item.authLevel === 2 ? "专业认证" : item.authLevel === 1 ? "实名认证" : "基础用户" }}</small>
        </RouterLink>
      </section>

      <section class="panel stack">
        <h2>关注</h2>
        <div v-if="!following.length" class="empty">暂无关注。</div>
        <RouterLink v-for="item in following" v-else :key="item.id" class="user-row" :to="`/users/${item.id}`">
          <span>{{ item.nickname || "社区用户" }}</span>
          <small>{{ item.authLevel === 2 ? "专业认证" : item.authLevel === 1 ? "实名认证" : "基础用户" }}</small>
        </RouterLink>
      </section>
    </div>
  </section>
</template>

<style scoped>
.public-card {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

.avatar {
  display: grid;
  width: 86px;
  height: 86px;
  place-items: center;
  overflow: hidden;
  color: white;
  background: var(--green);
  border-radius: 8px;
  font-size: 30px;
  font-weight: 800;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h1 {
  margin: 0 0 10px;
}

h2 {
  margin: 0;
  font-size: 20px;
}

.bio {
  margin-top: 18px;
  color: var(--ink);
  line-height: 1.8;
}

.profile-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0;
}

.profile-tags span {
  padding: 6px 10px;
  color: var(--green);
  background: #eef8f2;
  border: 1px solid var(--line);
  border-radius: 8px;
  font-weight: 700;
}

.star-button {
  margin-left: 10px;
}

.social-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: 20px;
}

.user-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.user-row span {
  font-weight: 700;
}

.user-row small {
  color: var(--muted);
}

@media (max-width: 560px) {
  .public-card {
    grid-template-columns: 1fr;
  }

  .social-grid {
    grid-template-columns: 1fr;
  }
}
</style>
