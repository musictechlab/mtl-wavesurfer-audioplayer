<template>
  <div class="flex items-center justify-center mr-8 md:mr-16 body2 md:body-1 w-80 md:w-90">
    <template v-if="isLoading">0:00 / 0:00</template>
    <template v-else>{{ currentTime }} / {{ currentDuration }}</template>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, ref } from 'vue'

export default defineComponent({
  name: 'MoleculeTrackProgress',
  props: {
    progress: {
      type: Function,
      default: () => 0,
    },
    duration: {
      type: Function,
      default: () => 0,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const interval = ref(0)
    const currentTime = ref('0:00')
    const currentDuration = ref('0:00')

    onMounted(() => {
      addInterval()
    })

    onUnmounted(() => {
      deleteInterval()
    })

    const addInterval = () => {
      interval.value = setInterval(() => {
        if (props.progress) {
          currentTime.value = formatTime(Math.floor(isNaN(props.progress()) ? 0 : props.progress()))
          currentDuration.value = formatTime(Math.floor(isNaN(props.duration()) ? 0 : props.duration()))
        }
      }, 500) as unknown as number
    }

    const deleteInterval = () => {
      if (interval.value) {
        clearInterval(interval.value)
      }
    }

    const formatTime = (seconds: number): string => {
      const minutes = Math.floor(seconds / 60)
      const restSeconds = seconds - minutes * 60
      const displayedSeconds = restSeconds < 10 ? `0${restSeconds}` : `${restSeconds}`

      return `${minutes}:${displayedSeconds}`
    }

    return {
      currentTime,
      currentDuration,
    }
  },
})
</script>
