<script setup lang="ts">
import { ref, watch } from "vue";

import { togglePostLike } from "../api/interactionApi";

const props = defineProps<{
  postId: number;
  initialCount: number;
}>();

const count = ref(props.initialCount);
const active = ref(false);
const loading = ref(false);
const errorMessage = ref("");

watch(
  () => props.initialCount,
  (value) => {
    count.value = value;
  }
);

async function submit() {
  loading.value = true;
  errorMessage.value = "";
  try {
    const result = await togglePostLike(props.postId);
    active.value = result.active;
    count.value = result.count;
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
      {{ active ? "已赞" : "点赞" }} {{ count }}
    </button>
    <span v-if="errorMessage" class="inline-error">{{ errorMessage }}</span>
  </div>
</template>
