<template>
  <div class="viewport has-header" v-touch:swipe.right="showMenu" v-touch:swipe.left="hideMenu">
    <header>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
      <div class="view-title">FAQ</div>
      <div class="icon-button" v-on:click="toggleMenu"><MenuIcon /></div>
    </header>
    <main class="content">
      <div style="text-align: center">
        <app-logo instance-name="KAIST" />
      </div>

      <p class="question" v-html="$t('faq-q-1')" />
      <p v-html="$t('faq-a-1')" />

      <p class="question" v-html="$t('faq-q-2')" />
      <p v-html="$t('faq-a-2')" v-if="treatmentName=='baseline'" />
      <p v-html="$t('faq-a-2-autonomy')" v-if="treatmentName=='autonomy'" />
      <p v-html="$t('faq-a-2-control')" v-if="treatmentName=='control'" />

      <p class="question" v-html="$t('faq-q-3')" />
      <p v-html="$t('faq-a-3')" />

      <p class="question" v-html="$t('faq-q-4')" />
      <p v-html="$t('faq-a-4')" />

      <p class="question" v-html="$t('faq-q-5')" />
      <p v-html="$t('faq-a-5')" />
    </main>
    <footer></footer>
  </div>
</template>

<i18n>
{
  "en": {
    "faq-q-1": "What is this app about?",
    "faq-a-1": "We're trying to make KAIST a better place. We want to collect everyone's diverse ideas. What do you think would make life on campus better?",
    "faq-q-2": "Why should I participate?",
    "faq-a-2": "You can have an impact on improving conditions for everyone. We are also preparing several rewards for good ideas and active contributors. We will share the details with you later, but rest assured all active participants are always eligible for all rewards.",
    "faq-a-2-autonomy": "You can have a real impact on improving conditions for everybody! The best ideas may be presented to the school and followed up with concrete steps to support their implementation.",
    "faq-a-2-control": "You can have a real impact on improving conditions for everybody! The best ideas may be presented to the school and followed up with concrete steps to support their implementation.",
    "faq-q-3": "What do you do with my data?",
    "faq-a-3": "We take privacy very seriously. Your personal information will not be shared with third parties. All data collected in this app will only be published in anonymized form. The data will be used for our research about design of voluntary participation apps. All personally identifiable data will be destroyed after the end of the study.",
    "faq-q-4": "Who's behind this?",
    "faq-a-4": "This is a research project from <a href='http://kixlab.org' target='_blank'>KIXLAB</a> at KAIST School of Computing. We are advised by Prof. Juho Kim.",
    "faq-q-5": "I have more questions.",
    "faq-a-5": "Don't hesitate to contact us any time! The easiest is by email: <a href='mailto:grau@kaist.ac.kr'>grau@kaist.ac.kr</a>."
  },
  "ko": {
    "faq-q-1": "뭐하는 앱인가요?",
    "faq-a-1": "우리는 KAIST를 더 나은 곳으로 만들기 위해 노력하고 있습니다. 우리는 모든 사람들의 다양한 아이디어를 모으고자 합니다. 더 나은 캠퍼스 라이프를 위해 어떤 일들을 할 수 있을까요?",
    "faq-q-2": "왜 제가 참여해야 하죠?",
    "faq-a-2": "교내 구성원들의 더 나은 삶을 만드는 데에 긍정적인 영향을 미칠 수 있습니다.",
    "faq-a-2-autonomy": "교내 구성원들의 더 나은 삶을 만드는 데에 긍정적인 영향을 미칠 수 있습니다.",
    "faq-a-2-control": "교내 구성원들의 더 나은 삶을 만드는 데에 긍정적인 영향을 미칠 수 있습니다.",
    "faq-q-3": "제 활동기록(사용 데이터)는 어떻게 처리되나요?",
    "faq-a-3": "저희 연구팀은 개인정보보호를 매우 중요하게 생각합니다. 귀하의 개인 정보는 제 3 자와 공유되지 않습니다. 이 앱에서 수집 된 모든 데이터는 익명으로 게시됩니다. 이 데이터는 자발적 참여 앱 디자인에 대한 연구 목적으로만 사용될 것입니다. 모든 개인 식별 데이터는 연구가 끝난 후에 폐기됩니다.",
    "faq-q-4": "이 프로젝트를 진행하는 사람이 누구에요?",
    "faq-a-4": "카이스트 전산학부 <a href='http://kixlab.org' target='_blank'>KIXLAB</a> (지도교수: 김주호)에서 진행하는 연구 프로젝트입니다.",
    "faq-q-5": "질문이 더 있어요.",
    "faq-a-5": "언제든지 저희 연구팀에게 이메일로 연락을 주세요! <a href='mailto:grau@kaist.ac.kr'>grau@kaist.ac.kr</a>."
  }
}
</i18n>

<script>
import MenuIcon from "icons/menu";
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  name: 'FAQ',
  components: {
    MenuIcon,
  }
};
</script>

<style scoped>
.content {
  padding: 1em;
}
.question {
  font-weight: bold;
  margin-bottom: 0;
}
</style>
