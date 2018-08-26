const localeMixin = {
  data() { return { locale: 'en' }; },
  watch: {
    locale(val) {
      this.$i18n.locale = val;
    },
  },
};


const navigationMixins = {
  computed: {
    isMenuOpened() {
      return this.$store.state.ui.menuOpen;
    },
    isAuthenticated() {
      return this.$store.state.user.isAuthenticated;
    },
    authToken() {
      return this.$store.getters.authToken;
    },
    user() {
      if (this.$store.state.user.isAuthenticated && this.$store.state.user.user.active_treatment.name === 'default') {
        this.$router.push('signup-test');
      }
      return this.$store.state.user.user;
    },
    treatmentName() {
      if (this.$store.state.user.isAuthenticated && this.$store.state.user.user.active_treatment) {
        return this.$store.state.user.user.active_treatment.name;
      }
      return false;
    },
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    gotoRoute(route) {
      this.$router.push(route);
    },
    toggleMenu() {
      this.$store.dispatch('toggleMenu');
    },
    showMenu() {
      this.$store.commit('setMenuOpened', true);
    },
    hideMenu() {
      this.$store.commit('setMenuOpened', false);
    },
    logout() {
      return this.$store.dispatch('logout').then(() => {
        this.$store.commit('setMenuOpened', false);
        this.$router.push('/');
      }).catch(() => {
        console.log('wow, error?');
      });
    },
  },
};

export {
  navigationMixins,
  localeMixin,
};
