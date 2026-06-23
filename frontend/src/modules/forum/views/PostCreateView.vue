<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { addPostPollOption, createAnalysisPost, createPost, fetchSections, fetchTags } from "../api/forumApi";
import type { Section, Tag } from "../types/forum";

const router = useRouter();
const sections = ref<Section[]>([]);
const tags = ref<Tag[]>([]);
const sectionId = ref<number | null>(null);
const title = ref("");
const content = ref("");
const postMode = ref<"normal" | "analysis" | "poll" | "short">("normal");
const pollOptionsText = ref("");
const selectedTags = ref<number[]>([]);
const saving = ref(false);
const errorMessage = ref("");

onMounted(async () => {
  const [sectionData, tagData] = await Promise.all([fetchSections(), fetchTags()]);
  sections.value = sectionData;
  tags.value = tagData;
  sectionId.value = sectionData[0]?.id ?? null;
});

async function submitPost() {
  if (!sectionId.value || !title.value.trim() || !content.value.trim()) {
    errorMessage.value = "请选择板块，并填写标题和正文。";
    return;
  }
  saving.value = true;
  errorMessage.value = "";
  try {
    const postTypeMap = {
      normal: 1,
      analysis: 2,
      poll: 3,
      short: 4
    };
    const payload = {
      section_id: sectionId.value,
      title: title.value.trim(),
      content: content.value.trim(),
      post_type: postTypeMap[postMode.value],
      tag_ids: selectedTags.value
    };
    const post = postMode.value === "analysis" ? await createAnalysisPost(payload) : await createPost(payload);
    if (postMode.value === "poll") {
      const options = pollOptionsText.value
        .split("\n")
        .map((item) => item.trim())
        .filter(Boolean)
        .slice(0, 8);
      await Promise.all(options.map((option) => addPostPollOption(post.id, option)));
    }
    router.push(`/posts/${post.id}`);
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "发布失败";
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>发布帖子</h1>
        <p>分享你的股票基金观点，并添加相关标签方便检索。</p>
      </div>
    </div>

    <form class="panel form-grid" @submit.prevent="submitPost">
      <div class="field">
        <label>所属板块</label>
        <select v-model.number="sectionId">
          <option v-for="section in sections" :key="section.id" :value="section.id">
            {{ section.name }}
          </option>
        </select>
      </div>

      <div class="field">
        <label>帖子标题</label>
        <input v-model="title" maxlength="120" placeholder="例如：A股震荡时如何看待新能源板块？" />
      </div>

      <div class="field">
        <label>内容类型</label>
        <select v-model="postMode">
          <option value="poll">Poll</option>
          <option value="short">Short update</option>
          <option value="normal">普通帖子</option>
          <option value="analysis">长文分析</option>
        </select>
      </div>

      <div class="field">
        <label>正文内容</label>
        <textarea v-model="content" placeholder="写下你的分析、观点或问题。"></textarea>
      </div>

      <div class="field">
        <label>股票/基金/主题标签</label>
        <div class="check-grid">
          <label v-for="tag in tags" :key="tag.id" class="check-item">
            <input v-model="selectedTags" type="checkbox" :value="tag.id" />
            <span>{{ tag.name }} · {{ tag.tag_type }}</span>
          </label>
        </div>
      </div>

      <div v-if="postMode === 'poll'" class="field">
        <label>鎶曠エ閫夐」</label>
        <textarea v-model="pollOptionsText" placeholder="姣忚涓€涓€夐」锛屾渶澶?8 椤?"></textarea>
      </div>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <button class="primary-button" type="submit" :disabled="saving">
        {{ saving ? "发布中..." : "提交发布" }}
      </button>
    </form>
  </section>
</template>

<style scoped>
.check-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
}

.check-item {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 10px;
  border: 1px solid #d8e0dc;
  border-radius: 8px;
}

.error {
  margin: 0;
  color: #c23b31;
  font-weight: 700;
}

button:disabled {
  cursor: wait;
  opacity: 0.72;
}
</style>
