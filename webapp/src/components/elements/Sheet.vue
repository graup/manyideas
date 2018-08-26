<template>
  <div class="sheet" v-bind:class="{visible}">
    <div class="darken" v-on:click="hide()"></div>
    <div class="content">
      <slot></slot>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Sheet',
  data () {
    return {
      visible: false,
    }
  },
  methods: {
    hide() {
      this.visible = false;
    },
    show() {
      this.visible = true;
    },
  },
  components: {
  },
};
</script>

<style lang="scss">
.sheet {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  
  pointer-events: none;
  z-index: 9999;

  &.visible {
    pointer-events: all;
  }

  .darken {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0,0,0,0.3);

    opacity: 0;
    transition: all .3s;
  }
  &.visible .darken {
    opacity: 1;
  }

  .content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #fff;
    padding: 20px;
    text-align: center;

    max-height: 70vh;
    overflow: scroll;

    transform: translateY(100%);
    transition: transform .25s;

    opacity: 0;
  }
  &.visible .content {
    transform: translateY(0%);

    opacity: 1;
  }
}

.button-list {
  display: flex;
  flex-direction: column;

  > * {
    margin-bottom: 10px;

    &:last-child {
      margin-bottom: 0;
    }
  }
}
</style>
