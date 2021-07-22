import { writable } from 'svelte/store'

export function saveable(name, server_side) {
  const data = server_side != null ?
    server_side : JSON.parse(localStorage.getItem(name))

  const { subscribe, set, update } = writable(data)
  return { subscribe, set: data => {
    set(data)
    localStorage.setItem(name, JSON.stringify(data))
  }, update, name }
}
