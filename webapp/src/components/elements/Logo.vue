<template>
  <div class="logo">
    <span><em>{{instanceName}}</em><br> Many Ideas</span>
    <img src="../../assets/logo.png">
  </div>
</template>

<script>
export default {
  name: 'app-logo',
  props: ['instanceName'],
};
</script>

<style lang="scss">
.logo {
  display: inline-block;

  height: 90px;
  line-height: 90px;

  margin: 2.5rem 0;

  color: #43708F;
  font-family: 'Patua One', serif;
  font-weight: normal;
  font-size: 36px; /*font-size: 42px;*/

  span {
    line-height: 1;
    display: inline-block;
    text-align: left;

    em {
      font-style: normal;
      font-size: 80%;
      color: #A32902;
    }
  }

  img {
    width: auto;
    height: 70px; /*height: 85px;*/
  }

  &.small {
    height: 50px;
    line-height: 50px;
    font-size: 22px;

    img {
      height: 40px;
    }
  }
  &.inverted {
    color: #fff;
  }
}

</style>
