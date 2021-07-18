import { writable } from 'svelte/store'

export function saveable(name) {
  const data = JSON.parse(localStorage.getItem(name))
  const { subscribe, set, update } = writable(data)
  return { subscribe, set: data => {
    set(data)
    localStorage.setItem(name, JSON.stringify(data))
  }, update, name }
}
