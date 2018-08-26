<template>
  <div class="issue" v-bind:class="{expanded}">

    <Sheet ref="sheet">
      <div class="button-list">
        <my-button v-on:click.native="flagIssue()"><FlagIcon class="button-icon" /> {{$t('report-issue')}}</my-button>
        <my-button v-on:click.native="deleteIssue()" v-if="isAuthor"><DeleteIcon class="button-icon" /> {{$t('delete-issue')}}</my-button>
      </div>
    </Sheet>

    <div class="issue-header" v-if="expanded">
      <span class="actions">
        <span v-on:click="showSheet"><SubmenuIcon fillColor="#888" /></span>
      </span>
      
      <span class="icon-with-text">
        <span v-bind:class="{isAuthor}"><PersonIcon /> {{item.author.username}}</span>
        <span class="date">{{item.created_date | moment("from", "now")}}</span>
      </span>
    </div>
    <h2 class="issue-title" v-on:click="gotoDetails">{{item.title}}</h2>
    <div class="issue-detail" v-if="expanded">
      <p class="issue-text">{{item.text}}</p>
    </div>
    <div class="issue-location" v-if="item.location && expanded">
      <LocationIcon /> {{item.location.name}}
      <div class="map" :style="'background-image: url(http://staticmap.openstreetmap.de/staticmap.php?center='+item.location.lat+'%2C'+item.location.lon+'&zoom=16&size=400x200&maptype=mapnik&markers='+item.location.lat+'%2C'+item.location.lon+'%2Col-marker-blue)'" />
    </div>
    <div class="issue-stats">
      <span class="icon-with-text" v-on:click.capture.stop="toggleLike">
        <span class="like-container" v-bind:class="{liked: item.user_liked}">
          <HeartIcon /> 
          <HeartFilledIcon fillColor="red" /> 
        </span> {{item.like_count}}
      </span>
      <span class="icon-with-text" v-on:click.capture.stop="gotoDetails">
        <span class="comment-container" v-bind:class="{commented: item.user_commented}">
          <CommentIcon />
          <CommentFilledIcon fillColor="#c521ff" />
        </span>
        {{item.comment_count}}
      </span>     
      <span class="icon-with-text">
        <span class="date" v-if="!expanded">{{item.created_date | moment("from", "now")}}</span>
        <span v-bind:class="{isAuthor}" v-if="!expanded"><PersonIcon /> {{item.author.username}}</span>
      </span>
    </div>
  </div>
</template>

<i18n>
{
  "en": {
    "issue-deleted": "The idea was successfully deleted.",
    "issue-reported": "Thank you for reporting this content.",
    "report-issue": "Report inappropriate content",
    "delete-issue": "Delete idea",
    "report-reason": "Why is this post inappropriate?",
    "delete-confirm": "Are you sure you want to delete this idea?"
  },
  "ko": {
    "issue-deleted": "아이디어가 성공적으로 삭제되었습니다.",
    "issue-reported": "신고해주셔서 감사합니다.",
    "report-issue": "부적절한 콘텐츠 신고하기",
    "delete-issue": "아이디어 삭제하기",
    "report-reason": "이 게시물이 부적절한 이유는 무엇입니까?",
    "delete-confirm": "이 아이디어를 삭제 하시겠습니까?"
  }
}
</i18n>

<script>
import HeartIcon from 'icons/heart-outline';
import HeartFilledIcon from 'icons/heart';
import CommentIcon from 'icons/comment-outline';
import CommentFilledIcon from 'icons/comment';
import LocationIcon from "icons/map-marker";
import PersonIcon from 'icons/account-circle';
import SubmenuIcon from "icons/dots-horizontal";
import FlagIcon from "icons/flag";
import DeleteIcon from "icons/delete";
import Sheet from "@/components/elements/Sheet";


import {completeTutorial} from "@/utils/tutorials";
import {navigationMixins} from "@/mixins";
import {getBBox} from "@/utils/geo";

