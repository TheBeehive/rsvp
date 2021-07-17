<script>
  import Toggle from "./Toggle.svelte"
  import TogglePrompt from "./TogglePrompt.svelte"

  const name = "Tony Thomas"
  const plusname = "Brook Osborne"
  const invited_to_brunch = true

  let reception
  let vaxxed
  let mask

  let cocktail
  let cocktail_excess
  let cocktail_excess_number = JSON.parse(localStorage.getItem("cocktail_excess_number"))
  $: localStorage.setItem("cocktail_excess_number", JSON.stringify(cocktail_excess_number))

  let hike
  let mobile = JSON.parse(localStorage.getItem("mobile"))
  $: localStorage.setItem("mobile", JSON.stringify(mobile))

  let brunch
</script>

<main>
<form>
  <h1>RSVP Form</h1>

  <p>Please complete this form and submit it by September 15th. If you need to
  make any changes, this form can be resubmitted until that date.</p>

  <p>Name: {name}</p>

  <p>
    Please review our
    <a href="https://www.hackersgethitched.com/" target=_blank>wedding website</a>
    for the latest information
  </p>

  <h2>Ceremony and Reception</h2>

  <p>The ceremony and reception will take place at the <a href="https://computerhistory.org/" target=_blank>Computer History Museum</a> on Saturday, October 23<sup>rd</sup> at 05:30 PM PDT. The dress code is black tie optional. This will be an adults-only (21+) celebration.</p>

  <iframe height="450" style="border: 0; width: 100%;" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJm7NJkla3j4AR8vR-HWRxgOo&key=AIzaSyAUU6DgJ-dorKgFb0XMCZ8qACjCRkcXY70"></iframe> 

  <TogglePrompt name="reception" bind:result={reception}>
    <p class="question">I will attend the wedding ceremony and reception</p>
  </TogglePrompt>

  {#if reception}
    <p>
      <textarea style="resize: vertical;" placeholder="Please let us know if you have any allergies or dietary restrictions..." />
    </p>

    <TogglePrompt name="vaxxed" bind:result={vaxxed}>
      <p class="question">I am fully vaccinated for COVID-19</p>
    </TogglePrompt>

    {#if vaxxed == 0}
      The <a href="https://www.cdph.ca.gov/" target=_blank>California Department of Public Health</a> requires unvaccinated individuals to wear masks in indoor public settings. Masks may be removed when outside, or when eating or drinking. <a href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/guidance-for-face-coverings.aspx#asterisknew" target=_blank>More Information</a>
      <TogglePrompt name="mask" bind:result={mask}>
        <p class="question">I will wear a mask inside the museum, except when eating or drinking</p>
      </TogglePrompt>

      {#if mask == 0}
        <p>We're sorry but you can't come</p>
      {/if}
    {/if}
  {/if}

  {#if reception && (vaxxed || !vaxxed && mask)}
    <h2>Cocktail Reception</h2>

    <p>You're welcome to attend a cocktail reception at <a href="https://vinolocale.org/" target=_blank>Vino Locale</a> on Friday, October 22<sup>nd</sup>, the day before the wedding, at 07:00 PM PDT.</p>

    <iframe height="450" style="border: 0; width: 100%;" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJ2S5OXzi7j4ARGnV-XOyU-4g&key=AIzaSyAUU6DgJ-dorKgFb0XMCZ8qACjCRkcXY70"></iframe> 

    <TogglePrompt name="cocktail" bind:result={cocktail}>
      <p class="question">I will attend the cocktail reception</p>
    </TogglePrompt>

    {#if cocktail}
      <TogglePrompt name="cocktail_excess" bind:result={cocktail_excess}>
        <p class="question">Will you bring any guests other than {plusname}?</p>
      </TogglePrompt>

      {#if cocktail_excess}
        <p>How many guests will you bring, excluding {plusname}?</p>
        <input type=number name="cocktail_excess_number" bind:value={cocktail_excess_number} required>
      {/if}
    {/if}

    <h2>Wedding Day Hike</h2>

    <p>If there's enough interest, we'll organize a group hike the morning of our wedding.</p>

    <TogglePrompt name="hike" bind:result={hike}>
      <p class="question">I'm interested in going on the group hike</p>
    </TogglePrompt>

    {#if hike}
      <p>My phone number</p>
      <input type=tel name="mobile" bind:value={mobile} placeholder="XXX-XXX-XXXX" required>
    {/if}

    {#if invited_to_brunch}
      <h2>Brunch</h2>

      <p>You're invited to brunch at <a href="https://changan-artisan-noodle.business.site/" target=_blank>Chang'an Artisan Noodle</a> on Sunday, October 24<sup>th</sup>, the day after the wedding, at 11:00 AM PDT.</p>

      <iframe height="450" style="border: 0; width: 100%;" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJ6X3Saaiwj4AR-ixm6fKP-rI&key=AIzaSyAUU6DgJ-dorKgFb0XMCZ8qACjCRkcXY70"></iframe> 

      <TogglePrompt name="brunch" bind:result={brunch}>
        <p class="question">I will attend brunch</p>
      </TogglePrompt>
    {/if}
  {/if}

  <input type=submit value="Submit">
</form>
</main>

<style>
  .question {
    font-weight: bold;
  }

  main {
    margin: 0 auto;
    padding: 1em;
    max-width: 640px;
  }
</style>
