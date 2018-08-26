<template>
  <div id="app">
    <NotificationCenter />
    <side-menu />
    <transition :name="transitionName">
      <router-view class="child-view" v-bind:class="{'menu-opened': isMenuOpened}" />
    </transition>
  </div>
</template>

<script>
import 'normalize.css';
import SideMenu from '@/components/elements/SideMenu';
import NotificationCenter from '@/components/elements/NotificationCenter';
import {navigationMixins} from "@/mixins";

export default {
  mixins: [navigationMixins],
  name: 'App',
  data () {
    return {
      transitionName: 'slide-left',
    }
  },
  watch: {
    '$route' (to, from) {
      const toDepth = to.path.split('/').length
      const fromDepth = from.path.split('/').length
      let goingUp = false;
      if (toDepth < fromDepth || to.path == '/') {
        goingUp = true;
      }
      this.transitionName = goingUp ? 'slide-right' : 'slide-left'
    }
  },
  components: {
    'side-menu': SideMenu,
    NotificationCenter,
  },
};
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Patua+One|Raleway:300,500,600');

body {
  background-color: #e7e7e7;
  -webkit-overflow-scrolling: touch;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;

  max-width: 420px; /* for testing mobile layout */
  margin: 0 auto;

  position: relative;
  background-color: #f4f4f4;

  overflow-x: hidden;

  .white {
    background-color: #fff;
  }
}
/* sticky footer */
.viewport {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  padding-bottom: 150px;
  box-sizing: border-box;
}
.content {
  flex: 1;
}
/* general typo */
p {
  line-height: 1.5;
  margin: 0 0 1em;
}
a {
  text-decoration: none;
}
/* buttons etc */
.icon-button {
  font-size: 120%;
  padding: 8px;
  cursor: pointer;
  line-height: 1;

  svg {
    vertical-align: middle;
  }
}
/* header */
header {
  display: flex;
  align-items: center;
  background-color: #d8d8d8;

  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 99;
  transition: all .2s;

  user-select: none;

  .view-title {
    /*flex: 1;*/
    text-align: center;
    line-height: 50px;
    font-weight: bold;
    text-transform: uppercase;
  }

  > :first-child {
    margin-right: auto;
  }
  > :last-child {
    /* put a copy of the first item here to achieve equal margins */
    margin-left: auto;
    &:not(.visible) {
      visibility: hidden;
    }
  }

  @media (min-width: 600px) {
    /* debugging on desktop */
    max-width: 420px;
    left: 50%;
    margin-left: -210px;
  }

}
.viewport.has-header {
  main {
    margin-top: 50px;
  }
}

/* footer */
footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  .call-to-action {
    background-color: #f0f0f0;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 -1px 6px rgba(0,0,0,0.25);
  }
}

/* forms */
.form-wrapper {
  min-width: 300px;
  width: 85%;
  max-width: 400px;
  padding: 50px 2rem 50px 2rem;
  box-sizing: border-box;
  margin: 35px auto;   
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 10px 25px rgba(50,50,93,.1),0 5px 5px rgba(0,0,0,.07);

  &.form-wide {

  }
}

.form-group {
  position:relative;  

  & + .form-group {
    margin-top: 30px;
  }
}

.form-label {
  position: absolute;
  left: 0;
  top: 10px;
  color: #999;
  background-color: #fff;
  z-index: 10;
  transition: transform 150ms ease-out, font-size 150ms ease-out;
}


:focus + .form-label,
:valid + .form-label {
  transform: translateY(-125%);
  font-size: .75em;
}

.form-input {
  position: relative;
  padding: 12px 0px 5px 0;
  width: 100%;
  outline: 0;
  border: 0;
  box-shadow: 0 1px 0 0 #e5e5e5;
  transition: box-shadow 150ms ease-out;
  
  &:focus {
    box-shadow: 0 3px 0 -1px #386b8d;
    outline: 0;
  }
}

.form-input.filled {
  box-shadow: 0 2px 0 0 lightgreen;
}
.form-group .error {
  color: #c51111;
  margin: .5rem 0 0 0;
  font-size: 90%;
}
.form-group .help {
  color: #aaa;
  margin: .5rem 0 0 0;
  font-size: 90%; 
}

.empty-state {
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #aaa;
  font-size: 110%;
  margin: 1rem 2rem;
  text-align: center;
  line-height: 1.5;
  text-shadow: 0 1px 1px #fff;
}

.view-help {
  text-align: center;
  margin: 1rem 3rem;
  font-size: 90%;
  color: #aaa;
  line-height: 1.5;
  text-shadow: 0 1px 1px #fff;
}

.big-loading {
  text-align: center;
  font-size: 90%;
  padding: 3rem 0;

  .spinner {
    width: 60px;
    display: block;
    margin: 1.5rem auto;
  }

  max-height: 200px;
  box-sizing: border-box;
}
.button.loading .spinner {
  width: auto;
}

.fade-up-enter-active, .fade-up-leave-active {
  transition: all .5s, opacity .3s;
}
.fade-up-enter, .fade-up-leave-to {
  opacity: 0;
  max-height: 0;
  padding: 0;
}

.tutorial-message {
  padding: 1rem;
  margin: 1rem 0 0;
  background-color: #fff;
  border: 2px dashed #ccc;
  border-width: 2px 0;
  line-height: 1.3;
  font-size: 95%;
  text-align: justify;
  hyphens: auto;
}

/* page transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s ease;
}
.fade-enter, .fade-leave-active {
  opacity: 0
}

.child-view > * {
  transition: all .5s cubic-bezier(.55,0,.1,1);
}
.slide-left-enter > *, .slide-right-leave-active > *  {
  opacity: 0;
  transform: translate(50px, 0);
}
.slide-left-leave-active > * , .slide-right-enter > *  {
  opacity: 0;
  transform: translate(-50px, 0);
}

.viewport.menu-opened > * {
  transform: translateX(200px);
}

/* toasts */
.toasted-container.top-center {
  width: 85vw;
  max-width: 350px;
}
.toasted-container .toasted {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  flex-direction: column;
  align-items: flex-start;
}
.toasted-container .toasted.primary {
  font-weight: normal;
  padding: 10px 12px;
}
.toasted-container .toasted .action {
  margin: 0;
  padding: 0;
}

</style>
