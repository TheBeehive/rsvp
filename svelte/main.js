import RSVP from './RSVP.svelte';
import IndeterminateRSVP from './IndeterminateRSVP.svelte';

const component_type =
  document.rsvp_info.type == 'indeterminate_rsvp' ? IndeterminateRSVP : RSVP
const rsvp = new component_type({
  target: document.body,
  props: { 'rsvp_info': document.rsvp_info },
})

export default rsvp;
