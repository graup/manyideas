<template>
  <div class="viewport feed has-header">
    <header>
      <div class="icon-button" v-on:click="gotoRoute('/feed')"><ChevronLeftIcon /></div>
      <div class="view-title">{{$t('issue-details')}}</div>
      <div class="icon-button" v-on:click="gotoRoute('/feed')"><ChevronLeftIcon /></div>
    </header>
    <main class="content">

      <vue-pull-refresh :on-refresh="onRefresh" :config="{startLabel: $t('pull-to-reload'), readyLabel: $t('release-to-reload'), loadingLabel: $t('loading'), pullDownHeight: 60}">

        <transition name="fade-up">
          <div class="big-loading" v-if="loading">
            <Spinner />
            {{$t('loading')}}
          </div>
        </transition>

        <div v-if="issue">
          <div class="tutorial-message" v-if="issue.author.username!=user.username && treatmentName">
            <span v-html="$t('tutorial-issue-details')" v-if="treatmentName=='baseline'"/>
            <span v-html="$t('tutorial-issue-details-autonomy')" v-if="treatmentName=='autonomy'" />
            <span v-html="$t('tutorial-issue-details-control')" v-if="treatmentName=='control'" />
          </div>

          <div class="tutorial-message" v-if="issue.author.username==user.username && !comments.length && issue.like_count<=1">
            {{$t('tutorial-your-idea')}}
          </div>
          
          <Issue v-bind:item="issue" expanded="true" />
        
          <div class="empty-state" v-if="!comments.length" v-html="$t('no-comments')"></div>

          <CommentList v-bind:items="comments" />

        </div>

      </vue-pull-refresh>

    </main>
    <footer>
      <div class="call-to-action">
        <div v-if="!commentMode">
          <p v-if="treatmentName">
            <span v-html="$t('comment-cta-autonomy')" v-if="treatmentName=='autonomy'" />
            <span v-html="$t('comment-cta-control')" v-if="treatmentName=='control'" />
          </p>
          <my-button :text="$t('comment-cta')" primary={true} v-on:click.native="toggleCommentMode()" />
        </div>
        <div v-if="commentMode" class="comment-form">
          <textarea name="text" class="comment-text" ref="commentText" autofocus placeholder="Write a comment..." v-model="commentText"></textarea>
          <my-button v-on:click.native="submitComment()" primary={true} icon={true} :loading="sendingComment"><SendIcon /></my-button>
        </div>
      </div>
    </footer>
  </div>
</template>

<i18n src='../../locales.json'></i18n>
<i18n>
{
  "en": {
    "issue-details": "Idea Details",
    "tutorial-issue-details": "Here you can see details about the idea and comments that other people left. If you agree with this issue, how about showing your support by tapping the heart? If you have another opinion, try writing a short comment.",
    "tutorial-issue-details-autonomy": "Here you can see details about the idea. <strong>Discussing ideas and showing your support is important for our community.</strong> If you agree with this issue, how about showing your support by tapping the heart? If you have another opinion, try writing a short comment.",
    "tutorial-issue-details-control": "Here you can see details about the idea. If you agree with this issue, how about showing your support by tapping the heart? If you have another opinion, try writing a short comment.",
    "tutorial-your-idea": "This is your idea! Good job. Let's wait until other members give their opinion.",
    "no-comments": "No comments yet. <br>You can be the first!",
    "comment-cta-autonomy": "Let's share our diverse viewpoints!",
    "comment-cta-control": "Be active, get a chance to win!",
    "comment-cta": "Leave a comment"
  },
  "ko": {
    "issue-details": "아이디어 세부 정보",
    "tutorial-issue-details": "여기에서 다른 사람들이 남긴 아이디어와 의견에 대한 세부 정보를 볼 수 있습니다. 이 문제에 동의하신다면 하트를 눌러 공감을 표시해 보시면 어떨까요? 다른 의견이 있으면 간단한 설명을 적어주세요.",
    "tutorial-issue-details-autonomy": "여기에서 다른 사람들이 남긴 아이디어와 의견에 대한 세부 정보를 볼 수 있습니다. <strong>아이디어를 토론하고 좋은 아이디어를 응원을 하면 우리 교내 커뮤니티에 큰 힘이 됩니다.</strong> 이 문제에 동의하신다면 하트를 눌러 공감을 표시해 보시면 어떨까요? 다른 의견이 있으면 간단한 설명을 적어주세요.",
    "tutorial-issue-details-control": "여기에서 다른 사람들이 남긴 아이디어와 의견에 대한 세부 정보를 볼 수 있습니다. 이 문제에 동의하신다면 하트를 눌러 공감을 표시해 보시면 어떨까요? 다른 의견이 있으면 간단한 설명을 적어주세요.",
    "tutorial-your-idea": "당신의 아이디어입니다! 훌륭해요. 다른 사람들이 의견을 남길 때까지 기다려 보아요.",
    "no-comments": "아직 댓글이 없습니다. <br> 첫번째 댓글을 남겨보세요.",
    "comment-cta-autonomy": "우리 각자의 다양한 관점을 공유해 보아요!",
    "comment-cta-control": "참여하고 경품 기회를 얻으세요!",
    "comment-cta": "댓글 남기기"
  }
}
</i18n>

