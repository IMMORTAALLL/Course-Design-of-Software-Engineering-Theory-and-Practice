import { createApp } from "vue";

import App from "./App.vue";
import router from "./shared/router";
import "./shared/styles/base.css";

createApp(App).use(router).mount("#app");
