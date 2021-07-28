<script>
  export let name
  export let result
</script>

<div class="prompt">
  <slot></slot>
  <span>
    <input type=radio id="{name}-toggle-1" class="toggle-1" {name} value={1}
      required bind:group={result}>
    <label for="{name}-toggle-1" class="pseudo button">Yes</label>

    <input type=radio id="{name}-toggle-0" class="toggle-0" {name} value={0}
      required bind:group={result}>
    <label for="{name}-toggle-0" class="pseudo button">No</label>
  </span>
</div>

<style>
  label {
    border: 1px solid #aaaaaa;
  }

  input[type="radio"]:checked + label {
    color: #ffffff;
  }

  input.toggle-1:checked + label {
    background: #2ecc40;
    border: 1px solid #2ecc40;
  }

  input.toggle-0:checked + label {
    background: #ff4136;
    border: 1px solid #ff4136;
  }
</style>
