<script>
  import Location from "./Location.svelte"
  import Toggle from "./Toggle.svelte"
  import { saveable } from "./saveable.js"

  export let rsvp_info = {}

  let name = rsvp_info.name
  let plusname = rsvp_info.plusname
  let noods = rsvp_info.noods

  function format_time(time) {
    return Intl.DateTimeFormat([], { dateStyle: "long", timeStyle: "long" }).format(new Date(time))
  }

  let link_form
  function handle_link() {
    link_form.submit()
  }

  // Ceremony and Reception //
  // ====================== //
  let reception = saveable("reception", rsvp_info.reception)
  let diet_info = saveable("diet_info", rsvp_info.diet_info)
  let vaxxed = saveable("vaxxed", rsvp_info.vaxxed)
  let masked = saveable("masked", rsvp_info.masked)
  $: attend = $reception && $masked
  /* $: attend = $reception && ($vaxxed || !$vaxxed && $masked) */

  $: done_to_reception =
      $reception == 1 && $vaxxed != null && $masked == 1 ||
      $reception == 0

  /* $: done_to_reception = */
  /*     $reception == 1 && $vaxxed == 1 || */
  /*     $reception == 1 && $vaxxed == 0 && $masked != null || */
  /*     $reception == 0 */

  // Cocktail Reception //
  // ================== //
  $: show_cocktail = attend && (done_to_reception ||
      $cocktail != null || $cocktail_switch != null || $cocktail_number != null)
  let cocktail = saveable("cocktail", rsvp_info.cocktail)
  let cocktail_switch = saveable("cocktail_switch",
      rsvp_info.cocktail_excess != null ?
      Number(rsvp_info.cocktail_excess > 0) : null)
  let cocktail_number = saveable("cocktail_number", rsvp_info.cocktail_excess)
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
  $: show_brunch = attend && (done_to_hike || $brunch != null)
  let brunch = saveable("brunch", rsvp_info.brunch)
  $: done_to_brunch = done_to_hike && (!noods || $brunch != null)

  // Submit //
  // ====== //
  $: show_submit =
      $reception == 1 && $vaxxed != null && $masked != null ||
      $reception == 0
</script>

