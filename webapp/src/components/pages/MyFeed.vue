<template>
  <div class="viewport feed has-header" v-touch:swipe.right="showMenu" v-touch:swipe.left="hideMenu">
    <header>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
      <div class="view-title">{{$t('my-ideas')}}</div>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
    </header>
    <main class="content">
      <vue-pull-refresh :on-refresh="onRefresh" :config="{startLabel: $t('pull-to-reload'), readyLabel: $t('release-to-reload'), loadingLabel: $t('loading'), pullDownHeight: 60}">

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

        <div class="empty-state" v-if="!loading && !issues.length">
          <span v-html="$t('empty-state')" v-if="treatmentName=='baseline'"/>
          <span v-html="$t('empty-state-autonomy')" v-if="treatmentName=='autonomy'" />
          <span v-html="$t('empty-state-control')" v-if="treatmentName=='control'" />
        </div>

      </vue-pull-refresh>
    </main>
    <footer>
      <FeedCallToAction treatment="user.active_treatment.name=='orientation_autonomy'" />
    </footer>
  </div>
</template>

<i18n src='../../locales.json'></i18n>
<i18n>
{
  "en": {
    "my-ideas": "My Ideas",
    "loading-error": "An error occurred while loading.<br>Try to reload this page.",
    "empty-state": "Nothing yet. <br>Post your first idea now!",
    "empty-state-autonomy": "Nothing yet. <br>Share your ideas with the community now!<br>Everyone’s voice counts.",
    "empty-state-control": "Nothing yet. <br>Please share your ideas with the community!"
  },
  "ko": {
    "my-ideas": "내 아이디어",
    "loading-error": "로딩 중 오류가 발생했습니다.<br>페이지를 새로고침 해 보십시오.",
    "empty-state": "아직 없습니다. <br> 지금 바로 첫 번째 아이디어를 게시하세요!",
    "empty-state-autonomy": "아직 없습니다. <br>바로 지금 여러분의 아이디어를 교내 구성원들과 공유하세요!<br>모든 사람의 의견 중요합니다.",
    "empty-state-control": "아직 없습니다. <br>2바로 지금 여러분의 아이디어를 교내 구성원들과 공유하세요!"
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
        this.issues = issues.filter(item => item.author.username == this.user.username);
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
        this.issues = issues.filter(item => item.author.username == this.user.username);
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
