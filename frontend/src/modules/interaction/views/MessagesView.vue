<script setup lang="ts">
import { onMounted, ref } from "vue";

import { fetchMessages, sendMessage } from "../api/interactionApi";
import type { PrivateMessageItem } from "../types/interaction";

const messages = ref<PrivateMessageItem[]>([]);
const targetUserId = ref<number | null>(null);
const content = ref("");
const loading = ref(true);
const sending = ref(false);
const errorMessage = ref("");

async function loadMessages() {
  loading.value = true;
  errorMessage.value = "";
  try {
    messages.value = await fetchMessages();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Messages failed to load";
  } finally {
    loading.value = false;
  }
}

async function submitMessage() {
  if (!targetUserId.value || !content.value.trim()) return;
  sending.value = true;
  errorMessage.value = "";
  try {
    await sendMessage(targetUserId.value, content.value.trim());
    content.value = "";
    await loadMessages();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Message failed";
  } finally {
    sending.value = false;
  }
}

onMounted(loadMessages);
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>Private Messages</h1>
        <p>Direct conversations between community users.</p>
      </div>
    </div>

    <form class="panel message-form" @submit.prevent="submitMessage">
      <input v-model.number="targetUserId" min="1" type="number" placeholder="User ID" />
      <textarea v-model="content" maxlength="1000" placeholder="Message content"></textarea>
      <button class="primary-button" type="submit" :disabled="sending || !targetUserId || !content.trim()">Send</button>
    </form>

    <p v-if="errorMessage" class="inline-error">{{ errorMessage }}</p>
    <div v-if="loading" class="empty">Loading messages...</div>
    <div v-else-if="!messages.length" class="empty">No private messages yet.</div>
    <section v-else class="panel stack">
      <article v-for="item in messages" :key="item.id" class="message-row">
        <div>
          <strong>{{ item.senderNickname }}</strong>
          <span>to {{ item.receiverNickname }}</span>
        </div>
        <p>{{ item.content }}</p>
        <small>{{ new Date(item.createdAt).toLocaleString() }}</small>
      </article>
    </section>
  </section>
</template>

<style scoped>
.message-form {
  display: grid;
  grid-template-columns: 120px minmax(0, 1fr) auto;
  gap: 10px;
  align-items: start;
}

.message-form input,
.message-form textarea {
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.message-form textarea {
  min-height: 84px;
}

.message-row {
  display: grid;
  gap: 6px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.message-row div {
  display: flex;
  gap: 8px;
  align-items: center;
}

.message-row span,
.message-row small {
  color: var(--muted);
}

.message-row p {
  margin: 0;
  line-height: 1.7;
}

@media (max-width: 640px) {
  .message-form {
    grid-template-columns: 1fr;
  }
}
</style>
