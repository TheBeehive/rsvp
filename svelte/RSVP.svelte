<script>
  import Toggle from "./Toggle.svelte"
  import { saveable } from "./saveable.js"

  export let rsvp_info = {}

  let name = rsvp_info.name || "Tony Thomas"
  let plusname = rsvp_info.plusname || "Brook Osborne"
  let invited_to_brunch = rsvp_info.invited_to_brunch || true

  let reception = saveable("reception",
      rsvp_info.reception == null ? null : Number(rsvp_info.reception))
  let vaxxed = saveable("vaxxed",
      rsvp_info.vaxxed == null ? null : Number(rsvp_info.vaxxed))
  let masked = saveable("masked",
      rsvp_info.masked == null ? null : Number(rsvp_info.masked))
  $: attendance = $reception && ($vaxxed || !$vaxxed && $masked)

  $: show_cocktail = attendance
  let cocktail = saveable("cocktail",
      rsvp_info.cocktail == null ? null : Number(rsvp_info.cocktail))
  let cocktail_switch = saveable("cocktail_switch", rsvp_info.cocktail_number > 0)
  let cocktail_number = saveable("cocktail_number", rsvp_info.cocktail_number)
  $: cocktail_excess = $cocktail_switch == 0 ? 0 : $cocktail_number
  $: cocktail_done = ($cocktail != null) && (
      $cocktail_switch == 0 ||
      $cocktail_switch == 1 && $cocktail_number != null)

  $: show_hike = attendance && (cocktail_done || $hike != null || $mobile != null)
  let hike = saveable("hike",
      rsvp_info.hike == null ? null : Number(rsvp_info.hike))
  let mobile = saveable("mobile", rsvp_info.mobile)
  $: hike_done = $hike == 0 || $hike == 1 && $mobile != null

  $: show_brunch = attendance && (hike_done || $brunch != null)
  let brunch = saveable("brunch",
      rsvp_info.brunch == null ? null : Number(rsvp_info.brunch))
  $: brunch_done = $brunch != null
</script>

