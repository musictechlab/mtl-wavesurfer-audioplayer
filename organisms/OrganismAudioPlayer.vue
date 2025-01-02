<template>
  <div
    class="border-0 md:border-1 border-white pt-68 md:pt-16 p-8 md:p-16 w-full flex flex-wrap items-center relative justify-between md:justify-unset"
  >
    <div class="block md:hidden h-4 w-full bg-black absolute left-0 top-56"></div>
    <div class="flex">
      <organism-audio-controls
        :is-playing="isPlaying"
        :is-previous-disabled="isPreviousDisabled"
        :is-next-disabled="isNextDisabled"
        :is-shuffle="isShuffleMode"
        @toggle-play="togglePlay"
        @previous="previousTrack()"
        @next="nextTrack()"
        @toggle-shuffle="onToggleShuffle"
      />
      <molecule-track-info :band-name="bandName" :track-name="trackName" />
      <molecule-track-progress
        v-if="waveSurfer"
        :progress="() => waveSurfer.getCurrentTime()"
        :duration="() => waveSurfer.getDuration()"
        :is-loading="isLoading"
      />
    </div>
    <organism-stems-controls
      v-if="areStemsVisible"
      :stems="stems"
      :progress="() => waveSurfer.getCurrentTime()"
      :max-width="stemsContainerMaxWidth"
      :style="{ left: `${stemsContainerLeftPosition}px` }"
      :volume="currentVolume"
      @select-stem="onSelectStem"
      @stem-time-update="onStemTimeUpdate"
    />
    <div
      id="mtl-wavesurfer-audioplayer"
      class="flex-1 absolute top-8 left-8 right-8 md:top-0 md:left-0 md:right-0 md:relative"
    >
      <organism-hook-controls
        v-if="hook"
        :style="{ left: `${hookLeftPosition}px` }"
        :is-playing-loop="isPlayingLoopHook"
        @share="shareHook()"
        @download="downloadHook()"
        @play-loop="playLoopHook()"
        @remove="removeHook()"
      />
    </div>
    <div class="flex">
      <molecule-stems-button v-if="stems && stems.length" @click="toggleStemsVisibility()" />
      <molecule-icon-button v-if="false" icon="hook" class="hidden md:flex" :disabled="!!hook" @click="addHook" />
      <molecule-volume-control v-if="waveSurfer" :value="currentVolume" @volume-change="onVolumeChange" />
      <molecule-menu
        :is-playing="isPlaying"
        :is-previous-disabled="isPreviousDisabled"
        :is-next-disabled="isNextDisabled"
        :is-shuffle="isShuffleMode"
        :hook="hook"
        @previous="previousTrack()"
        @next="nextTrack()"
        @toggle-shuffle="onToggleShuffle"
        @add-hook="addHook"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref, watch, Ref } from 'vue'
import MoleculeTrackProgress from '@/molecules/MoleculeTrackProgress.vue'
import OrganismAudioControls from '@/organisms/OrganismAudioControls.vue'
import MoleculeTrackInfo from '@/molecules/MoleculeTrackInfo.vue'
import MoleculeVolumeControl from '@/molecules/MoleculeVolumeControl.vue'
import OrganismHookControls from '@/organisms/OrganismHookControls.vue'
import MoleculeStemsButton from '@/molecules/MoleculeStemsButton.vue'
import OrganismStemsControls from '@/organisms/OrganismStemsControls.vue'
import MoleculeIconButton from '@/molecules/MoleculeIconButton.vue'
import MoleculeMenu from '@/molecules/MoleculeMenu.vue'
import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions.esm.js'


const regions = RegionsPlugin.create()

export interface IWaveSurfer {
  isPlaying(): boolean
  on(event: string, callback?): void
  getVolume(): number
  setVolume(volume: number): void
  play(start?: number): void
  pause(): void
  unAll(): void
  playPause(): void
  stop(): void
  load(url: string, peaks?, preload?: string): void
  getCurrentTime(): number
  getDuration(): number
  addRegion(options)
  clearRegions(): void
  skip(time: number): void
  exportPCM(): void
  regions
}

export declare interface WaveSurferHook {
  loop: boolean
  play(): void
  playLoop(): void
  remove(): void
  onDrag(timeInSeconds: number): void
  onResize(timeInSeconds: number, place: string): void
}

