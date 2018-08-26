<template>
  <div class="side-menu" v-bind:class="{opened: isMenuOpened}">
    <app-logo instance-name="KAIST" class="small inverted" />

    <div class="authentication-status" v-if="isAuthenticated">
      <PersonIcon fillColor="#fff" />
      {{user.username}}
    </div>

    <ul class="menu-items" v-if="isAuthenticated">
      <li><a class="menu-item" v-on:click="gotoRoute('feed')">{{$t('recent-ideas')}}</a></li>
      <li><a class="menu-item" v-on:click="gotoRoute('my-posts')">{{$t('my-ideas')}}</a></li>
      <li><a class="menu-item" v-on:click="gotoRoute('my-reactions')">{{$t('my-reactions')}}</a></li>
      <li><a class="menu-item" v-on:click="gotoRoute('faq')">{{$t('faq')}}</a></li>
      <li><a class="menu-item" v-on:click="logout">{{$t('logout')}}</a></li>
    </ul>
    <ul class="menu-items" v-if="!isAuthenticated">
      <li><a class="menu-item" v-on:click="$router.push('login')">{{$t('login')}}</a></li>
      <li><a class="menu-item" v-on:click="$router.push('signup-consent')">{{$t('signup')}}</a></li>
    </ul>
  </div>
</template>

<i18n>
{
  "en": {
    "recent-ideas": "Recent Ideas",
    "my-ideas": "My Ideas",
    "my-reactions": "My Reactions",
    "faq": "FAQ",
    "logout": "Log out",
    "login": "Log in",
    "signup": "Sign up"
  },
  "ko": {
    "recent-ideas": "최근 아이디어",
    "my-ideas": "내 아이디어",
    "my-reactions": "내 반응",
    "faq": "FAQ",
    "logout": "로그아웃",
    "login": "로그인",
    "signup": "회원가입"
  }
}
</i18n>

<script>
import {navigationMixins} from "@/mixins";
import PersonIcon from 'icons/account-circle';


export default {
  mixins: [navigationMixins],
  name: 'side-menu',
  props: ['instanceName'],
  created () {
    this.getUser();
  },
  watch: {
    'isAuthenticated': 'getUser'
  },
  methods: {
    getUser() {
      this.$store.dispatch('getCurrentUser');
    },
    gotoRoute(path) {
      this.$store.commit('setMenuOpened', false);
      this.$router.push(path);
    },
  },
  components: {
    PersonIcon,
  },
};
</script>

<style lang="scss">
.side-menu {
  position: fixed;
  z-index: 100;
  top: 0;
  left: 0;
  min-height: 100vh;
  width: 200px;
  background-color: #333;
  color: #fff;

  user-select: none;

  text-align: center;

  transition: all .5s cubic-bezier(.55,0,.1,1);
  transform: translateX(-100%);

  &.opened {
    transform: translateX(0%);
  }

}

.menu-items {
  list-style: none;
  margin: 0;
  padding: 0 1rem;

  li {
    border-bottom: 1px solid #666;

    &:last-child {
      border-bottom: none;
    }
  }
}
.menu-item {
  display: block;
  line-height: 2.5;
  cursor: pointer;
}

.token {
  width: 100%;
  text-overflow: ellipsis;
  overflow: hidden;
}
.authentication-status {
  font-size: 90%;
  margin-bottom: 1.5rem;

  .material-design-icon {
      display: block;
  }


}
</style>
