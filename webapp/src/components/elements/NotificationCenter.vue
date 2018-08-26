<template>
  <div id="notifications" :data-last-check="lastChecked"><!-- invisible--></div>
</template>

<script>
import {navigationMixins} from "@/mixins";
import { apiGet } from '../../utils/api';

export default {
  mixins: [navigationMixins],
  data () {
    return {
      lastChecked: (new Date()).getTime(),
    }
  },
  created () {
    this.checkNotifications();
  },
  computed: {

  },
  methods: {
    checkNotifications() {
      if (!this.isAuthenticated) return;
      console.log('checking for updates...');
      apiGet('users/me/updates/', {params: {since: this.lastChecked}}).then((resp) => {
        if (resp.data.length > 0) {
          // mark the comments as dirty
          resp.data.forEach(element => {
            this.$store.commit('markCommentsDirty', {slug: element.slug});
          });
          this.$toasted.show(this.$t('new-comments'), {
            action: {
              text: this.$t('go-to-issue'),
              onClick: (e, toastObject) => {
                toastObject.goAway(0);
                this.$router.push({ name: 'issue-detail', params: { slug: resp.data[0].slug }});
              }
            },
          });
        }
        this.lastChecked = (new Date()).getTime();
        setTimeout(() => {
          this.checkNotifications();
        }, 10000);
      }).catch((error) => {
        // Back off a little bit, but try again later
        console.error(error);
        setTimeout(() => {
          this.checkNotifications();
        }, 60000);
      });
    },
  },
  components: {
  },
};
</script>

<i18n>
{
  "en": {
    "new-comments": "There are new comments on your idea.",
    "go-to-issue": "Go to idea"
  },
  "ko": {
    "new-comments": "당신의 아이디어에 대한 새로운 댓글이 있습니다.",
    "go-to-issue": "아이디어로 이동하기"
  }
}
</i18n>

<style scoped>

</style>
