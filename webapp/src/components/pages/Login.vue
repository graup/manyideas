<template>
  <div class="viewport hello has-header">
    <header>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
      <div class="view-title">{{$t('login')}}</div>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
    </header>

    <main class="content">

      <div class="form-wrapper">
        
        <form action="" class="form">
          <div class="form-group">
            <input id="username" class="form-input" type="text" v-model="username" required />
            <label class="form-label" for="username">{{$t('username-email')}}</label>
          </div>
          <div class="form-group">
            <input id="password" class="form-input" type="password" v-model="password" required />
            <label class="form-label" for="password">{{$t('password')}}</label>
            <div class="error" v-if="error">{{error}}</div>
          </div>
          <div class="form-group button-group vertical spaced" style="max-width: 200px;">
            <my-button :text="$t('login')" primary={true} v-on:click.native.capture="login" v-bind:loading="loading" />
          </div>
        </form>
      </div>

      <p class="sub-login-text" v-on:click="gotoSignup">{{$t('go-to-signup')}}</p>
      
    </main>
    <footer></footer>
  </div>
</template>

<i18n>
{
  "en": {
    "username-email": "Username or email",
    "password": "Password",
    "login": "Log in",
    "login-button": "Log in",
    "go-to-signup": "Sign up now"
  },
  "ko": {
    "username-email": "아이디 또는 이메일",
    "password": "비밀번호",
    "login": "로그인",
    "login-button": "로그인",
    "go-to-signup": "회원가입"
  }
}
</i18n>

<script>
import ChevronLeftIcon from "icons/chevron-left";
import { mapGetters } from 'vuex'
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  data() {
    return {
      username: '',
      password: '',
      error: false,
      loading: false,
    };
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
    ])
  },
  methods: {
    login() {
      this.$data.loading = true;
      this.$data.error = false;
      const data = new FormData();
      data.set('username', this.$data.username);
      data.set('password', this.$data.password);
      data.set('grant_type', 'password');
      data.set('client_id', 'webapp');
      const requestOptions = {config: { headers: {'Content-Type': 'multipart/form-data' }}};
      this.$store.dispatch('login', { user: data, requestOptions }).then(() => {
        let dest = 'feed';
        if (this.$router.authRequiredRoute) {
          dest = this.$router.authRequiredRoute.path;
          this.$router.authRequiredRoute = null;
        }
        this.$router.push(dest);
      }).catch(error => {
        if (error.response) {
          this.$data.error = error.response.data.error_description;
        } else {
          this.$data.error = ''+error;
        }
        this.$data.loading = false;
      });
    },
    gotoSignup() {
      this.$router.push('signup');
    }
  },
  components: {
    ChevronLeftIcon,
  },
};
</script>

<style scoped>
.sub-login-text {
  text-align: center;
  text-shadow: 0 1px #fff;
  color: #386b8d;
  cursor: pointer;
  letter-spacing: 1px;
}
</style>

