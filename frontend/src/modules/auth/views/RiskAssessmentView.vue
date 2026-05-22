<script setup lang="ts">
import { ref } from "vue";

import { submitRiskAssessment } from "../api/authApi";

const questions = [
  "面对短期净值波动时，你通常能保持冷静吗？",
  "你是否能接受为追求收益承担一定本金波动？",
  "你是否具备较长期限的投资计划？",
  "你是否愿意了解股票、基金和宏观策略信息？",
  "你是否能根据风险提示调整自己的仓位？"
];

const answers = ref<number[]>([2, 2, 2, 2, 2]);
const loading = ref(false);
const resultText = ref("");
const errorMessage = ref("");

async function submitForm() {
  loading.value = true;
  resultText.value = "";
  errorMessage.value = "";
  try {
    const result = await submitRiskAssessment({ answers: answers.value });
    resultText.value = `你的风险偏好为：${result.label}`;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "测评提交失败";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h1>风险偏好测评</h1>
        <p>完成测评后，系统会更新你的风险偏好标签。</p>
      </div>
    </div>

    <form class="panel form-grid" @submit.prevent="submitForm">
      <div v-for="(question, index) in questions" :key="question" class="question">
        <div>
          <strong>{{ index + 1 }}. {{ question }}</strong>
          <p class="muted">1 表示保守，2 表示稳健，3 表示积极。</p>
        </div>
        <div class="score-options">
          <label v-for="score in [1, 2, 3]" :key="score">
            <input v-model.number="answers[index]" type="radio" :value="score" />
            <span>{{ score }}</span>
          </label>
        </div>
      </div>

      <p v-if="resultText" class="info">{{ resultText }}</p>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <button class="primary-button" type="submit" :disabled="loading">
        {{ loading ? "提交中..." : "提交测评" }}
      </button>
    </form>
  </section>
</template>

<style scoped>
.question {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 16px;
  align-items: center;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.question p {
  margin: 6px 0 0;
}

.score-options {
  display: flex;
  gap: 10px;
}

.score-options label {
  display: grid;
  width: 44px;
  height: 44px;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.score-options input {
  display: none;
}

.score-options label:has(input:checked) {
  color: white;
  background: var(--green);
  border-color: var(--green);
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

@media (max-width: 640px) {
  .question {
    grid-template-columns: 1fr;
  }
}
</style>
