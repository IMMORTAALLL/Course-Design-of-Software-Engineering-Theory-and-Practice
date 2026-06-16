<script setup lang="ts">
import { ref } from "vue";

const props = withDefaults(
  defineProps<{
    placeholder?: string;
    submitText?: string;
  }>(),
  {
    placeholder: "写下你的观点，注意投资内容风险提示。",
    submitText: "发布评论"
  }
);

const emit = defineEmits<{
  submit: [content: string];
}>();

const content = ref("");
const errorMessage = ref("");

function submit() {
  const value = content.value.trim();
  if (!value) {
    errorMessage.value = "内容不能为空。";
    return;
  }
  errorMessage.value = "";
  emit("submit", value);
  content.value = "";
}
</script>

<template>
  <form class="comment-editor" @submit.prevent="submit">
    <textarea v-model="content" :placeholder="props.placeholder"></textarea>
    <div class="editor-footer">
      <span v-if="errorMessage" class="inline-error">{{ errorMessage }}</span>
      <button class="primary-button" type="submit">{{ props.submitText }}</button>
    </div>
  </form>
</template>

<style scoped>
.comment-editor {
  display: grid;
  gap: 10px;
}

textarea {
  width: 100%;
  min-height: 110px;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 12px;
  resize: vertical;
}

.editor-footer {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}
</style>
