export default {
  state: {
    menuOpen: false,
  },
  mutations: {
    setMenuOpened(state, payload) {
      state.menuOpen = payload;
    },
  },
  actions: {
    toggleMenu({ commit, state }) {
      commit('setMenuOpened', !state.menuOpen);
    },
  },
};
