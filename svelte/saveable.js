import { writable } from 'svelte/store'

export function saveable(name, server_side) {
  let secret = name + '_' + document.rsvp_info.secret_id

  const data = server_side != null ?
    server_side : JSON.parse(localStorage.getItem(secret))

  const { subscribe, set, update } = writable(data)
  return { subscribe, set: data => {
    set(data)
    localStorage.setItem(secret, JSON.stringify(data))
  }, update, secret }
}
