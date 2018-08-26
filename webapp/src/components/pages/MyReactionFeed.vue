<template>
  <div class="viewport feed has-header" v-touch:swipe.right="showMenu" v-touch:swipe.left="hideMenu">
    <header>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
      <div class="view-title">{{$t('title')}}</div>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
    </header>
    <main class="content">
      <vue-pull-refresh :on-refresh="onRefresh" :config="{startLabel: $t('pull-to-reload'), readyLabel: $t('release-to-reload'), loadingLabel: $t('loading'), pullDownHeight: 60}">

        <div class="view-help" v-html="$t('view-explanation')" />

        <transition name="fade-up">
          <div class="big-loading" v-if="loading">
            <Spinner />
            {{$t('loading')}}
          </div>
          <div class="big-loading loading-error" v-if="error">
            <ErrorIcon /><br>
            <span v-html="$t('loading-error')"></span>
          </div>
        </transition>

        <IssueList v-bind:items="issues" />

        <div class="empty-state" v-if="!loading && !issues.length" v-html="$t('empty-state')" />

      </vue-pull-refresh>
    </main>
    <footer>
    </footer>
  </div>
</template>

<i18n src='../../locales.json'></i18n>
<i18n>
{
  "en": {
    "title": "My Reactions",
    "loading-error": "An error occurred while loading.<br>Try to reload this page.",
    "empty-state": "Nothing yet. <br>Try commenting or liking an idea!",
    "view-explanation": "These are all ideas that you have liked or commented on."
  },
  "ko": {
    "title": "내가 반응한 아이디어",
    "loading-error": "로딩 중 오류가 발생했습니다.<br>페이지를 새로고침 해 보십시오.",
    "empty-state": "아직 없습니다. <br> 댓글 남기거나 하트를 눌러 보세요!",
    "view-explanation": "회원님이 댓글을 남기거나 하트를 누른 아이디어입니다."
  }
}
</i18n>

<script>
import MenuIcon from "icons/menu";
import ErrorIcon from "icons/cloud-off-outline";
import Spinner from '@/components/elements/Spinner';
import VuePullRefresh from 'vue-pull-refresh';
import IssueList from "@/components/elements/IssueList";
import FeedCallToAction from "@/components/elements/FeedCallToAction";
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  data () {
    return {
      loading: false,
      issues: null,
      error: null
    }
  },
  created () {
    this.fetchData();
  },
  watch: {
    '$route': 'fetchData'
  },
  methods: {
    fetchData () {
      this.error = null;
      this.loading = true;
      
      return this.$store.dispatch('getIssues').then((issues) => {
        this.issues = issues.filter(item => item.user_liked || item.user_commented);
        this.loading = false;
        this.error = null;
      }).catch(error => {
        this.error = true;
        this.loading = false;
        console.error(error);
      })
    },
    onRefresh() {
      this.error = null;
      return this.$store.dispatch('fetchIssues').then((issues) => {
        this.issues = issues.filter(item => item.user_liked || item.user_commented);
      });
    },
  },
  components: {
    MenuIcon,
    ErrorIcon,
    IssueList,
    VuePullRefresh,
    Spinner,
    FeedCallToAction,
  },
};
</script>

<style scoped>

</style>
