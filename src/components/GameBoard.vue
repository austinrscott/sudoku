<template>
  <div class="board">
    <div v-for="(cell, index) in allCells"
         :data-row="getRow(index)"
         :data-column="index % 9"
         :class="{'board__cell': true, 'board__cell--expanded': expanded[0]}"
         :key="`board-cell-${index}`"
         style="{
          'grid-column': getColumn(index),
          'grid-row': getRow(index)
         }"
         @click="expand">
      {{cell.value ? cell.value : ''}}
    </div>
  </div>
</template>

<script>
export default {
  name: "GameBoard",
  methods: {
    getRow(index) {
      return Math.floor(index / 9);
    },
    getColumn(index) {
      return index % 9;
    },
    expand(event) {
      this.expanded = [event.target.dataset.row, event.target.dataset.column];
    }
  },
  data() {
    return {
      board: Array(9).fill(Array(9).fill(0)),
      expanded: null
    }
  },
  computed: {
    allCells() {
      return this.board.reduce(
        (array, line, row) => [
          ...array,
          ...line.map((value, column) => ({value, row, column}))
        ], []);
    }
  }
}
</script>

<style scoped>
.board {
  --cell-size: 25px;

  display: grid;
  grid: repeat(9, var(--cell-size)) / repeat(9, var(--cell-size));
  justify-content: center;
}

.board__cell {
  border: 1px solid lightgray;
  width: var(--cell-size);
  height: var(--cell-size);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.board__cell--expanded {
  outline: 1px red solid;
}

.board__cell:hover {
  background-color: #ffd;
  box-shadow: inset 5px 5px black;
}
</style>
