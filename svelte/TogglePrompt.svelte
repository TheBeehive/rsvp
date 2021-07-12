<script>
  import Toggle from "./Toggle.svelte"

  export let name
  export let result
</script>

<div class="prompt">
  <slot></slot>
  <Toggle {name} bind:result />
</div>

<style>
  .prompt {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    justify-content: space-between;
  }
</style>
