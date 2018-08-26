<template>
  <div class="viewport hello has-header">
    <header>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
      <div class="view-title">{{$t('title')}}</div>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
    </header>

    <main class="content">

      <p class="intro">{{$t('test-intro')}}</p>

      <div class="form-wrapper">

        <form action="" class="form">
          <div class="form-group">
            <label for="age">{{$t('age')}}</label>
            <select id="age" class="form-input" v-model="userData.age" required>
              <option value="">{{$t('please-select')}}</option>
              <option value="1826">18-26</option>
              <option value="2732">27-32</option>
              <option value="3340">33-40</option>
              <option value="4155">41-55</option>
              <option value="56">56+</option>
            </select>
            
            <div class="error" v-if="errors.age">{{errors.age.join(' ')}}</div>
          </div>
          <div class="form-group">
            <label for="sex">{{$t('sex')}}</label>
            <select id="sex" class="form-input" v-model="userData.sex" required>
              <option value="">{{$t('please-select')}}</option>
              <option value="female">{{$t('female')}}</option>
              <option value="male">{{$t('male')}}</option>
            </select>
            
            <div class="error" v-if="errors.sex">{{errors.sex.join(' ')}}</div>
          </div>
          <div class="form-group">
            <label for="occupation">{{$t('occupation')}}</label>
            <select id="occupation" class="form-input" v-model="userData.occupation" required>
              <option value="">{{$t('please-select')}}</option>
              <option value="undergrad">{{$t('undergrad')}}</option>
              <option value="grad">{{$t('grad')}}</option>
              <option value="faculty">{{$t('faculty')}}</option>
              <option value="staff">{{$t('staff')}}</option>
              <option value="other">{{$t('other')}}</option>
            </select>
            
            <div class="error" v-if="errors.occupation">{{errors.occupation.join(' ')}}</div>
          </div>

          <div class="form-group">
            <p>{{$t('test-instruction')}}</p>
          </div>

          <p style="margin-top: 1.5rem">{{$t('gcos-prompt')}}</p>

          <div class="form-group">
            <strong>{{$t('q2-question')}}</strong><br>
            {{$t('q2-answer')}}
            <RatingInput min="1" max="7" v-model="userData.score_impersonal" />
            <div class="error" v-if="errors.score_impersonal">{{errors.score_impersonal.join(' ')}}</div>
          </div>

          <div class="form-group">
            <strong>{{$t('q3-question')}}</strong><br>
            {{$t('q3-answer')}}
            <RatingInput min="1" max="7" v-model="userData.score_control" />
            <div class="error" v-if="errors.score_control">{{errors.score_control.join(' ')}}</div>
          </div>

          <div class="form-group">
            <strong>{{$t('q4-question')}}</strong><br>
            {{$t('q4-answer')}}
            <RatingInput min="1" max="7" v-model="userData.score_autonomy" />
            <div class="error" v-if="errors.score_autonomy">{{errors.score_autonomy.join(' ')}}</div>
          </div>

          <div class="form-group">
            <strong>{{$t('q1-question')}}</strong><br>
            {{$t('q1-answer')}}
            <RatingInput min="1" max="7" v-model="userData.score_amotivation" />
            <div class="error" v-if="errors.score_amotivation">{{errors.score_amotivation.join(' ')}}</div>
          </div>

          <div class="form-group button-group vertical spaced" style="max-width: 200px;">
            <my-button :text="$t('continue-button')" primary={true} v-on:click.native.capture="saveInfo" v-bind:loading="loading" />
          </div>
        </form>
      </div>
    </main>
    <footer></footer>
  </div>
</template>

