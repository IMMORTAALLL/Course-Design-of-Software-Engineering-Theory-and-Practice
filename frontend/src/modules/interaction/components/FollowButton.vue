<script setup lang="ts">
import { ref } from "vue";

import { toggleFollow } from "../api/interactionApi";

const props = defineProps<{
  userId: number;
}>();

const following = ref(false);
const followerCount = ref<number | null>(null);
const loading = ref(false);
const errorMessage = ref("");

async function submit() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const result = await toggleFollow(props.userId);
    following.value = result.following;
    followerCount.value = result.followerCount;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "操作失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="inline-action">
    <button class="action-button" :class="{ active: following }" type="button" :disabled="loading" @click="submit">
      {{ following ? "已关注" : "关注" }}
      <span v-if="followerCount !== null">{{ followerCount }}</span>
    </button>
    <span v-if="errorMessage" class="inline-error">{{ errorMessage }}</span>
  </div>
</template>
