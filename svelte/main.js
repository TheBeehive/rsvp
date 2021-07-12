import RSVP from './RSVP.svelte';

const rsvp = new RSVP({
  target: document.body,
  props: {
    name: 'world'
  }
});

export default rsvp;
