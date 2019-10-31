<template>
  <div id="app">
    <UploadPage msg="An auto blog poster. Powered by Blur."/>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import UploadPage from './components/UploadPage.vue'

export default {
  name: 'app',
  components: {
    UploadPage
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
