# MusicTech Lab Audio Player

## Used technologies and libraries

- [Vue.js](https://vuejs.org/) - main framework
- [Nuxt.js](https://nuxtjs.org/) - SSR framework for Vue
- [WaveSurfer.js](https://wavesurfer-js.org/) - library for drawing spectrum and dealing with audio
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

---

## Tools

- [Prettier](https://prettier.io/) - code formatter
- [ESLint](https://eslint.org/) - linter
- [Yarn](https://yarnpkg.com/) - packages manager

---

## Project structure

├── assets  
├───── css - global styles and Tailwind configuration  
├───── icons - SVG icons used in app  
├── atoms  
├── molecules  
├── layouts - Nuxt 2 layouts used in application  
├── organisms  
├── pages  
├── static - static resources  
├ nuxt.config.js - SSR configuration file  
├ tailwind.config.js - Tailwind CSS extension and configuration file

---

## Components documentation

All the components are reusable and based on [Atomic Design](https://vuedose.tips/how-to-structure-a-vue-js-app-using-atomic-design-and-tailwindcss/).

### Atoms

#### AtomIcon.vue - component used for rendering SVG icon

All available icons should be added to `/icons/index.ts` file with specific name. If we try to render an icon that name is not included in this file, the icon will not be rendered.

```html
<atom-icon name="stems" />
```

- Inputs:
- - `name` - the name of icon that should be rendered

### Molecules

#### MoleculeIconButton.vue - component used for rendering button with icon inside

```html
<molecule-icon-button :disabled="isPreviousDisabled" icon="previous" @click="onPreviousButtonClick" />
```

- Inputs:
- - `icon` - the name of icon that should be rendered
- - `disabled` - indicates if button should be disabled or not
- - `small` - indicates if button should be displayed ins small mode
- Outputs:
- - `click` - emitted after clicking on button

#### MoleculeMenu.vue - component used for displaying audio player mobile menu

```html
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
```

- Inputs:
- - `is-playing` - indicates if player is in playing mode
- - `is-previous-disabled` - indicates if previous button should be disabled or not
- - `is-next-disabled` - indicates if next button should be disabled or not
- - `is-shuffle` - indicates if shuffle button should be active or not
- - `hook` - indicates if hook button should be displayed ins small mode
- Outputs:
- - `previous` - emitted after clicking on previous button
- - `next` - emitted after clicking on next button
- - `toggle-shuffle` - emitted after clicking on button for shuffling playlist
- - `add-hook` - emitted after clicking on button for adding hook

#### MoleculeRadioButton.vue - component used for displaying custom radio input

```html
<molecule-radio-button :checked="isRadioButtonChecked" @click="selectStem" />
```

- Inputs:
- - `checked` - indicates if button should be marked as checked or not
- Outputs:
- - `click` - emitted after clicking on radio button

#### MoleculeStemsButton.vue - component used for displaying stems button responsible for showing stems box

```html
<molecule-stems-button disabled="false" stems-title="Stems" @click="toggleStemsVisibility" />
```

- Inputs:
- - `stems-title` - placeholder for button title
- - `disabled` - indicates if button should be disabled or not
- Outputs:
- - `click` - emitted after clicking on radio button

#### MoleculeTrackInfo.vue - component used for displaying information about current track

```html
<molecule-track-info :band-name="bandName" :track-name="trackName" />
```

- Inputs:
- - `band-name` - placeholder for the name of the track band
- - `track-name` - placeholder for the name of the track

#### MoleculeTrackProgress.vue - component used for displaying the progress and duration of the current track

```html
<molecule-track-progress
  v-if="waveSurfer"
  :progress="() => waveSurfer.getCurrentTime()"
  :duration="() => waveSurfer.getDuration()"
  :is-loading="isLoading"
/>
```

- Inputs:
- - `progress` - input for method for getting the current track time
- - `duration` - input for method for getting the current track duration
- - `is-playing` - indicates if the current track is in play mode

#### MoleculeVolumeControl.vue - component used for managing the audio player volume

```html
<molecule-volume-control v-if="waveSurfer" :value="currentVolume" @volume-change="onVolumeChange" />
```

- Inputs:
- - `value` - placeholder for the current value of volume
- Outputs:
- - `volume-change` - emitted after changing the volume

### Organisms

#### OrganismAudioControls.vue - component used for displaying audio player menu

```html
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
```

- Inputs:
- - `is-playing` - indicates if player is in playing mode
- - `is-previous-disabled` - indicates if previous button should be disabled or not
- - `is-next-disabled` - indicates if next button should be disabled or not
- - `is-shuffle` - indicates if shuffle button should be active or not
- Outputs:
- - `previous` - emitted after clicking on previous button
- - `next` - emitted after clicking on next button
- - `toggle-shuffle` - emitted after clicking on the button for shuffling playlist
- - `toggle-play` - emitted after clicking on the play/pause button

#### OrganismStemsControls.vue - component used for displaying and managing stems

```html
<organism-stems-controls
  v-if="areStemsVisible"
  :stems="stems"
  :progress="() => waveSurfer.getCurrentTime()"
  :max-width="stemsContainerMaxWidth"
  :volume="currentVolume"
  @select-stem="onSelectStem"
  @stem-time-update="onStemTimeUpdate"
/>
```

- Inputs:
- - `stems` - list of stems (each object should contain `name` and `icon` property)
- - `progress` - input for method for getting the current track time
- - `max-width` - indicates the maximum width of the spectrum container
- - `volume` - the current value of volume
- Outputs:
- - `select-stem` - emitted after stem selection. Contains 2 objects: the selected stem and the stem WaveSurfer
- - `stem-time-update` - emitted continuously if stem is playing. Notify the main WaveSurfer object to update it's progress

#### OrganismHookControls.vue - component used for displaying hooks menu and managing them

```html
<organism-hook-controls
  v-if="hook"
  :is-playing-loop="isPlayingLoopHook"
  @share="shareHook()"
  @download="downloadHook()"
  @play-loop="playLoopHook()"
  @remove="removeHook()"
/>
```

- Inputs:
- - `is-playing-loop` - indicates if the loop mode is active
- Outputs:
- - `share` - emitted after clicking `share` button
- - `download` - emitted after clicking `download` button
- - `play-loop` - emitted after clicking button for turning on/off loop mode
- - `remove` - emitted after clicking `remove` button

#### OrganismAudioPlayer.vue - the main component used for displaying the whole player.

Inside it contains all listed above components. It is responsible for generating spectrum and grouping all the functionalities of the audio player

```html
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
```

- Inputs:
- - `track-details` - object that contains information about the track URL and the spectrum data
- - `is-previous-disabled` - indicates if previous button should be disabled or not
- - `is-next-disabled` - indicates if next button should be disabled or not
- - `is-shuffle` - indicates if shuffle button should be active or not
- - `band-name` - placeholder for the name of the track band
- - `track-name` - placeholder for the name of the track
- - `stems` - list of stems (each object should contain `name` and `icon` property)
- Outputs:
- - `share-hook` - emitted after clicking `share` button in the hook menu
- - `download-hook` - emitted after clicking `download` button in the hook menu
- - `wave-surfer-init` - emitted after initializing of the new WaveSurfer object. It is done after playing new track
- - `previous` - emitted after clicking on previous button
- - `next` - emitted after clicking on next button
- - `toggle-shuffle` - emitted after clicking on the button for shuffling playlist

---

## Local environment setup

- Install NVM (Node version Manager): [for Mac or Ubuntu](https://github.com/nvm-sh/nvm) or [for Windows](https://github.com/coreybutler/nvm-windows)
- Run command `nvm install 22.9.0` and `nvm use`
- Install [Yarn](https://yarnpkg.com/)
- Install `node_modules` with command `yarn install`
- Run project with `yarn dev`
- App with hot reload on `http://localhost:3000`

---

## Lints and fixes files

- Run command `yarn lint`

## S3 Policy
https://eu-central-1.console.aws.amazon.com/s3/buckets/soundlab-poc?region=eu-central-1&bucketType=general&tab=permissions