import { createRouter, createWebHistory } from "vue-router";

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
    { path: "/hot", name: "hot", component: HotRankView }
  ]
});

export default router;
