<script>
  import { svelteState } from "../../../../stores/store.svelte";

  let numMembers = $state(3);
  let selectedRollNumbers = $state([]);
  let error = $state("Please select the correct number of roll numbers.");

  let buttonInvalid = $state(true);
  let buttonError = $state(
    "You have to verify if none of the selected students are already in a team."
  );

  let {
    g_id,
    allUsersAvailable = $bindable(),
    isSubmitDisabled,
    tryToEnableSubmit,
    isInvalid = $bindable(),
  } = $props();

  const checkIfStudentInTeam = async (rollNumber) => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/students/status?roll=${rollNumber}`,
        {
          method: "GET",
          credentials: "include",
        }
      );
      const data = await response.json();

      return data.message; // Ensure the response is explicitly checked for true
    } catch (error) {
      console.error("Error checking if student is in team:", error);
      return false;
    }
  };

  const checkIfAllStudentsNotInTeam = async () => {
    for (const rollNumber of selectedRollNumbers) {
      // Check if the student is already in a team
      const isStudentInTeam = await checkIfStudentInTeam(rollNumber);
      console.log("isStudentInTeam", isStudentInTeam);
      if (isStudentInTeam) {
        buttonInvalid = true;
        buttonError = `Roll number ${rollNumber} is already in a team.`;
        allUsersAvailable = false;
        isSubmitDisabled = true;
        tryToEnableSubmit();
        return;
      }
    }
    buttonError = "All selected students are available.";
    allUsersAvailable = true;
    tryToEnableSubmit();
  };

  const checkRollNumbers = () => {
    allUsersAvailable = false;
    buttonInvalid = true;
    buttonError =
      "You have to verify if none of the selected students are already in a team.";
    const currentUserRollNumber = svelteState.user.roll_no;

    if (selectedRollNumbers.includes(currentUserRollNumber)) {
      isInvalid = true;
      error = "You cannot select your own roll number.";
      isSubmitDisabled = true;
      tryToEnableSubmit();
      return;
    }

    const selectedCount = selectedRollNumbers.length;
    isInvalid = selectedCount !== numMembers;

    if (isInvalid) {
      error = `Please select ${numMembers} roll numbers.`;
      isSubmitDisabled = true;
      tryToEnableSubmit();
    } else {
      error = "";
      tryToEnableSubmit();
    }
  };
</script>

<div>
  <fieldset>
    <legend>Number of Team Members</legend>
    <div class="flex">
      <label>
        <input
          type="radio"
          name="team-members"
          value="2"
          onchange={() => (numMembers = 2)}
        />
        2
      </label>
      <label>
        <input
          type="radio"
          name="team-members"
          value="3"
          onchange={() => (numMembers = 3)}
          checked
        />
        3
      </label>
      <label>
        <input
          type="radio"
          name="team-members"
          value="4"
          onchange={() => (numMembers = 4)}
        />
        4
      </label>
    </div>
  </fieldset>
  <label>
    Select Roll Numbers (use Ctrl/Cmd to select multiple):
    <select
    multiple
      bind:value={selectedRollNumbers}
      onchange={checkRollNumbers}
      aria-invalid={isInvalid}
      aria-describedby="error-message"
      name="roll_call"
    >
      {#each Array.from({ length: 100 }, (_, i) => i + 1) as rollNumber}
        <option value={rollNumber}>{rollNumber}</option>
      {/each}
    </select>
    <small id="error-message">
      {error}
    </small>
  </label>
  <div class="flex-col">
    <small class="error-text">
      {#if buttonInvalid}
        {buttonError}
      {/if}
    </small>
    <button type="button" onclick={checkIfAllStudentsNotInTeam}>
      Check Roll Numbers
    </button>
  </div>
</div>

<style>
  .flex {
    display: flex;
    gap: 1rem;
  }
  .flex-col {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .error-text {
    color: rgb(232, 59, 59);
    font-size: 0.875rem;
  }
</style>