export default {
  mixins: [navigationMixins],
  props: ['item', 'expanded'],
  data () {
    return {
      liked: false,
    }
  },
  computed: {
    location_bbox() {
      return getBBox(this.$props.item.location.lat, this.$props.item.location.lon, 200);
    },
    isAuthor() {
      return this.user && this.user.username == this.$props.item.author.username;
    }
  },
  methods: {
    gotoDetails() {
      completeTutorial(this.$localStorage, 'feed');
      let slug = this.$props.item.slug;
      this.$router.push({ name: 'issue-detail', params: { slug: slug, item: this.$props.item }});
    },
    toggleLike() {
      console.log("like");
      if (this.$props.item.user_liked) {
        this.$props.item.like_count -= 1;
      } else {
        this.$props.item.like_count += 1;
      }
      this.$props.item.user_liked = !this.$props.item.user_liked;
      this.$store.dispatch('likeIssue', { issue: this.$props.item }).then(
        (issue) => {
          this.$props.item = issue;
        }
      );
    },
    showSheet() {
      this.$refs.sheet.show();
    },
    flagIssue() {
      let reason = prompt(this.$t('report-reason'));
      if (!reason) return;
      this.$store.dispatch('flagIssue', { issue: this.$props.item, reason }).then(() => {
        alert(this.$t('issue-reported'));
        this.$refs.sheet.hide();
      });
    },
    deleteIssue() {
      let check = confirm(this.$t('delete-confirm'));
      if (!check) return;
      this.$store.dispatch('deleteIssue', { issue: this.$props.item }).then(() => {
        this.$refs.sheet.hide();
        this.gotoRoute({name: 'my-posts'});
        this.$toasted.show(this.$t('issue-deleted'), {duration: 3000});
      }).catch(error => {
        alert('Failed. ' + error.response.data.detail);
      })
    },
  },
  components: {
    HeartIcon,
    HeartFilledIcon,
    CommentIcon,
    CommentFilledIcon,
    PersonIcon,
    LocationIcon,
    SubmenuIcon,
    Sheet,
    FlagIcon,
    DeleteIcon,
  },
};
</script>

<style lang="scss">
.issue {
  box-sizing: border-box;
  margin: .75rem;   
  background-color: #ffffff;
  border-radius: 2px;
  box-shadow: 0 2px 5px rgba(50,50,93,.15);
}
.issue-title {
  font-size: 1em;
  font-weight: normal;
  margin: 0;
  line-height: 1.3;
  cursor: pointer;
}
.issue-title, .issue-text, .issue-stats {
  padding: .75rem;
}
.issue-text {
  border-top: 1px solid #eee;
  font-size: 90%;
  margin: 0;
}
.issue-stats {
  border-top: 1px solid #eee;
  display: flex;

  :last-child {
    margin-left: auto;
  }
}
.issue-header {
  padding: .75em .75em 0;

  .actions {
    float: right;
  }
}
.issue-location {
  border-top: 1px solid #eee;
  padding: .75em;
  line-height: 1;
  font-size: .95em;

  .map {
    margin-top: .5em;
    width: 100%;
    height: 150px;
    background-position: center center;
  }

  .material-design-icon {
    margin-right: -3px;
    svg {
      width: 16px;
      height: 16px;
      vertical-align: middle;
      transform: translateY(-2px);
      fill: #386b8d;
    }
  }
}

.icon-with-text {
  font-weight: bold;
  margin-right: 1rem;
  font-size: 85%;
  cursor: pointer;

  &:last-child {
    margin-right: 0;
  }

  .material-design-icon {
    svg {
      width: 16px;
      height: 16px;
      vertical-align: text-top;
      transform: translateY(1px);
    }
  }

  .isAuthor svg {
    fill: #039e63;
  }
  .isAuthor {
    color: #039e63;
  }
  .date {
    color: #777;
    font-weight: 300;
  }
}

.like-container, .comment-container {
  position: relative;
  width: 16px;
  display: inline-block;
  vertical-align: top;

  .material-design-icon {
    position: absolute;
    left: 0;
    transition: all .3s cubic-bezier(0.14, 0.83, 0.37, 1.35);
  }
  .heart-icon, .comment-icon {
    transform: scale(0) translateY(0px);
    transform-origin: center center;
  }

  &.liked, &.commented {
    .heart-outline-icon, .comment-outline-icon {
      opacity: 0;
    }
    .heart-icon, .comment-icon {
      transform: scale(1.2) translateY(-1px);
    }
  }
}
</style>
