import { onDestroy } from 'svelte'
import { writable } from 'svelte/store'

export function saveable(name, original = null) {
  let object = writable(original)

  let skip = true
  let unsubscribe = object.subscribe(data => {
    // Don't PUT back the data that we just read
    if (skip)
      return skip = false

    fetch(window.location.pathname + window.location.search, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ [name]: data, time: new Date() }),
    })
  })
  onDestroy(unsubscribe)

  return object
}
