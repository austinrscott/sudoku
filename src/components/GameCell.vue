<template>
  <div :class="['board__cell', {'board__cell--expanded': expanded}]"
       :style="{gridArea: `${this.cell.row + 1} / ${this.cell.column + 1}`}"
       @click.stop="$emit('cell:expand', cell.id)">
    <span>{{cell.value}}</span>
  </div>
</template>

<script>
export default {
  name: 'GameCell',
  props: {
    cell: {
      type: Object,
      required: true
    },
    id: {
      type: Number,
      required: true
    },
    expanded: {
      type: Boolean,
      required: false,
      default: false
    }
  },
}
</script>

<style scoped>

.board__cell {
  border: 1px solid lightgray;
  background-color: white;

  width: var(--cell-size);
  height: var(--cell-size);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;

  transition: transform 250ms ease;
}

.board__cell-input {
  border: none;
  width: 100%;
}

.board__cell--expanded {
  transform: translateZ(25px);
  z-index: 5;
}

.board__cell:hover {
  background-color: #ffd;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
