<template>
  <div>
    <Sheet ref="sheet">
      <div class="button-list">
        <my-button v-on:click.native="flagComment()"><FlagIcon class="button-icon" /> {{$t('report-comment')}}</my-button>
        <my-button v-on:click.native="deleteComment()" v-if="isAuthor"><DeleteIcon class="button-icon" /> {{$t('delete-comment')}}</my-button>
      </div>
    </Sheet>

    <div class="comment" v-bind:class={isAuthor}>
      <div class="content" v-on:click="showSheet">
        {{item.text}}
        <span class="date">{{item.created_date | moment("from", "now")}}</span>
      </div>
      <div class="author">{{item.author.username}}</div>
    </div>
  </div>
</template>

<i18n>
{
  "en": {
    "comment-deleted": "The comment was successfully deleted.",
    "comment-reported": "Thank you for reporting this content.",
    "report-comment": "Report inappropriate content",
    "delete-comment": "Delete comment",
    "report-reason": "Why is this post inappropriate?",
    "delete-confirm": "Are you sure you want to delete this comment?"
  },
  "ko": {
    "comment-deleted": "댓글이 성공적으로 삭제되었습니다.",
    "comment-reported": "신고해주셔서 감사합니다.",
    "report-comment": "부적절한 콘텐츠 신고하기",
    "delete-comment": "댓글 삭제하기",
    "report-reason": "이 댓글이 부적절한 이유는 무엇입니까?",
    "delete-confirm": "이 댓글을 삭제 하시겠습니까?"
  }
}
</i18n>

<script>
import {navigationMixins} from "@/mixins";
import Sheet from "@/components/elements/Sheet";
import FlagIcon from "icons/flag";
import DeleteIcon from "icons/delete";

export default {
  mixins: [navigationMixins],
  props: ['item', ],
  computed: {
    isAuthor() {
      return this.user.username == this.$props.item.author.username;
    }
  },
  methods: {
    showSheet() {
      this.$refs.sheet.show();
    },
    flagComment() {
      let reason = prompt(this.$t('report-reason'));
      if (!reason) return;
      this.$store.dispatch('flagComment', { comment: this.$props.item, reason }).then(() => {
        alert(this.$t('comment-reported'));
        this.$refs.sheet.hide();
      });
    },
    deleteComment() {
      let check = confirm(this.$t('delete-confirm'));
      if (!check) return;
      this.$store.dispatch('deleteComment', { comment: this.$props.item }).then(() => {
        this.$refs.sheet.hide();
        this.gotoRoute({name: 'feed'});
        this.$toasted.show(this.$t('comment-deleted'), {duration: 3000});
      }).catch(error => {
        alert('Failed. ' + error.response.data.detail);
      })
    },
  },
  components: {
    Sheet,
    FlagIcon,
    DeleteIcon,
  },
};
</script>

<style lang="scss">
.comment {
  margin: 1rem 0;

  .author {
    font-size: .8em;
    color: #888;
    margin: 0 0 0 1.25rem;
    font-weight: 500;
  }
  .content {
    font-size: .9em;
    line-height: 1.5;
    background-color: #fff;
    border-radius: 10px;
    padding: .75rem;
    margin: .5rem;
    margin-bottom: 12px;

    position: relative;
    cursor: pointer;

    &:before {
      content: "";
      position: absolute;
      left: 16px;
      bottom: 0;
      border: 8px solid transparent;
      border-top-color: #fff;
      transform: translateY(16px);
    }
  }

  .date {
    display: block;
    font-size: .9em;
    text-align: right;
    color: #666;
  }
  &.isAuthor .author {
    color: #039e63;
  }
}
</style>
