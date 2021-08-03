<script>
  import Location from "./Location.svelte"
  import Toggle from "./Toggle.svelte"
  import { saveable } from "./saveable.js"

  export let rsvp_info = {}

  let name = rsvp_info.name
  let noods = rsvp_info.noods

  // Ceremony and Reception //
  // ====================== //
  let reception = saveable("reception", rsvp_info.reception)
  let vaxxed = saveable("vaxxed", rsvp_info.vaxxed)
  let masked = saveable("masked", rsvp_info.masked)

  let plus_switch = saveable("plus_switch", rsvp_info.plusname != null ?
    (rsvp_info.plusname ? 1 : 0) : null)
  let plusname = saveable("plusname", rsvp_info.plusname)
  let plusvaxxed = saveable("plusvaxxed", rsvp_info.plusvaxxed)
  let plusmasked = saveable("plusmasked", rsvp_info.plusmasked)

  $: attend = $reception && ($vaxxed || !$vaxxed && $masked)
  $: plusattend = $plus_switch == 1 &&
      $plusname && ($plusvaxxed || !$plusvaxxed && $plusmasked)
  $: attend_continue = attend && ($plus_switch == 0 || plusattend)


  $: done_to_reception = (
      $reception == 1 && $vaxxed == 1 ||
      $reception == 1 && $vaxxed == 0 && $masked != null ||
      $reception == 0
  ) && (!attend || (
      $plus_switch == 1 && $plusname && $plusvaxxed == 1 ||
      $plus_switch == 1 && $plusname && $plusvaxxed == 0 && $plusmasked != null ||
      $plus_switch == 0
  ))

  // Cocktail Reception //
  // ================== //
  $: show_cocktail = attend_continue && (done_to_reception ||
    $cocktail != null || $pluscocktail != null || $cocktail_switch != null || $cocktail_number != null)
  let cocktail = saveable("cocktail", rsvp_info.cocktail)
  let pluscocktail = saveable("pluscocktail", rsvp_info.pluscocktail)
  let cocktail_switch = saveable("cocktail_switch",
      rsvp_info.cocktail_excess != null ?
      Number(rsvp_info.cocktail_excess > 0) : null)
  let cocktail_number = saveable("cocktail_number", rsvp_info.cocktail_excess)
  $: cocktail_excess = !$cocktail_switch ? 0 : $cocktail_number
  $: done_to_cocktail = done_to_reception && (
      $cocktail == 1 && (!$plus_switch || $pluscocktail != null) &&
        $cocktail_switch == 0 ||
      $cocktail == 1 && (!$plus_switch || $pluscocktail != null) &&
        $cocktail_switch == 1 && $cocktail_number != null ||
      $cocktail == 0)

  // Hike //
  // ==== //
  $: show_hike = attend_continue && (done_to_cocktail ||
      $hike != null || $mobile != null || $plushike != null || $plusmobile != null)
  let hike = saveable("hike", rsvp_info.hike)
  let mobile = saveable("mobile", rsvp_info.mobile)
  let plushike = saveable("plushike", rsvp_info.plushike)
  let plusmobile = saveable("plusmobile", rsvp_info.plusmobile)
  $: done_to_hike = done_to_cocktail && (
    $hike == 1 && $mobile && (!$plus_switch || $plushike == 1 && $plusmobile) ||
    $hike == 1 && $mobile && (!$plus_switch || $plushike == 0) ||
    $hike == 0)

  // Brunch //
  // ====== //
  $: show_brunch = attend_continue && (done_to_hike || $brunch != null)
  let brunch = saveable("brunch", rsvp_info.brunch)
  let plusbrunch = saveable("plusbrunch", rsvp_info.plusbrunch)
  $: done_to_brunch = done_to_hike && (!noods ||
    $brunch != null && (!$plus_switch || $plusbrunch != null))

  // Submit //
  // ====== //
  $: show_submit = done_to_reception
</script>

