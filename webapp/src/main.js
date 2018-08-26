import Vue from 'vue';
import Vue2TouchEvents from 'vue2-touch-events';
import VueLocalStorage from 'vue-localstorage';
import VueMoment from 'vue-moment';
import VueI18n from 'vue-i18n';
import Toasted from 'vue-toasted';
import VueAnalytics from 'vue-analytics';

import Logo from '@/components/elements/Logo';
import Button from '@/components/elements/Button';

import App from './App';
import router from './router';
import store from './store';

require('formdata-polyfill');

Vue.config.productionTip = false;

Vue.use(VueAnalytics, {
  id: process.env.GA_ID,
  router,
  autoTracking: {
    pageviewOnLoad: true,
  },
});

Vue.use(Vue2TouchEvents);
Vue.use(VueLocalStorage, { bind: true });
Vue.use(VueMoment);
Vue.use(VueI18n);

Vue.use(Toasted, {
  theme: 'primary',
  duration: 10000, // 10s
  position: 'top-center',
  singleton: true,
});

Vue.component('app-logo', Logo);
Vue.component('my-button', Button);

router.beforeEach((to, from, next) => {
  const authRequired = to.matched.some(route => route.meta.auth);
  const unauthRequired = to.matched.some(route => route.meta.unauth);
  const authed = store.state.user.isAuthenticated;
  if (authRequired && !authed) {
    router.authRequiredRoute = router.currentRoute;
    next('/login');
  } else if (unauthRequired && authed) {
    next('/feed');
  } else {
    next();
  }
});

const i18n = new VueI18n({
  locale: 'ko',
  fallbackLocale: 'en',
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: h => h(App),
  localStorage: {
    completedTutorials: {
      type: Object,
      default: {},
    },
  },
});
