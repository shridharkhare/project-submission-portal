<script>
  let {
    isSubmitDisabled,
    tryToEnableSubmit,
    teamTopic = $bindable(),
  } = $props();

  const checkNameConstraints = () => {
    const nameRegex = /^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$/;

    if (teamTopic.value.length === 0) {
      teamTopic.error = "Topic is required";
      teamTopic.ariaInvalid = "true";
      isSubmitDisabled = false;
      tryToEnableSubmit();
    } else if (!nameRegex.test(teamTopic.value)) {
      teamTopic.error = "Invalid name format";
      teamTopic.ariaInvalid = "true";
      isSubmitDisabled = false;
      tryToEnableSubmit();
    } else {
      teamTopic.error = "Looks good!";
      teamTopic.ariaInvalid = "false";
      tryToEnableSubmit();
    }
  };
</script>

<label>
  Team Topic
  <input
    type="text"
    name="teamTopic"
    bind:value={teamTopic.value}
    oninput={checkNameConstraints}
    aria-invalid={teamTopic.ariaInvalid === ""
      ? "grammar"
      : teamTopic.ariaInvalid === "true"
        ? true
        : false}
    placeholder="Enter team topic"
    aria-describedby={teamTopic.ariaDescribedBy}
    required
  />
  <small id={teamTopic.ariaDescribedBy}>
    {teamTopic.error}
  </small>
</label>

<style>
  /* your styles go here */
</style>
