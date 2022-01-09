<template>
  <div>
    <button v-for="(option, index) in options"
            @click="option.function"
            :key="`menu-option-${index}`">
      {{option.title}}
    </button>
  </div>
</template>

<script>
export default {
  name: "GameMenu",
  data() {
    return {
      options: [
        {
          title: 'New Game',
          function: () => this.$emit('game:new-game')
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
