<template>
  <main class="p-32">
    <h1 class="heading mb-32">MusicTech Lab | Audio Player</h1>
    <div class="mb-32">
      <div
        v-for="track in tracks"
        :key="track.id"
        class="flex justify-between items-center p-16 mb-16 border-1 border-black w-full cursor-pointer"
        @click="selectTrack(track)"
      >
        <div class="flex items-center">
          <img v-if="track.thumbnail" :src="track.thumbnail" class="w-60 h-60 mr-32" alt="" />
          <p
            :class="[
              'body1',
              currentTrack &&
                currentTrack.mainFile &&
                currentTrack.mainFile.file_upload === track.mainFile.file_upload &&
                'text-violet',
            ]"
          >
            <strong>{{ track.title }}</strong>
            <br />
            <span>{{ track.music_store_author ? track.music_store_author.legal_name : '' }}</span>
          </p>
        </div>
        <molecule-icon-button
          :icon="
            currentTrack &&
            currentTrack.mainFile &&
            currentTrack.mainFile.file_upload === track.mainFile.file_upload &&
            isPlaying
              ? 'pause'
              : 'play'
          "
        />
      </div>
    </div>

    <div class="fixed md:relative bottom-0 left-0 w-full bg-white z-50">
      <client-only>
        <organism-audio-player
          v-if="currentTrack && currentTrack.mainFile"
          :track-details="currentTrack.mainFile"
          :is-previous-disabled="isStartOfTrackList"
          :is-next-disabled="isEndOfTrackList"
          :band-name="currentTrack.music_store_author ? currentTrack.music_store_author.legal_name : null"
          :track-name="currentTrack.title"
          :stems="currentTrack.stems"
          @toggle-shuffle="onShuffle($event)"
          @share-hook="onShareHook"
          @download-hook="onDownloadHook"
          @previous="onPreviousTrack"
          @next="onNextTrack"
          @wave-surfer-init="onWaveSurferInit"
        />
      </client-only>
    </div>
  </main>
</template>

<script lang="ts">
import { defineComponent, computed, ref, Ref, useFetch } from '@nuxtjs/composition-api'
import MoleculeIconButton from '~/molecules/MoleculeIconButton.vue'
import OrganismAudioPlayer from '~/organisms/OrganismAudioPlayer.vue'

const TRACKS_QUERY = `query MyQuery {
  music_store_music {
    id
    title
    music_store_musicfiles {
      file_name
      file_type
      bpm
      vocal_type
      file_upload
      waveform
      waveform_image
    }
    music_store_author {
      legal_name
      pseudonym
    }
  }
}`
const RESOURCE_URL = 'https://mt-audioplayer.s3.amazonaws.com/'
const DEFAULT_STEM_NAME = 'Other'
const DEFAULT_STEM_ICON = 'melody'
const STEMS_NAME_MAP = {
  STEM_INSTRUMENTS: 'Instrumental',
  STEM_DRUMS: 'Drums',
  STEM_BAS: 'Bas',
  STEM_KEYS: 'Keyboard',
  STEM_GUITAR: 'Guitar',
}
const STEMS_ICON_MAP = {
  STEM_INSTRUMENTS: 'instrumental',
  STEM_DRUMS: 'drums',
  STEM_BAS: 'guitar',
  STEM_KEYS: 'instrumental',
  STEM_GUITAR: 'guitar',
}

type FileType = 'STEM_INSTRUMENTS' | 'STEM_DRUMS' | 'STEM_BAS' | 'STEM_KEYS' | 'STEM_GUITAR'

type Track = {
  id: string
  title: string
  music_store_musicfiles: Array<{
    file_name: string
    file_type: string
    bpm: number
    vocal_type: string
    file_upload: string
    waveform: string
    waveform_image: string
  }>
  music_store_author: {
    legal_name: string
    pseudonym: string
  }
  thumbnail?: string
  mainFile?: {
    file_upload: string
  }
  stems: Array<{
    file_type: FileType
    name: string
    icon: string
  }>
}

