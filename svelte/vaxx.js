import Vaxx from './Vaxx.svelte';

const vaxx = new Vaxx({
  target: document.body,
  props: { 'vaxx_info': document.vaxx_info },
})

export default vaxx;