<main>
<header>
  <h1>RSVP Form for {name}</h1>

  {#if rsvp_info.submitted_at != null}
    <p><strong>Last submitted</strong> on {format_time(rsvp_info.submitted_at)}</p>
  {/if}

  <p>Please complete and submit by September 15<sup>th</sup>. This form will
  remain open for resubmission until then.</p>

  <form bind:this={link_form} action="https://www.hackersgethitched.com/" method=POST target=_blank>
    <input type=hidden name="email_address" value={rsvp_info.email}>
    <p>Details and updates on our
      <a href="https://www.hackersgethitched.com/" target=_blank on:click|preventDefault={handle_link}>wedding website</a>.
    </p>
  </form>
</header>

<form method=POST>
  <section class="active">
    <header><h2>1. Ceremony and Reception</h2></header>

    <div class="flex two detail">
      <dl>
        <dt>Time</dt>
        <dd>Saturday, October 23<sup>rd</sup> at 05:30 PM PDT</dd>

        <dt>Location</dt>
        <dd><a href="https://computerhistory.org/" target=_blank>Computer History Museum</a></dd>

        <dt>Dress</dt>
        <dd><a
          href="https://emilypost.com/advice/attire-guide-dress-codes-from-casual-to-white-tie" target=_blank>
          Black-Tie Optional</a></dd>

        <dt>Note</dt>
        <dd>This will be an adults-only (21+) celebration</dd>
      </dl>

      <Location id=ChIJm7NJkla3j4AR8vR-HWRxgOo />
    </div>

    <fieldset>
      <Toggle name="reception" bind:result={$reception}>
        <p class="question">I'd like to attend the wedding ceremony and reception</p>
      </Toggle>

      {#if $reception}
        <p><textarea name="diet_info" bind:value={$diet_info} style="height: 7em;" placeholder="Please let us know if you have any allergies or dietary restrictions..." /></p>

        <Toggle name="vaxxed" bind:result={$vaxxed}>
          <p class="question">I am fully vaccinated for COVID-19</p>
        </Toggle>

        {#if $vaxxed == 0}
          <p>We have registered your interest in attending the event. However, your RSVP is <strong>provisional</strong> at this time.</p>
          <p>Due to the evolving nature of the COVID-19 pandemic and the associated changes to local and state regulations as well as the requirements of our venue, we <strong>cannot</strong> guarantee that we will be able to accommodate unvaccinated guests at our wedding.</p>
          <p>If the requirements for attendance change between now and October 23<sup>rd</sup> such that we are unable to accommodate unvaccinated guests, we will notify you via email. Should your vaccination status change between now and then, please update and resubmit this form.</p>
          <hr>
        {/if}

        <p>At the moment, Santa Clara County requires all individuals, regardless of vaccination status, to <a href="https://covid19.sccgov.org/order-health-officer-08-02-2021-requiring-all-to-use-face-covering-indoors" target=_blank>wear a mask</a> when indoors, except when eating or drinking.</p>

        <Toggle name="masked" bind:result={$masked}>
          <p class="question">I will comply with any mask requirement in effect at the event</p>
        </Toggle>

        {#if $masked == 0}
          <p>To ensure the health and safety of our guests and staff, we're unable to accomodate your attendance.</p>
        {/if}
      {/if}
    </fieldset>
  </section>

  <section class:active={show_cocktail}>
    <header><h2>2. Welcome Reception</h2></header>

    {#if show_cocktail}
      <div class="flex two detail">
        <dl>
          <dt>Time</dt>
          <dd>Friday, October 22<sup>nd</sup> at 06:00 PM PDT</dd>

          <dt>Location</dt>
          <dd><a href="https://www.rosewoodhotels.com/en/sand-hill-menlo-park" target=_blank>Rosewood Sand Hill</a></dd>

          <dt>Dress</dt>
          <dd><a
            href="https://emilypost.com/advice/attire-guide-dress-codes-from-casual-to-white-tie" target=_blank>Semi-Formal</a></dd>
        </dl>

        <Location id=ChIJiUNAfPukj4ARkQSP3H1etD4 />
      </div>

      <fieldset>
        <Toggle name="cocktail" bind:result={$cocktail}>
          <p class="question">I will attend the cocktail reception</p>
        </Toggle>

        {#if $cocktail}
          <Toggle name="cocktail_switch" bind:result={$cocktail_switch}>
            <p class="question">Will you bring any guests apart from {plusname}?</p>
          </Toggle>
          <input type=hidden name="cocktail_excess" value={cocktail_excess}>

          {#if $cocktail_switch}
            <div class="prompt">
              <p class="question">How many other guests will you bring?</p>
              <select name="cocktail_number" bind:value={$cocktail_number} required>
                <option hidden value></option>
                <option value={1}>1</option>
                <option value={2}>2</option>
                <option value={3}>3</option>
              </select>
            </div>
          {/if}
        {/if}
      </fieldset>
    {/if}
  </section>

  <section class:active={show_hike}>
    <header><h2>3. Wedding Day Hike</h2></header>

    {#if show_hike}
      <p>If there's enough interest, our wedding crew will lead a group hike
      the morning of the wedding at a South Bay Open Space Preserve.</p>

      <fieldset>
        <Toggle name="hike" bind:result={$hike}>
          <p class="question">I'm interested in the group hike</p>
        </Toggle>

        {#if $hike}
          <p>We'll need your contact information to coordinate the hike. Please
          provide your day-of mobile number.</p>

          <div class="prompt">
            <p class="question">My day-of mobile number</p>
            <input type=tel name="mobile" bind:value={$mobile} placeholder="XXX-XXX-XXXX" required>
          </div>
        {/if}
      </fieldset>
    {/if}
  </section>

  {#if noods}
    <section class:active={show_brunch}>
      <header><h2>4. Brunch</h2></header>

      {#if show_brunch}
        <p>Drop by and join Kaiting and Melanie for a few California IPAs and
          spicy, numbing noodles at one of their favorite places in the South
          Bay!</p>
        <div class="flex two detail">
          <dl>
            <dt>Time</dt>
            <dd>Sunday, October 24<sup>th</sup> at 12:00 PM PDT</dd>

            <dt>Location</dt>
            <dd><a href="https://changan-artisan-noodle.business.site/" target=_blank>Chang'an Artisan Noodle</a></dd>

            <dt>Dress</dt>
            <dd>Casual</dd>

            <dt>Note</dt>
            <dd>This will be an adults-only (21+) celebration.</dd>
          </dl>

          <Location id=ChIJ6X3Saaiwj4AR-ixm6fKP-rI />
        </div>

        <fieldset>
          <Toggle name="brunch" bind:result={$brunch}>
            <p class="question">I will attend the brunch</p>
          </Toggle>
        </fieldset>
      {/if}
    </section>
  {/if}

  <section class:active={show_submit}>
    <p class="action">
      <a class="pseudo button help" href="mailto:ktchen14@gmail.com,melanieplageman@gmail.com?subject=Help with RSVP Form">Help</a>
      {#if show_submit}
        <input type=submit value="Submit">
      {/if}
    </p>
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

  .action {
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

  input, select {
    width: auto;
  }

  select {
    padding-right: 1.2em;
  }
</style>
