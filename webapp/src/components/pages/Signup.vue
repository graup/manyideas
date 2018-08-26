<template>
  <div class="viewport hello has-header">
    <header>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
      <div class="view-title">{{$t('sign-up')}}</div>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
    </header>

    <main class="content">

      <div class="form-wrapper">

        <form action="" class="form">
          <div class="form-group">
            <input id="username" class="form-input" type="text" v-model="username" required autocorrect="off" autocapitalize="off" />
            <label class="form-label" for="username">{{$t('username')}}</label>
            <div class="error" v-if="errors.username">{{errors.username.join(' ')}}</div>
            <div class="help">{{$t('username-help')}}</div>
          </div>
          <div class="form-group">
            <input id="email" class="form-input" type="email" v-model="email" required />
            <label class="form-label" for="email">{{$t('email')}}</label>
            <div class="error" v-if="errors.email">{{errors.email.join(' ')}}</div>
            <div class="help">{{$t('email-help')}}</div>
          </div>
          <div class="form-group">
            <input id="password" class="form-input" type="password" v-model="password" required />
            <label class="form-label" for="password">{{$t('password')}}</label>
            <div class="error" v-if="errors.password">{{errors.password.join(' ')}}</div>
            <div class="help">{{$t('password-help')}}</div>
          </div>
          <div class="form-group">
            <input id="password2" class="form-input" type="password" v-model="password2" required />
            <label class="form-label" for="password2">{{$t('repeat-password')}}</label>
            <div class="error" v-if="errors.password2">{{errors.password2.join(' ')}}</div>
          </div>
          <div class="form-group button-group vertical spaced" style="max-width: 200px;">
            <my-button :text="$t('sign-up-button')" primary={true} v-on:click.native.capture="signup" v-bind:loading="loading" />
          </div>
        </form>
      </div>
    </main>
    <footer></footer>
  </div>
</template>

<i18n>
{
  "en": {
    "sign-up": "Sign up",
    "username": "Username",
    "username-help": "Will appear next to your ideas and comments.",
    "email": "Email",
    "email-help": "Will be kept private.",
    "password": "Password",
    "password-help": "At least 8 characters, not entirely numeric.",
    "repeat-password": "Repeat password",
    "sign-up-button": "Sign up",
    "passwords-dont-match": "Passwords do not match."
  },
  "ko": {
    "sign-up": "회원 가입",
    "username": "아이디",
    "username-help": "아이디어와 댓글 옆에 나타납니다.",
    "email": "이메일",
    "email-help": "비공개로 유지됩니다.",
    "password": "비밀번호",
    "password-help": "최소 8자, 숫자가 아닌 문자를 하나 이상 포함해 주시기 바랍니다.",
    "repeat-password": "비밀번호 확인",
    "sign-up-button": "가입하기",
    "passwords-dont-match": "비밀번호가 일치하지 않습니다."
  }
}
</i18n>

<script>
import ChevronLeftIcon from "icons/chevron-left";
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      errors: {},
      loading: false,
    };
  },
  methods: {
    signup() {
      if (this.$data.password !== this.$data.password2) {
        this.$data.errors = {password2: [this.$t('passwords-dont-match')]};
        return;
      }
      this.$data.loading = true;

      const data = new FormData();
      data.set('username', this.$data.username);
      data.set('password', this.$data.password);
      data.set('email', this.$data.email);
      this.$store.dispatch('signup', { user: data, requestOptions: {} }).then(() => {
        this.$router.push('signup-test');
      }).catch(error => {
        this.$data.errors = error.response.data;
        this.$data.loading = false;
      });
    },
  },
  components: {
    ChevronLeftIcon,
  },
};
</script>

<style scoped>
</style>
