<template>
  <ul class="comment-list">
    <transition-group name="comment-appear">
      <li v-for="item in items" v-bind:key="item.id">
        <Comment v-bind:item="item"></Comment>
      </li>
    </transition-group>
  </ul>
</template>

<script>
import Comment from "@/components/elements/Comment";

export default {
  props: ['items'],
  components: {
    Comment,
  },
};
</script>

<style lang="scss">
.comment-list {
  margin: 2rem 0;
  padding: 0;
  list-style: none;
}
.comment-appear-enter-active, .comment-appear-leave-active {
  transition: all .5s cubic-bezier(.55,0,.1,1);
}
.comment-appear-enter, .comment-appear-leave-to {
  opacity: 0;
  margin-top: -90px;

}

</style>
