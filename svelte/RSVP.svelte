<script>
  import Location from "./Location.svelte"
  import Toggle from "./Toggle.svelte"
  import { saveable } from "./saveable.js"

  export let rsvp_info = {}

  let name = rsvp_info.name
  let plusname = rsvp_info.plusname
  let invited_to_brunch = rsvp_info.invited_to_brunch

  // Ceremony and Reception //
  // ====================== //
  let reception = saveable("reception", rsvp_info.reception)
  let vaxxed = saveable("vaxxed", rsvp_info.vaxxed)
  let masked = saveable("masked", rsvp_info.masked)
  $: done_to_reception =
      $reception == 1 && $vaxxed == 1 ||
      $reception == 1 && $vaxxed == 0 && $masked != null ||
      $reception == 0
  $: attend = $reception && ($vaxxed || !$vaxxed && $masked)

  // Cocktail Reception //
  // ================== //
  $: show_cocktail = attend && (done_to_reception ||
      $cocktail != null || $cocktail_switch != null || $cocktail_number != null)
  let cocktail = saveable("cocktail", rsvp_info.cocktail)
  let cocktail_switch = saveable("cocktail_switch",
      Number(rsvp_info.cocktail_number > 0))
  let cocktail_number = saveable("cocktail_number", rsvp_info.cocktail_number)
  $: cocktail_excess = !$cocktail_switch ? 0 : $cocktail_number
  $: done_to_cocktail = done_to_reception && (
      $cocktail == 1 && $cocktail_switch == 0 ||
      $cocktail == 1 && $cocktail_switch == 1 && $cocktail_number != null ||
      $cocktail == 0)

  // Hike //
  // ==== //
  $: show_hike = attend && (done_to_cocktail ||
      $hike != null || $mobile != null)
  let hike = saveable("hike", rsvp_info.hike)
  let mobile = saveable("mobile", rsvp_info.mobile)
  $: done_to_hike = done_to_cocktail && (
      $hike == 1 && $mobile || $hike == 0)

  // Brunch //
  // ====== //
  $: show_brunch = attend && (done_to_hike ||
      $brunch != null)
  let brunch = saveable("brunch", rsvp_info.brunch)
  $: done_to_brunch = done_to_hike && (
      !invited_to_brunch || $brunch != null)

  // Submit //
  // ====== //
  $: show_submit = done_to_reception
</script>

<main>
<form method=POST>
  <header>
    <h1>RSVP Form for {name}</h1>

    <p>Please complete this form and submit it by September 15<sup>th</sup>. If
    you need to make any changes, this form can be resubmitted until that
    date.</p>

    <p>Please review our
      <a href="https://www.hackersgethitched.com/" target=_blank>wedding website</a>
      for the latest information.</p>
  </header>

  <section class="active">
    <header><h2>1. Ceremony and Reception</h2></header>

    <div class="flex two detail">
      <dl>
        <dt>Time</dt>
        <dd>Saturday, October 23<sup>rd</sup> at 05:30 PM PDT</dd>

        <dt>Location</dt>
        <dd><a href="https://computerhistory.org/" target=_blank>Computer History Museum</a></dd>

        <dt>Note</dt>
        <dd>The dress code is black tie optional. This will be an adults-only (21+) celebration.</dd>
      </dl>

      <Location id=ChIJm7NJkla3j4AR8vR-HWRxgOo />
    </div>

    <fieldset>
      <Toggle name={reception.name} bind:result={$reception}>
        <p class="question">I will attend the wedding ceremony and reception</p>
      </Toggle>

      {#if $reception}
        <p><textarea style="height: 7em;" placeholder="Please let us know if you have any allergies or dietary restrictions..." /></p>

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

  <section class:active={show_cocktail}>
    <header><h2>2. Cocktail Reception</h2></header>

    {#if show_cocktail}
      <div class="flex two detail">
        <dl>
          <dt>Time</dt>
          <dd>Friday, October 22<sup>nd</sup> at 07:00 PM PDT</dd>

          <dt>Location</dt>
          <dd><a href="https://vinolocale.org/" target=_blank>Vino Locale</a></dd>
        </dl>

        <Location id=ChIJ2S5OXzi7j4ARGnV-XOyU-4g />
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

  <section class:active={show_hike}>
    <header><h2>3. Wedding Day Hike</h2></header>

    {#if show_hike}
      <p>If there's enough interest, we'll organize a group hike the morning of our wedding.</p>

      <fieldset>
        <Toggle name={hike.name} bind:result={$hike}>
          <p class="question">I'm interested in going on the group hike</p>
        </Toggle>

        {#if $hike}
          <div class="prompt">
            <p class="question">My mobile number</p>
            <input type=tel name={mobile.name} bind:value={$mobile} placeholder="XXX-XXX-XXXX" required>
          </div>
        {/if}
      </fieldset>
    {/if}
  </section>

  {#if invited_to_brunch}
  <section class:active={show_brunch}>
    <header><h2>4. Brunch</h2></header>

    {#if show_brunch}
      <div class="flex two detail">
        <dl>
          <dt>Time</dt>
          <dd>Sunday, October 24<sup>th</sup> at 12:00 PM PDT</dd>

          <dt>Location</dt>
          <dd><a href="https://changan-artisan-noodle.business.site/" target=_blank>Chang'an Artisan Noodle</a></dd>
        </dl>

        <Location id=ChIJ6X3Saaiwj4AR-ixm6fKP-rI />
      </div>

      <fieldset>
        <Toggle name={brunch.name} bind:result={$brunch}>
          <p class="question">I will attend brunch</p>
        </Toggle>
      </fieldset>
    {/if}
  </section>
  {/if}

  <section class:active={show_submit}>
    {#if show_submit}
      <p style="text-align: right;"><input type=submit value="Submit"></p>
    {/if}
  </section>
</form>
</main>

<style>
  section {
    margin: 1em auto;
    border-top: 1px solid #aaaaaa;
  }

  .active {
    border-top: 1px solid #000000;
  }

  header {
    margin-bottom: 1em;
  }

  .active h2 {
    padding-bottom: 0.6em;
    border-bottom: 1px solid #aaaaaa;
    color: #000000;
  }

  h2 {
    padding-bottom: 0;
    color: #aaaaaa;
  }

  .detail > :global(*) {
    flex-grow: 1 !important;
  }

  dt {
    color: #aaaaaa;
    font-weight: bold;
    text-transform: uppercase;
  }

  dd {
    margin-bottom: 1em;
  }

  fieldset {
    margin-top: 0.4em;
    border-radius: 0.2em;
    padding: 1em;
    background: #f5f2f0;
  }

  .question {
    margin-right: 1em;
    font-weight: bold;
  }

  input {
    width: auto;
  }
</style>
