import { createRouter, createWebHistory } from "vue-router";

import AdminAuditView from "@/modules/admin/views/AdminAuditView.vue";
import AdminDashboard from "@/modules/admin/views/AdminDashboard.vue";
import AdminModerationView from "@/modules/admin/views/AdminModerationView.vue";
import AdminReportsView from "@/modules/admin/views/AdminReportsView.vue";
import AdminSensitiveWordsView from "@/modules/admin/views/AdminSensitiveWordsView.vue";
import AdminStatisticsView from "@/modules/admin/views/AdminStatisticsView.vue";
import HomeView from "@/modules/forum/views/HomeView.vue";
import HotRankView from "@/modules/forum/views/HotRankView.vue";
import PostCreateView from "@/modules/forum/views/PostCreateView.vue";
import PostDetailView from "@/modules/forum/views/PostDetailView.vue";
import SearchResultView from "@/modules/forum/views/SearchResultView.vue";
import SectionDetailView from "@/modules/forum/views/SectionDetailView.vue";
import SectionListView from "@/modules/forum/views/SectionListView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/sections", name: "sections", component: SectionListView },
    { path: "/sections/:id", name: "section-detail", component: SectionDetailView },
    { path: "/posts/create", name: "post-create", component: PostCreateView },
    { path: "/posts/:id", name: "post-detail", component: PostDetailView },
    { path: "/search", name: "search", component: SearchResultView },
    { path: "/hot", name: "hot", component: HotRankView },
    { path: "/admin", name: "admin-dashboard", component: AdminDashboard },
    { path: "/admin/audits", name: "admin-audits", component: AdminAuditView },
    { path: "/admin/reports", name: "admin-reports", component: AdminReportsView },
    { path: "/admin/sensitive-words", name: "admin-sensitive-words", component: AdminSensitiveWordsView },
    { path: "/admin/users", name: "admin-users", component: AdminModerationView },
    { path: "/admin/statistics", name: "admin-statistics", component: AdminStatisticsView }
  ]
});

export default router;