<main>
<form>
  <header>
    <h1>RSVP Form for {name}</h1>

    <p>Please complete this form and submit it by September 15<sup>th</sup>. If
    you need to make any changes, this form can be resubmitted until that
    date.</p>

    <p>
      Please review our
      <a href="https://www.hackersgethitched.com/" target=_blank>wedding website</a>
      for the latest information.
    </p>
  </header>

  <section>
    <header>
      <h2>Ceremony and Reception</h2>
      <p>You're kindly invited. Some sentence goes here</p>
    </header>

    <div class="flex two">
      <dl>
        <dt>Time</dt>
        <dd>Saturday, October 23<sup>rd</sup> at 05:30 PM PDT</dd>

        <dt>Location</dt>
        <dd><a href="https://computerhistory.org/" target=_blank>Computer History Museum</a></dd>

        <dt>Note</dt>
        <dd>The dress code is black tie optional. This will be an adults-only (21+) celebration.</dd>
      </dl>

      <iframe height="360" style="border: 0; width: 50%;" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJm7NJkla3j4AR8vR-HWRxgOo&key=AIzaSyAUU6DgJ-dorKgFb0XMCZ8qACjCRkcXY70"></iframe>
    </div>

    <fieldset>
      <Toggle name={reception.name} bind:result={$reception}>
        <p class="question">I will attend the wedding ceremony and reception</p>
      </Toggle>

      {#if $reception}
        <p>
          <textarea placeholder="Please let us know if you have any allergies or dietary restrictions..." />
        </p>

        <Toggle name={vaxxed.name} bind:result={$vaxxed}>
          <p class="question">I am fully vaccinated for COVID-19</p>
        </Toggle>

        {#if $vaxxed == 0}
          The <a href="https://www.cdph.ca.gov/" target=_blank>California Department of Public Health</a> requires unvaccinated individuals to wear masks in indoor public settings. Masks may be removed when outside, or when eating or drinking. <a href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/guidance-for-face-coverings.aspx#asterisknew" target=_blank>More Information</a>
          <Toggle name={masked.name} bind:result={$masked}>
            <p class="question">I will wear a mask inside the museum, except when eating or drinking</p>
          </Toggle>

          {#if $masked == 0}
            <p>We're sorry but you can't come</p>
          {/if}
        {/if}
      {/if}
    </fieldset>
  </section>

  <section>
    <header><h2>Cocktail Reception</h2></header>

    {#if show_cocktail}
      <div class="flex two">
        <dl>
          <dt>Time</dt>
          <dd>Friday, October 22<sup>nd</sup> at 07:00 PM PDT</dd>

          <dt>Location</dt>
          <dd><a href="https://vinolocale.org/" target=_blank>Vino Locale</a></dd>
        </dl>

        <iframe height="450" style="border: 0; width: 50%;" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJ2S5OXzi7j4ARGnV-XOyU-4g&key=AIzaSyAUU6DgJ-dorKgFb0XMCZ8qACjCRkcXY70"></iframe>
      </div>

      <fieldset>
        <Toggle name={cocktail.name} bind:result={$cocktail}>
          <p class="question">I will attend the cocktail reception</p>
        </Toggle>

        {#if $cocktail}
          <Toggle name={cocktail_switch.name} bind:result={$cocktail_switch}>
            <p class="question">Will you bring any guests other than {plusname}?</p>
          </Toggle>
          <input type=hidden name="cocktail_excess" value={cocktail_excess}>

          {#if $cocktail_switch}
            <p class="question">How many guests will you bring, excluding {plusname}?</p>
            <input type=number name={cocktail_number.name} bind:value={$cocktail_number} required>
          {/if}
        {/if}
      </fieldset>
    {/if}
  </section>

  <section>
    <header><h2>Wedding Day Hike</h2></header>

    {#if attendance && cocktail_done}
      <p>If there's enough interest, we'll organize a group hike the morning of our wedding.</p>

      <fieldset>
        <Toggle name={hike.name} bind:result={$hike}>
          <p class="question">I'm interested in going on the group hike</p>
        </Toggle>

        {#if $hike}
          <p>My phone number</p>
          <input type=tel name={mobile.name} bind:value={$mobile} placeholder="XXX-XXX-XXXX" required>
        {/if}
      </fieldset>
    {/if}
  </section>

  <section>
    <header><h2>Brunch</h2></header>

    {#if attendance && invited_to_brunch && hike_done}
      <p>You're invited to brunch at <a href="https://changan-artisan-noodle.business.site/" target=_blank>Chang'an Artisan Noodle</a> on Sunday, October 24<sup>th</sup>, the day after the wedding, at 11:00 AM PDT.</p>

      <iframe height="450" style="border: 0; width: 100%;" loading="lazy" allowfullscreen src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJ6X3Saaiwj4AR-ixm6fKP-rI&key=AIzaSyAUU6DgJ-dorKgFb0XMCZ8qACjCRkcXY70"></iframe>

      <fieldset>
        <Toggle name={brunch.name} bind:result={$brunch}>
          <p class="question">I will attend brunch</p>
        </Toggle>
      </fieldset>
    {/if}
  </section>

  <input type=submit value="Submit">
</form>
</main>

<style>
  .question {
    margin-right: 1rem;
    font-weight: bold;
  }

  section > :not(header, fieldset) {
    box-sizing: border-box;
    margin: 0.5rem;
  }

  header {
    margin: 1rem 0;
  }

  textarea {
    height: 7em;
  }

  h2 {
    border-top: 1px solid #000000;
    border-bottom: 1px solid #000000;
  }

  dt {
    text-transform: uppercase;
    font-weight: bold;
    color: #aaaaaa;
  }

  dd {
    margin-bottom: 1rem;
    margin-right: 1rem;
  }
</style>