export default defineComponent({
  name: 'IndexPage',
  components: { MoleculeIconButton, OrganismAudioPlayer },
  setup() {
    const currentTrack: Ref<Track | null> = ref(null)
    const currentWaveSurfer: Ref<> = ref(null)
    const isShuffle = ref(false)
    const isPlaying = ref(false)
    const tracks: Ref<Array<Track>> = ref([])
    const isStartOfTrackList = computed(() => tracks.value.indexOf(currentTrack.value) === 0)
    const isEndOfTrackList = computed(() => tracks.value.indexOf(currentTrack.value) === tracks.value.length - 1)

    useFetch(async () => {
      const response = await fetch('http://mtl-audioplayer-api.MusicTech Lab.io/v1/graphql', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'x-hasura-admin-secret': 'mtl-audioplayer',
        },
        body: JSON.stringify({
          query: TRACKS_QUERY,
        }),
      })
      const data = (await response.json()).data

      if (data && data.music_store_music) {
        tracks.value = data.music_store_music.map((track: Track) => {
          const musicFiles = track.music_store_musicfiles.map((file) => ({
            ...file,
            file_upload: `${RESOURCE_URL}${file.file_upload}`,
          }))
          const coverFile = musicFiles.find((file) => file.file_type === 'COVER')
          const mainVocalFile = musicFiles.find((file) => file.file_type === 'VOCAL')
          const mainInstrumentalFile = musicFiles.find((file) => file.file_type === 'INSTRUMENTAL')
          const stems = musicFiles
            .filter((file) => file.file_type.includes('STEM'))
            .map((stem: { file_type: FileType }) => ({
              ...stem,
              name: STEMS_NAME_MAP[stem.file_type] || DEFAULT_STEM_NAME,
              icon: STEMS_ICON_MAP[stem.file_type] || DEFAULT_STEM_ICON,
            }))

          return {
            ...track,
            music_store_musicfiles: musicFiles,
            thumbnail: coverFile ? coverFile.file_upload : null,
            mainFile: mainVocalFile || mainInstrumentalFile,
            stems,
          }
        }) as Array<Track>
      }
    })

    const onPreviousTrack = () => {
      if (isShuffle.value) {
        getRandomTrack()
      } else {
        const previousIndex = tracks.value.indexOf(currentTrack.value) - 1

        currentTrack.value = tracks.value[previousIndex]
      }
    }

    const onNextTrack = () => {
      if (isShuffle.value) {
        getRandomTrack()
      } else {
        const nextIndex = tracks.value.indexOf(currentTrack.value) + 1

        currentTrack.value = tracks.value[nextIndex]
      }
    }

    const getRandomTrack = () => {
      const trackIndex = Math.floor(Math.random() * tracks.value.length)

      currentTrack.value = tracks.value[trackIndex]
    }

    const onShareHook = ($event) => {
      console.log('SHARE HOOK', $event)
    }

    const onDownloadHook = ($event) => {
      console.log('DOWNLOAD HOOK', $event)
    }

    const onShuffle = (shuffle: boolean) => {
      isShuffle.value = shuffle
    }

    const selectTrack = (track) => {
      if (currentTrack.value?.mainFile?.file_upload === track?.mainFile?.file_upload && currentWaveSurfer.value) {
        if (currentWaveSurfer.value?.isPlaying()) {
          currentWaveSurfer.value?.pause()
        } else {
          currentWaveSurfer.value?.play()
        }
        isPlaying.value = currentWaveSurfer.value?.isPlaying()
      } else {
        currentTrack.value = track
        isPlaying.value = true
      }
    }

    const onWaveSurferInit = (waveSurfer) => {
      currentWaveSurfer.value = waveSurfer
    }

    return {
      currentTrack,
      tracks,
      isStartOfTrackList,
      isEndOfTrackList,
      isPlaying,
      selectTrack,
      onShuffle,
      onPreviousTrack,
      onNextTrack,
      onShareHook,
      onDownloadHook,
      onWaveSurferInit,
    }
  },
  head() {
    return {
      link: [
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Sora:wght@400;600&display=swap',
        },
      ],
      script: [
        {
          src: 'https://unpkg.com/wavesurfer.js',
        },
        {
          src: 'https://unpkg.com/wavesurfer.js/dist/plugin/wavesurfer.regions.min.js',
        },
      ],
    }
  },
})
</script>
