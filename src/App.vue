<template>
  <div id="app">
    <GameMenu/>
    <GameBoard :ref="'board'"/>
    <span v-for="[key, value] in Object.entries(debug)" :key="key">
      <strong>{{ key }}</strong>
      <span>{{ value }}</span>
    </span>
  </div>
</template>

<script>
import GameMenu from "@/components/GameMenu";
import GameBoard from "@/components/GameBoard";

export default {
  name: 'App',
  components: {
    GameBoard,
    GameMenu,
  },
  computed: {
    debug() {
      return {
        test: this.$refs.board?.complete
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
