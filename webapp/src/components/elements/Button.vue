<template>
  <div class="button" v-bind:class="{primary, loading, icon}" v-on:click="click">
    <span class="label"><slot>{{text}}</slot></span>
    <Spinner v-if="loading" size="18px" />
  </div>
</template>

<script>
import Spinner from './Spinner';

export default {
  name: 'Button',
  props: ['text', 'primary', 'icon', 'linkTo', 'loading'],
  methods: {
    click() {
      if (typeof this.$props.linkTo !== 'undefined') {
        this.$router.push(this.$props.linkTo);
        return;
      }
    },
  },
  components: {
    Spinner,
  },
};
</script>

<style lang="scss">
.button {
  display: inline-block;
  border-radius: 4px;
  line-height: 2.5;
  padding: 0 1.5em;
  font-weight: 600;
  text-align: center;

  background-color: #8FB5CE;
  color: #fff;
  cursor: pointer;
  box-sizing: border-box;

  transition: all .4s cubic-bezier(0.84, 0, 0.66, 1);

  &:hover {
    text-decoration: none;
    background-color: darken(#8FB5CE, 10%);
  }

  &.primary {
    background-color: #386b8d;

    &:hover {
      background-color: darken(#386b8d, 10%);
    }
  }

  &.icon {
    padding: 0 .5em;
  }

  &.huge {
    font-size: 110%;
  }

  .label {
    opacity: 1;
    transition: opacity .4s;
    white-space: nowrap;

    svg {
      fill: #fff;
      vertical-align: middle;
    }
  }

  max-width: 400px;
  &.loading {
    max-width: 50px;

    .label {
      opacity: 0;
    }

    position: relative;

    .spinner {
      position: absolute;
      top: 0;
      left: 50%;
      margin: 8px 0 0 -9px;
    }
  }
}
.button-group {
  display: flex;

  /*&.horizontal {

  }*/
  &.vertical {
    flex-direction: column;
    align-items: center;
    margin-left: auto;
    margin-right: auto;

    .button {
      margin-bottom: 1rem;
      display: block;
      width: 100%;

      &:last-child {
        margin-bottom: 0;
      }
    }

  }
}

.button-icon {
  svg {
    width: 20px;
    height: 20px;
    transform: translateY(-2px);
  }
}

.button-list .button {
  border: 1px solid #bbb;
  background-color: #fff;
  color: #333;

  svg {
    fill: #666;
  }
}
</style>
