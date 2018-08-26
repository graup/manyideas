<template>
  <div class="viewport feed has-header" v-touch:swipe.right="showMenu" v-touch:swipe.left="hideMenu">
    <header>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
      <div class="view-title">{{$t('recent-ideas')}}</div>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
    </header>
    <main class="content">
      <vue-pull-refresh :on-refresh="onRefresh" :config="{startLabel: $t('pull-to-reload'), readyLabel: $t('release-to-reload'), loadingLabel: $t('loading'), pullDownHeight: 60}">

        <div class="tutorial-message" v-if="tutorial_feed && treatmentName">
          <span v-html="$t('tutorial-welcome')" v-if="treatmentName=='baseline'"/>
          <span v-html="$t('tutorial-welcome-autonomy')" v-if="treatmentName=='autonomy'" />
          <span v-html="$t('tutorial-welcome-control')" v-if="treatmentName=='control'" />
        </div>

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

        <IssueList v-bind:items="issues" v-on::click.native="completeTutorial('feed')" />

      </vue-pull-refresh>
    </main>
    <footer>
      <FeedCallToAction />
    </footer>
  </div>
</template>

<i18n src='../../locales.json'></i18n>
<i18n>
{
  "en": {
    "recent-ideas": "Recent Ideas",
    "loading-error": "An error occurred while loading.<br>Try to reload this page.",
    "tutorial-welcome": "<strong>Welcome to Many Ideas for KAIST!</strong><br>We're happy to have you here. On this page, you can see ideas by other members. Do you see anything you are interested in?<br>Try tapping on a post.",
    "tutorial-welcome-autonomy": "Welcome to Many Ideas for KAIST, <strong>where our combined voice can have a real impact!</strong> We're happy to have you here. On this page, you can see ideas by other members. Do you see anything you are interested in? Try tapping on a post.",
    "tutorial-welcome-control": "Welcome to Many Ideas for KAIST! We're happy to have you here. On this page, you can see ideas by other members. Do you see anything you are interested in? Try tapping on a post."
  },
  "ko": {
    "recent-ideas": "최근 제안된 아이디어",
    "loading-error": "로딩 중 오류가 발생했습니다.<br>이 페이지를 새로고침 해보십시오.",
    "tutorial-welcome": "<strong>KAIST를 위한 Many Ideas에 오신 것을 환영합니다!</strong> <br> 방문해주셔서 감사합니다.  이 페이지에서 다른 사용자가 올린 아이디어를 볼 수 있습니다. 관심있는 내용이 있나요? <br> 게시물을 클릭해보세요.",
    "tutorial-welcome-autonomy": "<strong>우리의 하나 된 목소리가 실질적인 변화를 만들어낼 수 있는 곳!</strong> KAIST를 위한 Many Ideas에 오신 것을 환영합니다 방문해주셔서 감사합니다. 이 페이지에서 다른 사용자가 올린 아이디어를 볼 수 있습니다. 관심있는 내용이 있나요? <br> 게시물을 클릭해보세요.",
    "tutorial-welcome-control": "KAIST를 위한 Many Ideas에 오신 것을 환영합니다! <br> 방문해주셔서 감사합니다.  이 페이지에서 다른 사용자가 올린 아이디어를 볼 수 있습니다. 관심있는 내용이 있나요? <br> 게시물을 클릭해보세요."
  }
}
</i18n>

<script>
import MenuIcon from "icons/menu";
import ErrorIcon from "icons/cloud-off-outline";
import Spinner from '@/components/elements/Spinner';
import VuePullRefresh from 'vue-pull-refresh';
import IssueList from "@/components/elements/IssueList";
import {navigationMixins} from "@/mixins";
import {hasCompletedTutorial, completeTutorial} from "@/utils/tutorials";
import FeedCallToAction from '@/components/elements/FeedCallToAction';

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
  computed: {
    tutorial_feed() {
      return ! hasCompletedTutorial(this.$localStorage, 'feed');
    },
  },
  methods: {
    completeTutorial(name) {
      completeTutorial(this.$localStorage, name);
    },
    fetchData () {
      this.error = null;
      this.loading = true;
      
      return this.$store.dispatch('getIssues').then((issues) => {
        this.issues = issues;
        this.loading = false;
        this.error = null;
      }).catch(error => {
        this.error = true;
        this.loading = false;
      })
    },
    onRefresh() {
      this.error = null;
      return this.$store.dispatch('fetchIssues').then((issues) => {
        this.issues = issues;
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
