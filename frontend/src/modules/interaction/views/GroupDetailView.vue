<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import {
  createGroupPost,
  createGroupResource,
  fetchGroup,
  fetchGroupPosts,
  fetchGroupResources,
  joinGroup,
  leaveGroup
} from "../api/interactionApi";
import type { GroupItem, GroupPostItem, GroupResourceItem } from "../types/interaction";

const route = useRoute();
const groupId = computed(() => Number(route.params.id));
const group = ref<GroupItem | null>(null);
const groupPosts = ref<GroupPostItem[]>([]);
const groupResources = ref<GroupResourceItem[]>([]);
const postContent = ref("");
const resourceTitle = ref("");
const resourceUrl = ref("");
const resourceDescription = ref("");
const loading = ref(true);
const acting = ref(false);
const errorMessage = ref("");

const membershipButtonText = computed(() => {
  if (!group.value) return "";
  if (group.value.pending) return "申请中";
  if (group.value.joined) return "退出群组";
  return group.value.permission === 2 ? "申请加入" : "加入群组";
});

async function loadData() {
  loading.value = true;
  errorMessage.value = "";
  try {
    group.value = await fetchGroup(groupId.value);
    if (group.value.joined) {
      const [posts, resources] = await Promise.all([
        fetchGroupPosts(groupId.value),
        fetchGroupResources(groupId.value)
      ]);
      groupPosts.value = posts;
      groupResources.value = resources;
    } else {
      groupPosts.value = [];
      groupResources.value = [];
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "群组加载失败";
  } finally {
    loading.value = false;
  }
}

async function toggleMembership() {
  if (!group.value || group.value.pending) return;
  acting.value = true;
  errorMessage.value = "";
  try {
    group.value = group.value.joined ? await leaveGroup(group.value.id) : await joinGroup(group.value.id);
    await loadData();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "操作失败";
  } finally {
    acting.value = false;
  }
}

async function submitGroupPost() {
  const content = postContent.value.trim();
  if (!group.value || !content) return;
  acting.value = true;
  errorMessage.value = "";
  try {
    await createGroupPost(group.value.id, content);
    postContent.value = "";
    groupPosts.value = await fetchGroupPosts(group.value.id);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Group post failed";
  } finally {
    acting.value = false;
  }
}

async function submitGroupResource() {
  if (!group.value || !resourceTitle.value.trim() || !resourceUrl.value.trim()) return;
  acting.value = true;
  errorMessage.value = "";
  try {
    await createGroupResource(group.value.id, {
      title: resourceTitle.value.trim(),
      resourceUrl: resourceUrl.value.trim(),
      description: resourceDescription.value.trim() || undefined
    });
    resourceTitle.value = "";
    resourceUrl.value = "";
    resourceDescription.value = "";
    groupResources.value = await fetchGroupResources(group.value.id);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Group resource failed";
  } finally {
    acting.value = false;
  }
}

onMounted(loadData);
watch(groupId, loadData);
</script>

<template>
  <section class="page">
    <div v-if="loading" class="empty">正在加载群组...</div>
    <div v-else-if="errorMessage && !group" class="empty">{{ errorMessage }}</div>

    <template v-else-if="group">
      <div class="panel group-hero">
        <div>
          <p class="muted">{{ group.permission === 1 ? "公开群组" : group.permission === 2 ? "需审核群组" : "私密群组" }}</p>
          <h1>{{ group.name }}</h1>
          <p>{{ group.description || "暂无群组简介。" }}</p>
          <div class="meta">
            <span>群主 {{ group.creatorNickname }}</span>
            <span>{{ group.memberCount }} 位成员</span>
            <span>{{ new Date(group.createdAt).toLocaleString() }}</span>
          </div>
        </div>
        <button class="primary-button" type="button" :disabled="acting || group.pending" @click="toggleMembership">
          {{ membershipButtonText }}
        </button>
      </div>

      <p v-if="errorMessage" class="inline-error">{{ errorMessage }}</p>

      <section class="panel stack">
        <form v-if="group.joined" class="inline-form" @submit.prevent="submitGroupPost">
          <textarea v-model="postContent" maxlength="1000" placeholder="Share a group update"></textarea>
          <button class="primary-button" type="submit" :disabled="acting || !postContent.trim()">Publish</button>
        </form>
        <p v-if="!group.joined" class="muted">Join the group to view discussions and resources.</p>
        <div v-else-if="!groupPosts.length" class="empty">No group discussion yet.</div>
        <article v-for="item in groupPosts" v-else :key="item.id" class="group-item">
          <strong>{{ item.authorNickname }}</strong>
          <p>{{ item.content }}</p>
          <small>{{ new Date(item.createdAt).toLocaleString() }}</small>
        </article>
        <h2>群内讨论</h2>
        <p class="muted">群内暂时还没有公开讨论内容。</p>
      </section>
      <section v-if="group.joined" class="panel stack">
        <h2>Group Resources</h2>
        <form class="resource-form" @submit.prevent="submitGroupResource">
          <input v-model="resourceTitle" maxlength="120" placeholder="Title" />
          <input v-model="resourceUrl" maxlength="255" placeholder="URL" />
          <input v-model="resourceDescription" maxlength="255" placeholder="Description" />
          <button class="primary-button" type="submit" :disabled="acting || !resourceTitle.trim() || !resourceUrl.trim()">Add</button>
        </form>
        <div v-if="!groupResources.length" class="empty">No resources yet.</div>
        <a
          v-for="item in groupResources"
          v-else
          :key="item.id"
          class="group-item"
          :href="item.resourceUrl"
          target="_blank"
          rel="noreferrer"
        >
          <strong>{{ item.title }}</strong>
          <span>{{ item.description || item.resourceUrl }}</span>
          <small>{{ item.authorNickname }} · {{ new Date(item.createdAt).toLocaleString() }}</small>
        </a>
      </section>
    </template>
  </section>
</template>

<style scoped>
.group-hero {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
}

h1,
h2 {
  margin: 0;
}

.group-hero p {
  line-height: 1.8;
}

.inline-form,
.resource-form {
  display: grid;
  gap: 10px;
}

.inline-form textarea {
  min-height: 96px;
}

.resource-form {
  grid-template-columns: minmax(120px, 1fr) minmax(160px, 1.4fr) minmax(120px, 1fr) auto;
}

.resource-form input,
.inline-form textarea {
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.group-item {
  display: grid;
  gap: 6px;
  padding: 12px;
  color: var(--ink);
  border: 1px solid var(--line);
  border-radius: 8px;
}

.group-item p {
  margin: 0;
  color: var(--ink-soft);
  line-height: 1.7;
}

.group-item small,
.group-item span {
  color: var(--muted);
}

@media (max-width: 640px) {
  .group-hero {
    flex-direction: column;
  }

  .resource-form {
    grid-template-columns: 1fr;
  }
}
</style>
