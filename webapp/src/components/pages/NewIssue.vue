<template>
  <div class="viewport post-issue has-header">
    <Sheet ref="sheet">
      <div class="big-loading" v-if="locationLoading">
        <Spinner />
        {{$t('searching-places')}}
      </div>
      
      <div v-if="errors.location">
        <p class="error">{{errors.location.join(' ')}}</p>
        <my-button :text="$t('try-again')" v-on:click.native.capture="showNearPlaces" />
        <my-button :text="$t('cancel')" v-on:click.native.capture="$refs.sheet.hide()" primary={true} />
      </div>

      <div v-if="nearPlaces.length">
        <p>{{$t('select-place')}}</p>
        <ul class="near-places-list">
          <li v-for="place in nearPlaces" v-bind:key="place.id" v-on:click="selectPlace(place)">
            <span class="distance">{{Math.round(place.distance*1000)}}m</span>
            {{place.tags.name}}
          </li>
        </ul>
        <my-button :text="$t('cancel')" v-on:click.native.capture="$refs.sheet.hide()" primary={true} />
      </div>
    </Sheet>


    <header>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
      <div class="view-title">{{$t('new-idea')}}</div>
      <div class="icon-button" v-on:click="goBack"><ChevronLeftIcon /></div>
    </header>
    <main class="content">
      <p class="intro">
        {{$t('intro-text')}}
      </p>
      <p v-if="treatmentName" class="intro">
        <span v-html="$t('sub-text-autonomy')" v-if="treatmentName=='autonomy'" />
        <span v-html="$t('sub-text-control')" v-if="treatmentName=='control'" />
      </p>

      <div class="form-wrapper form-wide">
        <form action="" class="form">
          <div class="form-group">
            <input id="title" class="form-input" type="text" v-model="title" required />
            <label class="form-label" for="title">{{$t('title-label')}}</label>
            <div class="error" v-if="errors.title">{{errors.title.join(' ')}}</div>
          </div>
          <div class="form-group">
            <textarea id="text" class="form-input" v-model="text" required :placeholder="$t('description-placeholder')"></textarea>
            <label class="form-label" for="text">{{$t('description-label')}}</label>
            <div class="error" v-if="errors.text">{{errors.text.join(' ')}}</div>
          </div>
          <div class="form-group">
            <p class="like-form-label">{{$t('attachments-label')}}</p>
            <my-button text="Location" v-on:click.native.capture="showNearPlaces" icon={true}><LocationIcon /></my-button>
            {{location.name}}
          </div>
          <div class="form-group button-group vertical spaced" style="max-width: 200px;">
            <my-button :text="$t('post-idea-button')" primary={true} v-on:click.native.capture="createIssue" />
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
    "new-idea": "New Idea",
    "intro-text": "What is your idea to make KAIST a better place? It could be about facilities, organization, social problems, ...",
    "sub-text-autonomy": "<strong>Let's have a real impact together!</strong>",
    "sub-text-control": "",
    "title-label": "What's your idea in one sentence?",
    "description-label": "Describe your idea in a bit more detail",
    "description-placeholder": "Reasons, expected outcomes, affected population...",
    "attachments-label": "Attach place (optional)",
    "post-idea-button": "Post Idea",
    "select-place": "Select a place related to this idea",
    "searching-places": "Finding places near you...",
    "cancel": "Cancel",
    "try-again": "Try again"
  },
  "ko": {
    "new-idea": "새로운 아이디어",
    "intro-text": "KAIST를 더 좋은 곳으로 만들기 위한 당신의 생각은 무엇인가요? 시설, 조직, 문화 문제 등...",
    "sub-text-autonomy": "<strong>함께 변화를 만들어 보아요!</strong>",
    "sub-text-control": "",
    "title-label": "아이디어를 한 문장 이내로 써주세요",
    "description-label": "아이디어를 자세하게 설명해주세요",
    "description-placeholder": "이유, 예상 결과, 대상 등",
    "attachments-label": "위치 첨부 (선택 사항)",
    "post-idea-button": "아이디어 게시하기",
    "select-place": "이 아이디어와 관련된 장소를 선택해주세요.",
    "searching-places": "근처 장소를 찾는 중...",
    "cancel": "취소",
    "try-again": "다시 시도"
  }
}
</i18n>

<script>
import ChevronLeftIcon from "icons/chevron-left";
import LocationIcon from "icons/map-marker";
import {navigationMixins} from "@/mixins";
import {getPlacesAroundPoint} from "@/utils/geo";
import Sheet from "@/components/elements/Sheet";
import Spinner from '@/components/elements/Spinner';

export default {
  mixins: [navigationMixins],
  components: {
    ChevronLeftIcon,
    LocationIcon,
    Sheet,
    Spinner,
  },
  data() {
    return {
      title: '',
      text: '',
      location: {},
      categories: [1],
      errors: {},
      loading: false,
      nearPlaces: [],
      locationLoading: false,
    };
  },
  methods: {
    createIssue() {
      this.$data.loading = true;
      let data = {
        title: this.$data.title,
        text: this.$data.text,
        categories: this.$data.categories,
      };
      if (Object.keys(this.$data.location).length) {
        data.location = this.$data.location;
      }
      this.$store.dispatch('createIssue', { issue: data }).then((issue) => {
        this.$router.push({ name: 'issue-detail', params: { slug: issue.slug, item: issue }});
      }).catch(error => {
        this.$data.errors = error.response.data;
        this.$data.loading = false;
      });
    },
    showNearPlaces() {
      if (this.locationLoading || this.nearPlaces.length) {
        // still loading or already loaded
        this.$refs.sheet.show();
        return;
      }
      if (navigator.geolocation) {
        this.locationLoading = true;
        this.nearPlaces = [];
        this.errors.location = null;
        this.$refs.sheet.show();
        navigator.geolocation.getCurrentPosition((position) => {
          getPlacesAroundPoint(position.coords.latitude, position.coords.longitude).then((places) => {
            this.nearPlaces = places;
            this.locationLoading = false;
          });
        }, (error) => {
          let msgs = {
            [error.PERMISSION_DENIED]: "You denied getting access to your location.",
            [error.POSITION_UNAVAILABLE]: "Your location information is unavailable.",
            [error.TIMEOUT]: "Finding your location is taking too long.",
            [error.UNKNOWN_ERROR]: "An unknown error occurred.",
          }
          this.errors.location = [msgs[error.code]];
          this.locationLoading = false;
        }, {
          enableHighAccuracy: false,
          timeout: 60000,
          maximumAge: 10*1000
        });
      }
    },
    selectPlace(place) {
      this.location = {
        'name': place.tags.name,
        'external_id': place.id,
        'lat': place.center.lat,
        'lon': place.center.lon,
      };
      this.$refs.sheet.hide();
    },
  },
};
</script>

<style lang="scss" scoped>
.intro {
  padding: 0 2em;
  margin: 1rem 0;
  text-align: center;
}
textarea {
  height: 150px;
}
.near-places-list {
  list-style: none;
  margin: 0 0 20px 0;
  padding: 0;

  li {
    line-height: 40px;
    border-bottom: 1px solid #eee;
    text-align: left;
    cursor: pointer;

    .distance {
      float: right;
      color: #999;
      font-size: 90%;
    }
  }
}
</style>
