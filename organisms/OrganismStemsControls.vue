<template>
  <div
    ref="stemsControl"
    class="flex flex-wrap border-x-0 md:border-x-1 border-1 border-black absolute bg-white bottom-full z-50 right-stems-r"
  >
    <div
      v-for="(stem, index) in stems"
      :key="`stem_${index}`"
      class="h-40 w-full flex border-b-1 border-black last-of-type:border-b-0 pl-8 md:pl-0"
    >
      <div :id="`stem-wavesurfer-${index}`" class="flex-1" :style="{ maxWidth: `${maxWidth || 600}px` }"></div>
      <div class="max-w-64 md:max-w-[113px] w-full p-8 border-l-1 border-black w-full flex items-center">
        <atom-icon :name="stem.icon" class="w-20 h-20 mr-8 md:mr-4" />
        <span class="hidden md:block body4 text-ellipsis overflow-hidden flex-1 pr-4">{{ stem.name }}</span>
        <molecule-radio-button
          :checked="selectedStem && selectedStem.file_type === stem.file_type"
          @click="selectStem(stem, index)"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, ref, Ref } from 'vue'
import AtomIcon from '@/atoms/AtomIcon.vue'
import MoleculeRadioButton from '@/molecules/MoleculeRadioButton.vue'

export default defineComponent({
  name: 'OrganismStemsControls',
  components: {
    AtomIcon,
    MoleculeRadioButton,
  },
  props: {
    stems: {
      type: Array,
      default: () => [],
    },
    progress: {
      type: Function,
      default: () => 0,
    },
    maxWidth: {
      type: Number,
      default: 600,
    },
    volume: {
      type: Number,
      default: 100,
    },
  },
  emits: ['stem-time-update', 'select-stem'],
  setup(props, { emit }) {
    const stemWaveSurfers: Ref<Array<WaveSurfer>> = ref([])
    const interval = ref(0)
    const selectedStem: Ref<Stem | null> = ref(null)
    const selectedStemIndex: Ref<number> = ref(-1)
    const selectedStemWaveSurfer: Ref<WaveSurfer | null> = ref(null)

    onMounted(() => {
      if (process.browser && window.WaveSurfer) {
        addInterval()
        initStemsWaveSurfers()
      }
    })

    onUnmounted(() => {
      deleteInterval()
    })

    const initStemsWaveSurfers = () => {
      if (props.stems?.length) {
        props.stems.forEach((stem: Stem, index: number) => {
          const stemWaveSurfer = window.WaveSurfer.create({
            container: `#stem-wavesurfer-${index}`,
            backend: 'MediaElement',
            height: 36,
            width: 600,
            progressColor: '#000000',
            waveColor: '#b2b2b2',
            responsive: true,
            cursorWidth: 0,
            barHeight: 1,
            normalize: true,
          })
          stemWaveSurfer.load(stem.file_upload, stem.waveform.data, 'auto')
          stemWaveSurfers.value.push(stemWaveSurfer)
        })
      }
    }

    const addInterval = () => {
      interval.value = setInterval(() => {
        if (props.progress) {
          if (selectedStemWaveSurfer.value) {
            updateWaveSurfersTimeInternally()
          } else {
            updateWaveSurfersTime()
          }
        }
      }, 200) as unknown as number
    }

    const deleteInterval = () => {
      if (interval.value) {
        clearInterval(interval.value)
      }
    }

    const updateWaveSurfersTime = () => {
      stemWaveSurfers.value.forEach((waveSurfer: WaveSurfer) => {
        const offset = props.progress() - waveSurfer.getCurrentTime()
        waveSurfer.skip(offset)
      })
    }

    const updateWaveSurfersTimeInternally = () => {
      emit('stem-time-update', selectedStemWaveSurfer.value?.getCurrentTime())

      stemWaveSurfers.value.forEach((waveSurfer: WaveSurfer, index: number) => {
        if (index !== selectedStemIndex.value) {
          const offset = selectedStemWaveSurfer.value?.getCurrentTime() - waveSurfer.getCurrentTime()
          waveSurfer.skip(offset)
        }
      })
    }

    const selectStem = (stem: Stem, index: number) => {
      selectedStemWaveSurfer.value?.pause()

      if (selectedStem.value?.file_type === stem.file_type) {
        selectedStem.value = null
        selectedStemWaveSurfer.value = null
        selectedStemIndex.value = -1
      } else {
        selectedStem.value = stem
        selectedStemWaveSurfer.value = stemWaveSurfers.value[index]
        selectedStemIndex.value = index
        selectedStemWaveSurfer.value.setVolume(props.volume / 100)
        selectedStemWaveSurfer.value.play()
      }

      emit('select-stem', selectedStem.value, selectedStemWaveSurfer.value)
    }

    return {
      selectedStem,
      selectStem,
    }
  },
})
</script>