<i18n>
{
  "en": {
    "title": "Sign up Information",
    "test-intro": "Please answer the following questions honestly. This information is important for our research. It is not used inside this application and will always be kept private.",
    "age": "Age range",
    "please-select": "Please select",
    "sex": "Sex",
    "female": "Female",
    "male": "Male",
    "occupation": "Position",
    "undergrad": "Undergrad student",
    "grad": "Grad student",
    "faculty": "Faculty",
    "staff": "Staff",
    "other": "Other",
    "continue-button": "Continue",
    "test-instruction": "To help us better understand your personal attitude towards civic participation, please answer the following questions.",
    "gcos-prompt": "Imagine the following situations and how you would respond.",
    "q1-question": "Whether you volunteer or not, what do you think is the reason for that?",
    "q1-answer": "I don’t know; I can’t see what I’m getting out of it.",
    "q2-question": "You have a school-age daughter. On parents' night the teacher tells you that your daughter is doing poorly and doesn't seem involved in the work.",
    "q2-answer": "You are likely to scold her and hope she does better.",
    "q3-question": "You have been invited to a large party where you know very few people. As you look forward to the evening, you would likely expect that:",
    "q3-answer": "You'll try to fit in with whatever is happening in order to have a good time and not look bad.",
    "q4-question": "A woman who works for you has generally done an adequate job. However, for the past two weeks her work has not been up to par and she appears to be less actively interested in her work. Your reaction is likely to be:",
    "q4-answer": "Ask her about the problem and let her know you are available to help work it out."
  },
  "ko": {
    "title": "가입 정보",
    "test-intro": "다음 질문에 솔직하게 답해주세요. 본 연구에 중요한 정보입니다. 애플리케이션에서는 사용되지 않으며 항상 비공개로 유지됩니다.",
    "age": "연령대",
    "please-select": "선택 해주세요",
    "sex": "성별",
    "female": "여성",
    "male": "남성",
    "student": "학생",
    "occupation": "직업",
    "undergrad": "학부생",
    "grad": "대학원생",
    "faculty": "교원",
    "staff": "직원",
    "other": "기타",
    "continue-button": "계속하기",
    "test-instruction": "시민 참여에 대한 당신의 태도를 묻는 다음 질문에 답해 주세요.",
    "gcos-prompt": "다음과 같은 상황에서 당신은 어떻게 대응할지 상상해보세요.",
    "q1-question": "현재 당신이 자원 봉사를 하는지의 여부와 상관 없이, 자원 봉사를 하는 이유에 대해 생각해 본다면...",
    "q1-answer": "글쎄, 딱히 나에게 어떤 혜택이 돌아오는지 모르겠다.",
    "q2-question": "당신게 학교에 다니는 딸이 있는데, 딸의 학교 선생님이 당신게 딸이 학교에서 잘 못하고 있고 학업에 집중하지 못하는 것 같다고 말씀하셨습니다.",
    "q2-answer": "딸을 꾸짖고 더 잘하기를 기대한다",
    "q3-question": "당신이 큰 파티에 초대되었는데, 오는 사람 중 극소수와만 친분이 있습니다. 당신은 파티에 대해 어떤 생각을 하고 있을까요?",
    "q3-answer": "즐거운 시간을 보내고 나쁜 인상을 남기지 않기 위해 일어나고 있는 일에 적응하려고 노력할 것이다.",
    "q4-question": "그동안 전반적으로 일을 무난하게 해온 부하직원이 있습니다. 그러나 지난 2주 동안 이 직원의 일의 능률이 떨어지고 일에 소극적인 태도를 보였습니다.",
    "q4-answer": "부하직원에게 문제가 뭔지 물어보고, 해결에 도움을 줄 수 있다고 이야기한다."
  }
}
</i18n>

<script>
import ChevronLeftIcon from "icons/chevron-left";
import RatingInput from "../elements/RatingInput";
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  data() {
    return {
      userData: {
        occupation: '',
        age: '',
        sex: '',
        score_amotivation: null,
        score_autonomy: null,
        score_impersonal: null,
        score_control: null,
      },
      errors: {},
      loading: false,
    };
  },
  methods: {
    saveInfo() {
      this.$data.loading = true;
      console.log(this.userData);
      this.$store.dispatch('saveClassification', { user: this.userData, requestOptions: {} }).then(() => {
        let dest = 'feed';
        if (this.$router.authRequiredRoute) {
          dest = this.$router.authRequiredRoute.path;
          this.$router.authRequiredRoute = null;
        }
        this.$router.push(dest);
      }).catch(error => {
        if (error.response) {
          this.$data.errors = error.response.data;
        }
        console.log(error);
        this.$data.loading = false;
      });
    },
  },
  components: {
    ChevronLeftIcon,
    RatingInput,
  },
};
</script>

<style scoped>
.intro {
  padding: 0 2em;
  margin: 1rem 0;
  text-align: center;
}
</style>
