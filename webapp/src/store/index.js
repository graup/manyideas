import Vue from 'vue';
import Vuex from 'vuex';

import { analyticsMiddleware } from 'vue-analytics';

import user from './user';
import ui from './ui';
import issue from './issue';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    ui,
    issue,
  },
  plugins: [
    analyticsMiddleware,
  ],
});
