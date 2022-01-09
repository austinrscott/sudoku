<template>
  <div class="board">
    <GameCell v-for="(cell, index) in Object.values(board.cells)"
              :data-row="cell.row"
              :data-column="cell.column"
              :key="`sudoku-cell-${index}`"
              :cell="cell"
              :id="index"
              @cell:expand="handleCellExpand(index)"
              :expanded="expanded !== null && expanded === index"
              @change="handleCellChange"
    />
  </div>
</template>

<script>
import GameBoard from "@/models/gameBoard";
import GameCell from "@/components/GameCell";

export default {
  name: "GameBoard",
  expose: ['board'],
  components: {GameCell},
  created() {
    window.addEventListener('keydown', this.handleKeydown);
  },
  destroyed() {
    window.removeEventListener('keydown', this.handleKeydown);
  },
  methods: {
    handleKeydown(event) {
      if (this.expanded !== null) {
        switch (event.code) {
          case 'ArrowUp':
            this.handleCellExpand(Math.max(0, this.expanded - 9));
            break;
          case 'ArrowRight':
            this.handleCellExpand(Math.min(81, this.expanded + 1));
            break;
          case 'ArrowDown':
            this.handleCellExpand(Math.min(81, this.expanded + 9));
            break;
          case 'ArrowLeft':
            this.handleCellExpand(Math.max(1, this.expanded - 1));
            break;
          case 'Enter':
            this.expanded = null;
            break;
          default:
            if (['Digit', 'Numpad'].some(prefix => event.code.startsWith(prefix)) && parseInt(event.code.at(-1)) > 0) {
              this.handleCellChange(this.expanded, event.key);
            }
            break;
        }
      }
    },
    handleCellExpand(id) {
      this.expanded = id;
      window.addEventListener('click', () => this.expanded = null);
    },
    handleCellChange(id, value) {
      const row = Math.floor(id / 9);
      const column = id % 9;
      this.board.updateCell({row, column, value})
    }
  },
  data() {
    return {
      board: GameBoard(),
      expanded: null
    }
  },
}
</script>

<style scoped>
.board {
  --cell-size: 25px;

  display: grid;
  grid: repeat(9, var(--cell-size)) / repeat(9, var(--cell-size));
  justify-content: center;
  perspective: 200px;
}

.board >>> [data-row="2"]:after, [data-row="5"]:after {
  border-bottom: 2px black solid;
}
</style>