<script>
import Spinner from '@/components/elements/Spinner';
import ChevronLeftIcon from "icons/chevron-left";
import SubmenuIcon from "icons/dots-horizontal";
import SendIcon from "icons/send";
import {navigationMixins} from "@/mixins";
import Issue from "@/components/elements/Issue";
import CommentList from "@/components/elements/CommentList";
import autosize from 'autosize';
import VuePullRefresh from 'vue-pull-refresh';


export default {
  mixins: [navigationMixins],
  props: ['slug', 'item'],
  data () {
    return {
      loading: false,
      issue: null,
      comments: [],
      error: null,
      commentMode: false,
      commentText: '',
      sendingComment: false,
    }
  },
  created () {
    this.fetchData();
  },
  watch: {
    '$route': 'fetchData'
  },
  components: {
    ChevronLeftIcon,
    Issue,
    Spinner,
    CommentList,
    SendIcon,
    SubmenuIcon,
    VuePullRefresh,
  },
  methods: {

    onRefresh() {
      this.error = null;
      let slug = this.issue.slug || this.$props.slug;
      return Promise.all([
        this.$store.dispatch('fetchIssue', { slug }).then((issue) => {
          this.issue = issue;
        }),
        this.$store.dispatch('fetchComments', { slug }).then((comments) => {
          this.comments = comments;
        }),
      ]).catch((error) => {
        this.error = error;
      });
    },
    fetchData () {
      if (this.$props.item) {
        // issue was passed in through router, no need to load again
        this.issue = this.$props.item;
      } else {
        this.error = this.issue = null;
        this.loading = true;
        this.$store.dispatch('getIssue', {slug: this.$props.slug}).then((issue) => {
          this.issue = issue;
          this.loading = false;
        });
      }

      this.$store.dispatch('getComments', {slug: this.$props.slug}).then((comments) => {
        this.comments = comments;
        this.loading = false;
      });
    },
    submitComment() {
      this.sendingComment = true;
      let comment = { text: this.commentText, issue: this.issue.id };
      let started = (new Date()).getTime();
      this.$store.dispatch('createComment', {slug: this.issue.slug, comment}).then((comment) => {
        let wait = Math.max(1, 1000 - ((new Date()).getTime() - started)); // wait at least 1 s
        setTimeout(() => {
          this.commentText = '';
          this.sendingComment = false;
          this.commentMode = false;
          this.comments.unshift(comment);
          this.issue.comment_count += 1;
        }, wait);
      });
    },
    toggleCommentMode() {
      if (!this.$store.state.user.isAuthenticated) {
        this.$router.authRequiredRoute = this.$router.currentRoute;
        this.$router.push('/login');
        return;
      }
      
      this.commentMode = !this.commentMode;
      if (this.commentMode) {
        this.$nextTick(() => {
          autosize(this.$refs.commentText);
          this.$refs.commentText.focus()
        });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.comment-form {
  display: flex;
  align-items: center;

  .comment-text {
    flex: 1;
    
    padding: 10px;
    margin-right: 1em;
    border: none;
    background-color: #fff;
  }

}
</style>
