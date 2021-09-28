<script>
  export let vaxx_info = {}

  let upload_form;
  let view;

  if (vaxx_info.on_server && vaxx_info.on_server.endsWith('.pdf')) {
    const PDFJS = window['pdfjs-dist/build/pdf']
    PDFJS.GlobalWorkerOptions.workerSrc =
      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js'

    PDFJS.getDocument(vaxx_info.on_server).promise.then(function(pdf) {
      pdf.getPage(1).then(function(page) {
        const viewport = page.getViewport({ scale:
          view.parentElement.clientWidth / page.getViewport({ scale: 1 }).width
        });
        const outputScale = window.devicePixelRatio || 1;

        const context = view.getContext('2d');

        view.width = Math.floor(viewport.width * outputScale);
        view.height = Math.floor(viewport.height * outputScale);
        view.style.width = Math.floor(viewport.width) + "px";
        view.style.height =  Math.floor(viewport.height) + "px";

        const transform = outputScale !== 1
          ? [outputScale, 0, 0, outputScale, 0, 0]
          : null;

        page.render({
          canvasContext: context, transform: transform, viewport: viewport
        })
      })
    })
  }
</script>

<main>
<header>
  <h1>Vaccination Card for {vaxx_info.name}</h1>

  {#if vaxx_info.status != 'Upload succeeded' }
    <p>Please upload your proof of vaccination. Otherwise, you <strong>must</strong> render it in person at the wedding, or we <strong>will</strong> deny you entrance into the event.</p>
  {/if}
</header>

{#if vaxx_info.on_server}
  <article class=card>
  {#if vaxx_info.on_server && vaxx_info.on_server.endsWith('.pdf')}
    <canvas bind:this={view} style="height: 100%;">Uploaded File</canvas>
  {:else}
    <img alt="Uploaded File" src={vaxx_info.on_server}>
  {/if}
  </article>
{/if}

{#if vaxx_info.error}
  <p class="button error status" style="display: block;">{vaxx_info.error}</p>
{/if}

<footer>
  <a class="pseudo button help" href="mailto:ktchen14@gmail.com,melanieplageman@gmail.com?subject=Help with Vaccination Card">Help</a>
  {#if vaxx_info.status == 'Upload succeeded' }
    <p class="button success status">Vaccination documentation uploaded</p>
  {:else}
    <form enctype="multipart/form-data" method=POST bind:this={upload_form}>
      <label class="upload pseudo button">
        Upload
        <input type=file name=file accept="image/*,.pdf" on:change={upload_form.submit()}>
      </label>
    </form>
  {/if}
</footer>

</main>

<style>
header > h1 {
  text-align: center;
}

canvas, img[alt="Uploaded File"] {
  max-width: 100%;
}

footer {
  display: flex;
  align-content: flex-start;
  align-items: baseline;
  flex-wrap: wrap;
  justify-content: space-between;
}

.help {
  background-color: #ff851b;
  color: #ffffff;
}

.help:hover {
  box-shadow: inset 0 0 0 99em rgba(255, 255, 255, 0.2);
  text-decoration: none;
}

.status {
  cursor: auto;
  -khtml-user-select: auto;
  -moz-user-select: auto;
  -ms-user-select: auto;
  -webkit-user-select: auto;
  user-select: auto;
}

.status:hover {
  box-shadow: none;
}

.upload {
  background-color: #0074d9;
  color: #ffffff;
}

.upload input[type="file"] {
  display: none;
}
</style>
