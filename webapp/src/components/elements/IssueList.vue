<template>
  <ul class="issue-list">
    <li v-for="item in items" v-bind:key="item.id">
      <Issue v-bind:item="item"></Issue>
    </li>
  </ul>
</template>

<script>
import Issue from "@/components/elements/Issue";

export default {
  props: ['items'],
  components: {
    Issue,
  },
};
</script>

<style lang="scss">
.issue-list {
  margin: 0;
  padding: 0;
  list-style: none;

}
</style>
