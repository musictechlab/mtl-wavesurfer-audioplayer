import { onBeforeUnmount, onMounted, Ref } from 'vue'

export function useClickOutside(elTargetRef: Ref, callback: () => void) {
  if (!elTargetRef) {
    return
  }

  const listener = ($event: Event) => {
    if ($event.target === elTargetRef.value || $event.composedPath()?.includes(elTargetRef.value)) {
      return
    }

    if (typeof callback === 'function') {
      callback()
    }
  }

  onMounted(() => window.addEventListener('click', listener))
  onBeforeUnmount(() => window.removeEventListener('click', listener))

  return {
    listener,
  }
}
