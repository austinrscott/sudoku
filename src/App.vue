<template>
  <div id="app">
    <GameMenu/>
    <GameBoard :board="board"/>
    <span v-for="[key, value] in Object.entries(debug)" :key="key">
      <strong>{{ key }}: </strong>
      <span>{{ value }}</span>
    </span>
  </div>
</template>

<script>
import GameMenu from "@/components/GameMenu";
import GameBoard from "@/components/GameBoard";
import Board from "@/models/gameBoard";

export default {
  name: 'App',
  components: {
    GameBoard,
    GameMenu,
  },
  data() {
    return {
      board: Board(),
    }
  },
  computed: {
    debug() {
      return {
        test: `${JSON.stringify(this.board.groups)}`
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
