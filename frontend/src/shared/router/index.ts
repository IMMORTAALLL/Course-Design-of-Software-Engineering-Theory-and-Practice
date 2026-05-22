import { createRouter, createWebHistory } from "vue-router";

import CertificationView from "@/modules/auth/views/CertificationView.vue";
import LoginView from "@/modules/auth/views/LoginView.vue";
import ProfileView from "@/modules/auth/views/ProfileView.vue";
import RegisterView from "@/modules/auth/views/RegisterView.vue";
import RiskAssessmentView from "@/modules/auth/views/RiskAssessmentView.vue";
import UserPublicView from "@/modules/auth/views/UserPublicView.vue";
import HomeView from "@/modules/forum/views/HomeView.vue";
import HotRankView from "@/modules/forum/views/HotRankView.vue";
import PostCreateView from "@/modules/forum/views/PostCreateView.vue";
import PostDetailView from "@/modules/forum/views/PostDetailView.vue";
import SearchResultView from "@/modules/forum/views/SearchResultView.vue";
import SectionDetailView from "@/modules/forum/views/SectionDetailView.vue";
import SectionListView from "@/modules/forum/views/SectionListView.vue";
import { hasAuthToken } from "@/modules/auth/stores/authStore";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/login", name: "login", component: LoginView },
    { path: "/register", name: "register", component: RegisterView },
    { path: "/me", name: "profile", component: ProfileView, meta: { requiresAuth: true } },
    { path: "/me/certification", name: "certification", component: CertificationView, meta: { requiresAuth: true } },
    { path: "/me/risk-assessment", name: "risk-assessment", component: RiskAssessmentView, meta: { requiresAuth: true } },
    { path: "/users/:id", name: "user-public", component: UserPublicView },
    { path: "/sections", name: "sections", component: SectionListView },
    { path: "/sections/:id", name: "section-detail", component: SectionDetailView },
    { path: "/posts/create", name: "post-create", component: PostCreateView, meta: { requiresAuth: true } },
    { path: "/posts/:id", name: "post-detail", component: PostDetailView },
    { path: "/search", name: "search", component: SearchResultView },
    { path: "/hot", name: "hot", component: HotRankView }
  ]
});

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !hasAuthToken()) {
    return {
      path: "/login",
      query: { redirect: to.fullPath }
    };
  }
});

export default router;
