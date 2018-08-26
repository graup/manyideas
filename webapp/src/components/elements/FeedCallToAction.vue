<template>
  <div class="call-to-action">
    <p v-if="treatmentName">
      <span v-html="$t('cta-lead-text')" v-if="treatmentName=='baseline'"/>
      <span v-html="$t('cta-lead-text-autonomy')" v-if="treatmentName=='autonomy'" />
      <span v-html="$t('cta-lead-text-control')" v-if="treatmentName=='control'" />
    </p>
    <my-button :text="$t('cta-button-text')" primary={true} :link-to="{name: 'new-issue'}" />
    <div v-if="treatmentName">
      <p class="message" v-html="$t('cta-sub-text-autonomy', {count: number_of_contributors})" v-if="treatmentName=='autonomy'" />
      <p class="message" v-html="$t('cta-sub-text-control')" v-if="treatmentName=='control'" />
    </div>
  </div>
</template>

<i18n>
{
  "en": {
    "cta-lead-text": "Make our community a better place!",
    "cta-lead-text-autonomy": "We need everyone's contribution!",
    "cta-lead-text-control": "Become a Top Contributor of the Week!",
    "cta-sub-text-autonomy": "{count} other people contributed today.<br>Your ideas matter.",
    "cta-sub-text-control": "",
    "cta-button-text": "Share your idea"
  },
  "ko": {
    "cta-lead-text": "우리 커뮤니티를 더 좋은 곳으로 만드세요!",
    "cta-lead-text-autonomy": "우리 모두의 참여가 필요합니다!",
    "cta-lead-text-control": "이번 주 최우수 사용자가 되세요!",
    "cta-sub-text-autonomy": "오늘 {count} 명의 사람들이 참여했습니다.<br>당신의 아이디어는 소중합니다.",
    "cta-sub-text-control": "",
    "cta-button-text": "당신의 아이디어 공유하기"
  }
}
</i18n>

<script>
import moment from 'moment';
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  data () {
    return {
      stats: {},
    };
  },
  created () {
    this.fetchData();
  },
  watch: {
    '$route': 'fetchData'
  },
  computed: {
    number_of_contributors() {
      let num = 0;
      if (this.$data.stats.number_of_contrbutors) {
        num = this.$data.stats.number_of_contrbutors.today;
      }
      const hours = moment().get('hour');
      const estimate = Math.floor(hours / 4);
      return Math.max(num, estimate);
    },
  },
  methods: {
    fetchData() {
      this.$store.dispatch('getStats').then(stats => {
        this.$data.stats = stats;
      });
    }
  }
};
</script>

<style lang="scss" scoped>
p {
  margin-bottom: .75em;
}
.message {
  margin: .75em 0 0;
}
.call-to-action {
  font-size: .9em;
}
</style>
