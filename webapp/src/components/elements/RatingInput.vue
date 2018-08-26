<template>
  <div class="rating">
    <ul class="rating-items">
      <li v-for="item in items" v-bind:key="item.id">
        <label>
          <input type="radio" :name="name" required
            v-bind:value="item.id"
            v-on:change="$emit('input', item.id)"
            v-bind:checked="item.id == value">
          {{item.label}}
        </label>
      </li>
    </ul>
    <ul class="rating-items rating-labels">
      <li>{{$t('complete-disagree')}}</li>
      <li>{{$t('complete-agree')}}</li>
    </ul>
  </div>
</template>

<i18n>
{
  "en": {
    "complete-disagree": "completely disagree",
    "complete-agree": "completely agree"
  },
  "ko": {
    "complete-disagree": "전혀 동의하지 않는다",
    "complete-agree": "완전히 동의한다"
  }
}
</i18n>

<script>
import {localeMixin} from "@/mixins";

export default {
  mixins: [localeMixin],
  props: ['min', 'max', 'value'],
  computed: {
    name() {
      return(Math.random().toString(36).substring(7));
    },
    items() {
      const max = parseInt(this.max);
      const min = parseInt(this.min);
      return [...Array(max).keys()].map(i => ({id: (i+min), label: i+min}));
    }
  }
};
</script>

<style lang="scss">
.rating {
  margin: 0 0 1.5rem;

  .rating-items {
    list-style: none;
    display: flex;
    margin: 0;
    padding: 0;
    justify-content: space-between;
    justify-content: stretch;

    li {
      flex: 1;
      text-align: center;

      label {
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        padding: .75rem 0;
      }

      input {
        margin-bottom: 4px;
      }
    }
  }

  .rating-labels {
    li {
      text-align: center;
      font-size: 85%;

      &:first-child {
        text-align: left;
      }
      &:last-child {
        text-align: right;
      }
    }
  }
}
</style>
