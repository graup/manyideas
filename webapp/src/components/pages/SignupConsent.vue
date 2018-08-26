<template>
  <div class="viewport hello has-header">
    <header>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
      <div class="view-title">{{$t('title')}}</div>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
    </header>

    <main class="content">

      <p class="intro">{{$t('consent-intro')}}</p>

      <div class="consent-text-wrap">
        <div class="consent-text">

<p>1.  본  연구는  오로지  연구만을  목적으로  수행됩니다.</p>

<p>2.  연구의  배경  및  목적<br>
자발적인 참여를보다 효과적으로 만드는 전략을 연구하고 있습니다. 이 연구의 결과는 시민 기술의 디자인을 향상 시키는데 사용될 것입니다. 이 실험은 "소셜컴퓨팅  기술을  활용한  국가  청렴도  개선" 연구의 일부입니다.</p>

<p>3.  예상  참여기간  및  본  시험에  참여하는  대략의  전체  피험자  수 <br>
KAIST의 모든 구성원이 본 응용 프로그램을 사용하여 자유롭게 이 연구에 참여하도록 초청합니다.
</p>

<p>4.  본  연구에  참여하게  됨으로써  받게  되는  검사  및  절차<br>
참가자는 응용 프로그램을 자유롭게 사용합니다.</p>

<p>5.  본  연구에  참여함으로써  피험자(피험자가  임부일  경우  태아,  수유부일  경우  영유아)에게  미칠  것 으로  예견되는  위험(부작용)이나  불편사항 <br>
본 실험에서는 일체의 침습적 처치 혹은 약물을 사용하지 않습니다. 데이터 수집은 웹 인터페이스를 통해서 이루어집니다. 이에 예견되는 위험이나 불편사항은 없습니다.</p>

<p>6.  이  연구에  참여함으로써  기대되는  이익 <br>
해당 인터페이스가 다루는 사회적, 정치적 지식에 대한 새로운 접근을 경험하실 수 있습니다. 또 한, 연구를 통해 얻은 정보는 추후 관련 연구에 도움이 됩니다.</p>

<p>7.  신분의  비밀보장  및  개인정보  보호(자료의  열람  권한  설정  및  보관,  관리,  폐기,  임상시험  결과  발표  시  피험자의  신원  보호) <br>
개인 정보 보호를 위해 모든 데이터는 익명으로 처리되며, 추후 연구결과를 발표하게 될 시에 결과 내용에 연구대상자의 신원이 드러나는 식별정보는 포함되지 않을 것입니다. 수집된 정보는 외부에서 접근이 제한된 서버에 저장이 되며, 참여연구원에 의해서만 처리 및 가공되어 연구 결 과를 도출하는 용도로만 이용될 것입니다. 수집된 정보는 연구 기간 종료 후 전량 파기 조치하 고, 만일 데이터 수집 기간 동안 참가자로부터 수집 중단 및 데이터 이용 중단 요구가 있을 경우 참가를 중단하고 해당 참가자의 데이터는 모두 파기할 것입니다.</p>

<p>8.  연구와  관련된  손상이  발생하였을  경우  피험자에게  주어질  보상이나  치료방법 <br>
본 연구는 연구 참가자에게 어떤 조작을 가하거나 육체적인 활동을 요구하지 않습니다. 만약 이 연구에 의한 손상이 발생했다고 판단될 경우 그에 상응하는 보상을 할 것입니다.</p>

<p>9.  피험자가  연구의  참가에  동의하지  않더라도  불이익이나  차별을  받지  않는다는  것  /  피험자가  자 발적으로  연구의  참가를  동의한  경우라도  자유의사에  의해  언제든지  이를  철회할  수  있다는  내 용(단,  이와  같은  철회가  시험  개시  이전에  이루어지고  연구참가에  대한  보상이  있었던  경우  보 상금의  반환  여부) <br>
본 실험에 참가 여부를 결정하는 것은 피험자에 달려있습니다. 피험자는 언제든지 연구에 참여 하지 않기로 결정할 수 있고 또한 중도에 그만둘 수 있습니다. 피험자가 본 연구에 참여하지 않아도 아무런 불이익을 받지 않습니다. 인터페이스 사용 중 불편을 느끼고 연구 참가를 중단 하고 싶다면 언제든지 중지할 수 있습니다. 그리고 수집된 데이터의 이용 중단을 요구할 경우 연 구진은 수집 데이터 일체를 파기할 것입니다.</p>

