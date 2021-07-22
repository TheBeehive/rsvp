import RSVP from './RSVP.svelte';

const rsvp = new RSVP({
  target: document.body,
  props: { 'rsvp_info': document.rsvp_info },
});

export default rsvp;
