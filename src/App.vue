<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <GameMenu/>
    <GameBoard/>
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