<p>10.  본  연구를  위해  피험자가  준수해야  하는  사항<br>
본 연구를 오염시키기 위한 악의적인 목적으로 인터페이스 사용에 임하지 말아야 합니다. 연구 원이 피험자가 악의적인 목적을 가지고 있다고 판단한다면, 관련 데이터를 파기할 수 있습니 다.</p>

<p>11. 연구에  참여함으로써  받게  되는  금전적  보상  유무  및  참여정도에  따른  조정  정도  및  연구 에  참여함으로써  피험자에게  추가적으로  발생이  예상되는  비용<br>
연구에 참여는 자발적이며 무보수입니다.</p>

<p>12. 연구의  지속  참여  의지에  영향을  줄  수  있는  새로운  정보가  얻어지면  적시에  피험자  본인  또 는  대리인에게  알려드릴  것입니다.</p>

<p>13. 연구진이  필요하다고  판단할  경우,  본인의  동의  없이도  본  연구  참여에서  제한될  수  있습니다.  또한  이  경우  연구책임자  또는  동의서상에  명시된  연구자에게  통보함으로써  본  연구에서  불참 할  수  있습니다.</p>

<p>14. 연구에  대한  추가적인  정보를  얻고자  하거나  연구와  관련이  있는  손상이  발생한  경우에  접촉해야  하는  사람과  연락처 <br>
본  연구의  참여와  관련하여  문의  및  불만  사항이  있으신  경우에는  언제든지  연구진에게  연락  하여  주시기  바랍니다. </p>

<hr>
<p>
본인은 이 동의서를 읽고 이해하였으며 모든 질문에 대한 답변을 들었습니다. 이에 본인 은 자발적으로 본 연구에 참여함을 서명으로 확인합니다.
또한, 본인은<br>
1. 본인과 연구자 및 KAIST 사이에 본인의 연구 참여결정에 영향을 줄 수 있는 어떠 한 관계도 없고,<br>
2. 요양원 같은 수용 시설에 거주하거나, 인지 기능에 문제가 있지 아니하며,<br>
3. 장애인이 아니며,<br>
4. 만약, 위에 열거한 1, 2, 3의 상황에 해당되는 경우 생명윤리심의위원회 간사의 입 회하에 본 동의서에 대한 설명을 듣고 아래 서명을 하였음을 확인합니다.
</p>

<p>연구 책임자: 김주호, 전산학과 교수. 전화번호: 042-350-3570. 이메일: juhokim@kaist.ac.kr</p>
</div>
</div>

        <form action="" class="form">
          <div class="form-group button-group vertical spaced" style="max-width: 200px;">
            <my-button :text="$t('consent-button')" primary={true} v-on:click.native.capture="consent" />
          </div>
        </form>

    </main>
    <footer></footer>
  </div>
</template>

<i18n>
{
  "en": {
    "consent-intro": "This application is part of a research project administered by KIXLAB, School of Computing, KAIST. Please make sure to read and understand the following information.",
    "consent-button": "Accept",
    "title": "Consent"
  },
  "ko": {
    "consent-intro": "본 응용 프로그램은 카이스트 전산학부 KIXLAB에서 진행하는 연구 프로젝트입니다. 다음 정보를 읽고 동의합니다 버튼을 눌러주세요.",
    "consent-button": "동의합니다",
    "title": "피험자 동의"
  }
}
</i18n>

<script>
import ChevronLeftIcon from "icons/chevron-left";
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  methods: {
    consent() {
      this.$router.push('signup');
    },
  },
  components: {
    ChevronLeftIcon,
  },
};
</script>

<style lang="scss" scoped>
.intro {
  padding: 0 2em;
  margin: 1rem 0;
  text-align: center;
}
.consent-text-wrap {
  margin: 1rem 1rem 2rem;
  padding:  1rem;
  box-sizing: border-box;
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 10px 25px rgba(50, 50, 93, 0.1), 0 5px 5px rgba(0, 0, 0, 0.07);

  .consent-text {
    max-height: 50vh;
    overflow-y: scroll;
    font-size: 90%;
    padding-right: .5rem;
  }
}
hr {
  border: 1px solid #ccc;
  border-width: 1px 0 0 0;
  margin: 1.5rem 4rem;
  
}
</style>
