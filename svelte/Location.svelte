<script>
  export let id
</script>

<iframe allowfullscreen
  loading=lazy
  src="https://www.google.com/maps/embed/v1/place?q=place_id:{id}&key=AIzaSyAUU6DgJ-dorKgFb0XMCZ8qACjCRkcXY70"
  title="Google Maps" />

<style>
  iframe {
    border: 0;
    height: min(360px, 100vh);
    min-width: min(360px, calc(100vw - 1.6em));
  }
</style>
