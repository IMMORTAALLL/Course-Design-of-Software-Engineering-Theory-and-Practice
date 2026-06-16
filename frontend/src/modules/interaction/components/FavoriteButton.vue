<script setup lang="ts">
import { ref } from "vue";

import { togglePostFavorite } from "../api/interactionApi";

const props = defineProps<{
  postId: number;
}>();

const active = ref(false);
const loading = ref(false);
const errorMessage = ref("");

async function submit() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const result = await togglePostFavorite(props.postId);
    active.value = result.active;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "操作失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="inline-action">
    <button class="action-button" :class="{ active }" type="button" :disabled="loading" @click="submit">
      {{ active ? "已收藏" : "收藏" }}
    </button>
    <span v-if="errorMessage" class="inline-error">{{ errorMessage }}</span>
  </div>
</template>
