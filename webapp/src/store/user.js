import Vue from 'vue';
import VueAuthenticate from 'vue-authenticate';
import VueAxios from 'vue-axios';
import axios from 'axios';
import $http from '../utils/http';
import { apiGet, apiPost } from '../utils/api';

Vue.use(VueAxios, axios);

const vueAuth = VueAuthenticate.factory(Vue.prototype.$http, {
  baseUrl: process.env.API_BASE_URL,
  registerUrl: 'auth/signup',

  bindRequestInterceptor: () => {
    /* eslint-disable no-param-reassign, dot-notation */
    $http.interceptors.request.use((request) => {
      console.log(`HTTP ${request.method} ${request.url}`);
      if (vueAuth.isAuthenticated()) {
        request.headers['Authorization'] = [
          vueAuth.options.tokenType, vueAuth.getToken(),
        ].join(' ');
      } else {
        delete request.headers['Authorization'];
      }
      return request;
    });
  },

  bindResponseInterceptor: () => {
    $http.interceptors.response.use((response) => {
      vueAuth.setToken(response);
      return response;
    }, (error) => {
      if (error.response && error.response.status === 401) {
        console.error('Authentication error, should re-login');
        vueAuth.logout();
        location.reload(); // TODO find a better way to force a login
      }
      throw error;
    });
  },
});

export default {
  state: {
    isAuthenticated: vueAuth.isAuthenticated(),
    user: {},
    user_loaded: false,
  },
  getters: {
    isAuthenticated() {
      return vueAuth.isAuthenticated();
    },
    authToken() {
      return vueAuth.getToken();
    },
  },
  mutations: {
    isAuthenticated(state, payload) {
      state.isAuthenticated = payload.isAuthenticated;
      state.user_loaded = false;
    },
    setUser(state, { user }) {
      state.user = user;
      state.user_loaded = true;
    },
  },
  actions: {
    getCurrentUser({ commit, state }) {
      return new Promise((resolve, reject) => {
        if (state.user_loaded) {
          resolve(state.user);
        } else {
          if (!state.isAuthenticated) {
            // simply drop if not authenticated
            return;
          }
          apiGet('users/me/').then((response) => {
            const user = response.data;
            commit('setUser', {
              user,
              meta: {
                analytics: [
                  ['set', 'userId', user.id],
                ],
              },
            });
            resolve(user);
          }).catch(reject);
        }
      });
    },
    login({ commit }, payload) {
      return vueAuth.login(payload.user, payload.requestOptions).then(() => {
        commit('isAuthenticated', {
          isAuthenticated: vueAuth.isAuthenticated(),
        });
      });
    },
    signup({ dispatch }, payload) {
      return new Promise((resolve, reject) => {
        console.log('send register', payload);
        vueAuth.register(payload.user, payload.requestOptions).then(() => {
          payload.user.set('grant_type', 'password');
          payload.user.set('client_id', 'webapp');
          payload.requestOptions = { config: { headers: { 'Content-Type': 'multipart/form-data' } } };
          dispatch('login', payload).then(resolve).catch(reject);
        }).catch(reject);
      });
    },
    saveClassification({ commit, state }, { user }) {
      return new Promise((resolve, reject) => {
        if (!state.isAuthenticated) {
          reject();
        }
        apiPost('classification/', user).then((response) => {
          user = response.data;
          commit('setUser', {
            user,
            meta: {
              analytics: [
                ['set', 'userId', user.id],
                ['set', 'userTreatment', user.active_treatment.name],
              ],
            },
          });
          resolve(user);
        }).catch(reject);
      });
    },
    logout({ commit }) {
      return vueAuth.logout().then(() => {
        commit('isAuthenticated', {
          isAuthenticated: false,
        });
      });
    },
  },
};
