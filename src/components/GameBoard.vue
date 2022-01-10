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
    <div v-show="expanded !== null"
         class="board__expanded-shadow"
         :style="{gridArea: `${Math.floor(expanded / 9) + 1} / ${(expanded % 9) + 1}`}"/>
    <div class="board__row-divider" :style="{gridArea: '4 / 1'}"/>
    <div class="board__row-divider" :style="{gridArea: '7 / 1'}"/>
    <div class="board__column-divider" :style="{gridArea: '1 / 4'}"/>
    <div class="board__column-divider" :style="{gridArea: '1 / 7'}"/>
  </div>
</template>

<script>
import GameCell from "@/components/GameCell";

export default {
  name: "GameBoard",
  props: {
    board: {
      type: Object,
      required: true
    },
  },
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
      expanded: null
    }
  },
}
</script>

<style scoped>
.board {
  --cell-size: 25px;
  --cell-gap: 2px;
  --divider-width: 3px;

  display: grid;
  grid: repeat(9, var(--cell-size)) / repeat(9, var(--cell-size));
  gap: var(--cell-gap);
  justify-content: center;
  perspective: 200px;
}

.board__row-divider {
  content: " ";
  display: block;
  background-color: black;
  height: var(--divider-width);
  width: calc(9 * var(--cell-size) + 8 * var(--cell-gap));
}

.board__column-divider {
  content: " ";
  display: block;
  background-color: black;
  width: var(--divider-width);
  height: calc(9 * var(--cell-size) + 8 * var(--cell-gap));
}

.board__expanded-shadow {
  grid-area: 5 / 9 / auto / auto;
  box-shadow: rgba(0, 0, 0, 0.3) 0px 0px 10px;
  background-color: rgba(0, 0, 0, 0.2);
}
</style>