export interface HookData {
  start: number
  end: number
}

declare global {
  interface Window {
    WaveSurfer
    RegionsPlugin
  }
}

export default defineComponent({
  name: 'OrganismAudioPlayer',
  ssr: false,
  components: {
    MoleculeMenu,
    OrganismAudioControls,
    OrganismHookControls,
    OrganismStemsControls,
    MoleculeTrackProgress,
    MoleculeTrackInfo,
    MoleculeVolumeControl,
    MoleculeStemsButton,
    MoleculeIconButton,
  },
  props: {
    trackDetails: {
      type: Object,
      required: true,
    },
    isPreviousDisabled: {
      type: Boolean,
      required: false,
    },
    isNextDisabled: {
      type: Boolean,
      required: false,
    },
    isShuffle: {
      type: Boolean,
      required: false,
      default: false,
    },
    bandName: {
      type: String,
      default: '',
    },
    trackName: {
      type: String,
      required: true,
    },
    stems: {
      type: Array,
      default: null,
    },
    stemsTitle: {
      type: String,
      default: 'Stems',
    },
    volume: {
      type: Number,
      default: 100,
    },
  },
  emits: ['next', 'previous', 'toggle-shuffle', 'share-hook', 'download-hook', 'wave-surfer-init'],
  setup(props, { emit }) {
    const volumeMultiplyFactor = 100
    const waveSurfer: Ref<IWaveSurfer | null> = ref(null)
    const stemWaveSurfer: Ref<IWaveSurfer | null> = ref(null)
    const hook: Ref<WaveSurferHook | null> = ref(null)
    const hookData: Ref<HookData | null> = ref(null)
    const isPlayingLoopHook = ref(false)
    const isShuffleMode = ref(props.isShuffle)
    const isPlaying = ref(false)
    const isLoading = ref(false)
    const areStemsVisible = ref(false)
    const hookLeftPosition = ref(0)
    const currentVolume = ref(
      waveSurfer.value ? waveSurfer.value?.getVolume() * volumeMultiplyFactor : volumeMultiplyFactor,
    )
    const currentTrack = computed(() => props.trackDetails)
    const propsVolume = computed(() => props.volume)
    const currentTime = computed(() => waveSurfer.value?.getCurrentTime())
    const stemsContainerLeftPosition = ref(0)
    const stemsContainerMaxWidth = ref(0)

    onMounted(() => {
      if (process.browser && window.WaveSurfer) {
        initWaveSurfer()
      }
    })

    watch(currentTrack, () => {
      waveSurfer.value?.stop()
      waveSurfer.value?.load(props.trackDetails.file_upload, props.trackDetails.waveform.data, 'auto')
    })

    watch(propsVolume, () => onVolumeChange(props.volume))

    const initWaveSurfer = () => {
      waveSurfer.value = window.WaveSurfer.create({
        container: '#mtl-wavesurfer-audioplayer',
        backend: 'MediaElement',
        height: 40,
        width: 600,
        progressColor: '#000000',
        waveColor: '#b2b2b2',
        responsive: true,
        cursorWidth: 0,
        barHeight: 1,
        normalize: true,
        plugins: [regions],
      })
      waveSurfer.value?.on('play', () => (isPlaying.value = true))
      waveSurfer.value?.on('pause', () => (isPlaying.value = stemWaveSurfer.value?.isPlaying() || false))
      waveSurfer.value?.on('finish', () => {
        areStemsVisible.value = false
        emit('next')
      })
      waveSurfer.value?.on('loading', (progress: number) => (isLoading.value = progress < 100))
      waveSurfer.value?.on('volume', (volume: number) => (currentVolume.value = volume * volumeMultiplyFactor))
      waveSurfer.value?.on('region-updated', ($event: HookData) => {
        updateHookControlsPosition()
        updateHookData($event.start, $event.end)
      })
      waveSurfer.value?.on('ready', () => {
        setTimeout(() => waveSurfer.value?.play(), 0)
        removeHook()
      })
      emit('wave-surfer-init', waveSurfer.value)

      waveSurfer.value?.load(props.trackDetails.file_upload, props.trackDetails.waveform.data, 'auto')
    }

    const onVolumeChange = (volume: number) => {
      const newVolume = volume / volumeMultiplyFactor

      waveSurfer.value?.setVolume(newVolume)
      stemWaveSurfer.value?.setVolume(newVolume)
    }

    const addHook = () => {
      if (!hook.value) {
        const start = waveSurfer.value?.getCurrentTime() as number
        const startOffset = start + 15
        const duration = waveSurfer.value?.getDuration() as number
        const end = Math.min(startOffset, duration)

        hook.value = waveSurfer.value?.addRegion({
          color: 'rgba(150, 150, 150, 0.7)',
          start,
          end,
        }) as WaveSurferHook
        waveSurfer.value?.stop()
        hook.value?.play()
        updateHookData(start, end)
        updateHookControlsPosition()
      }
    }

    const updateHookControlsPosition = () => {
      const regionElement: HTMLElement | null = document.querySelector('.wavesurfer-region')

      if (regionElement) {
        hookLeftPosition.value = regionElement.offsetLeft
      }
    }

    const updateHookData = (start: number, end: number) => {
      hookData.value = { start, end } as HookData
    }

    const removeHook = () => {
      hook.value?.remove()
      hook.value = null
      hookData.value = null
    }

    const shareHook = () => {
      if (hookData.value) {
        emit('share-hook', {
          url: props.trackDetails.file_upload,
          ...hookData.value,
        } as HookData)
      }
    }

    const downloadHook = () => {
      if (hookData.value) {
        emit('download-hook', {
          url: props.trackDetails.file_upload,
          ...hookData.value,
        } as HookData)
      }
    }

    const playLoopHook = () => {
      if (hook.value) {
        isPlayingLoopHook.value = !isPlayingLoopHook.value

        if (isPlayingLoopHook.value) {
          hook.value.playLoop()
        } else {
          hook.value.loop = false
        }
      }
    }

    const onToggleShuffle = () => {
      isShuffleMode.value = !isShuffleMode.value
      emit('toggle-shuffle', isShuffleMode.value)
    }

    const onSelectStem = (stem, stemSurfer: IWaveSurfer | null) => {
      if (stem) {
        waveSurfer.value?.pause()
        stemWaveSurfer.value = stemSurfer
        addStemWaveSurferListeners()
        stemWaveSurfer.value?.play()
      } else {
        stemWaveSurfer.value?.unAll()
        stemWaveSurfer.value = null
        waveSurfer.value?.play()
      }
    }

    const addStemWaveSurferListeners = () => {
      if (stemWaveSurfer.value) {
        stemWaveSurfer.value?.on('play', () => (isPlaying.value = true))
        stemWaveSurfer.value?.on('pause', () => (isPlaying.value = false))
      }
    }

    const previousTrack = () => {
      areStemsVisible.value = false
      emit('previous')
    }

    const nextTrack = () => {
      areStemsVisible.value = false
      emit('next')
    }

    const toggleStemsVisibility = () => {
      if (areStemsVisible.value) {
        onSelectStem(null, null)
      }

      if (typeof document !== 'undefined') {
        stemsContainerLeftPosition.value =
          window.innerWidth < 768 ? 0 : (document.getElementById('mtl-wavesurfer-audioplayer')?.offsetLeft as number) || 0
        stemsContainerMaxWidth.value = document.getElementById('mtl-wavesurfer-audioplayer')?.offsetWidth || 0
      }
      areStemsVisible.value = !areStemsVisible.value
    }

    const onStemTimeUpdate = (time: number) => {
      const offset = time - (waveSurfer.value?.getCurrentTime() || 0)
      waveSurfer.value?.skip(offset)
    }

    const togglePlay = () => {
      if (stemWaveSurfer.value) {
        stemWaveSurfer.value?.playPause()
      } else {
        waveSurfer.value?.playPause()
      }
    }

    return {
      waveSurfer,
      currentTime,
      isPlaying,
      currentVolume,
      isLoading,
      hook,
      hookLeftPosition,
      isPlayingLoopHook,
      isShuffleMode,
      areStemsVisible,
      stemsContainerLeftPosition,
      stemsContainerMaxWidth,
      onToggleShuffle,
      onVolumeChange,
      removeHook,
      shareHook,
      downloadHook,
      playLoopHook,
      onSelectStem,
      addHook,
      previousTrack,
      nextTrack,
      toggleStemsVisibility,
      onStemTimeUpdate,
      togglePlay,
    }
  },
})
</script>