<main>
<form method=POST>
  <header>
    <h1>RSVP Form for {name}</h1>

    <p>Please complete and submit by September 15<sup>th</sup>. This form will
    remain open for resubmission until then.</p>

    <p>Details and updates on our
      <a href="https://www.hackersgethitched.com/" target=_blank>wedding website</a>.
    </p>
  </header>

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
          href="https://emilypost.com/advice/attire-guide-dress-codes-from-casual-to-white-tie">
          Black-Tie Optional</a></dd>

        <dt>Note</dt>
        <dd>This will be an adults-only (21+) celebration</dd>
      </dl>

      <Location id=ChIJm7NJkla3j4AR8vR-HWRxgOo />
    </div>

    <fieldset>
      <Toggle name="reception" bind:result={$reception}>
        <p class="question">I will attend the wedding ceremony and reception</p>
      </Toggle>

      {#if $reception}
        <p><textarea style="height: 7em;" placeholder="Please let us know if you have any allergies or dietary restrictions..." /></p>

        <Toggle name="vaxxed" bind:result={$vaxxed}>
          <p class="question">I am fully vaccinated for COVID-19</p>
        </Toggle>

        {#if $vaxxed == 0}
          <p>The <a href="https://www.cdph.ca.gov/" target=_blank>California Department of Public Health</a> requires unvaccinated individuals to wear a mask in public settings when indoors, except when eating or drinking. <a href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/guidance-for-face-coverings.aspx#asterisknew" target=_blank>More Information</a></p>

          <Toggle name="masked" bind:result={$masked}>
            <p class="question">I will comply with this state mandated requirement</p>
          </Toggle>

          {#if $masked == 0}
            <p>To ensure the health and safety of our guests and staff, we're unable to accomodate your attendance.</p>
          {/if}
        {/if}
      {/if}

      {#if attend}
        <Toggle name="plus_switch" bind:result={$plus_switch}>
          <p class="question">I'm bringing a plus one</p>
        </Toggle>

        {#if $plus_switch}
          <div class="prompt">
            <p class="question">Who's your plus one?</p>
            <input type=text name="plusname" bind:value={$plusname} placeholder="Full Name" required>
          </div>

          {#if $plusname}
            <Toggle name="plusname" bind:result={$plusvaxxed}>
              <p class="question">{$plusname} is fully vaccinated for COVID-19</p>
            </Toggle>

            {#if $plusvaxxed == 0}
              <!-- Skip this informational section if it's redundant -->
              {#if $vaxxed != 0}
                <p>The <a href="https://www.cdph.ca.gov/" target=_blank>California Department of Public Health</a> requires unvaccinated individuals to wear a mask in public settings when indoors, except when eating or drinking. <a href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/guidance-for-face-coverings.aspx#asterisknew" target=_blank>More Information</a></p>
              {/if}

              <Toggle name="plusmasked" bind:result={$plusmasked}>
                <p class="question">{$plusname} will comply with the state mandated mask requirement</p>
              </Toggle>

              {#if $plusmasked == 0}
                <p>To ensure the health and safety of our guests and staff, we're unable to accomodate {$plusname}'s attendance.</p>
              {/if}
            {/if}
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

          <dt>Dress</dt>
          <dd><a
            href="https://emilypost.com/advice/attire-guide-dress-codes-from-casual-to-white-tie">
            Dressy Casual</a></dd>
        </dl>

        <Location id=ChIJ2S5OXzi7j4ARGnV-XOyU-4g />
      </div>

      <fieldset>
        <Toggle name="cocktail" bind:result={$cocktail}>
          <p class="question">I will attend the cocktail reception</p>
        </Toggle>

        {#if $cocktail}
          {#if plusattend}
            <Toggle name="pluscocktail" bind:result={$pluscocktail}>
              <p class="question">Will you bring {$plusname}?</p>
            </Toggle>
          {/if}

          {#if plusattend && $pluscocktail != null || !plusattend}
            <Toggle name="cocktail_switch" bind:result={$cocktail_switch}>
              <p class="question">
                {#if plusattend && $pluscocktail}
                  Will you bring any guests apart from {$plusname}?
                {:else}
                  Will you bring any guests?
                {/if}
              </p>
            </Toggle>
          {/if}
          <input type=hidden name="cocktail_excess" value={cocktail_excess}>

          {#if $cocktail_switch}
            <div class="prompt">
              <p class="question">
                How many {#if plusattend && $pluscocktail} other {/if} guests will you bring?
              </p>
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
          {#if plusattend}
            <Toggle name="plushike" bind:result={$plushike}>
              <p class="question">{$plusname} is interested in the group hike</p>
            </Toggle>
          {/if}

          <p>We'll need your contact information to coordinate the hike. Please
          provide your day-of mobile number.</p>

          <div class="prompt">
            <p class="question">My day-of mobile number</p>
            <input type=tel name="mobile" bind:value={$mobile} placeholder="XXX-XXX-XXXX" required>
          </div>

          {#if plusattend && $plushike}
            <div class="prompt">
              <p class="question">{$plusname}'s day-of mobile number</p>
              <input type=tel name="plusmobile" bind:value={$plusmobile} placeholder="XXX-XXX-XXXX" required>
            </div>
          {/if}
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
        {#if $brunch && plusattend}
          <Toggle name="plusbrunch" bind:result={$plusbrunch}>
            <p class="question">{$plusname} will attend the brunch</p>
          </Toggle>
        {/if}
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
