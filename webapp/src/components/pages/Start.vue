<template>
  <div class="viewport hello">
    <header></header>
    <main class="content">
      <app-logo instance-name="KAIST" />

      <p class="intro">
        {{ $t('hello') }}
      </p>

      <div class="button-group vertical spaced" style="max-width: 200px;">
        <my-button :text="$t('signup')" link-to="signup-consent" primary={true} />
        <my-button :text="$t('login')" link-to="login" />
      </div>

      <div v-if="!touchDevice" class="message warning">
        <p v-html="$t('mobile-browser-advice')"></p>
        <img :src='codeUrl' alt=''>
        <br>
        https://manyideas.org
      </div>
    </main>
    <footer></footer>
  </div>
</template>

<i18n>
{
  "en": {
    "hello": "Join us in collecting important issues and ideas for the future of KAIST. We need everyone’s contribution!",
    "signup": "Sign up",
    "login": "Log in",
    "mobile-browser-advice": "This application is designed for use on mobile devices.<br>Please visit this web site on a mobile device."
  },
  "ko": {
    "hello": "KAIST의 미래를 위한 중요한 이슈와 아이디어를 모으는 데에 참여하세요. 우리 모두의 참여가 필요합니다!",
    "signup": "회원 가입",
    "login": "로그인",
    "mobile-browser-advice": "이 웹사이트는 모바일에서 사용하도록 설계되었습니다. <br> 모바일 기기에서 웹사이트를 방문하십시오."
  }
}
</i18n>

<script>
import {localeMixin} from "@/mixins";

export default {
  mixins: [localeMixin],
  name: 'Start',
  computed: {
    codeUrl() {
      const currentUrl = window.location.href;
      return `https://chart.googleapis.com/chart?cht=qr&chl=${encodeURIComponent(currentUrl)}&chs=180x180&choe=UTF-8&chld=L|2`;
    }
  },
  data() {
    return {
      touchDevice: !!('ontouchstart' in window),
    };
  },
};
</script>

<style scoped>
.content {
  text-align: center;
}
.intro {
  padding: 0 2em;
  margin-bottom: 3rem;
  font-size: 1.1em;
}
.message {
  margin: 3rem 1rem 0;
  border: 1px solid orange;
  padding: 1rem;
  background-color: #fff;
  border-radius: 5px;
}
</style>
