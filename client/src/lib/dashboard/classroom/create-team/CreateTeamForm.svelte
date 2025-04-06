<script>
  let { activeClassroom } = $props();

  import { notifyAlert, svelteState } from "../../../../stores/store.svelte";

  import TeamMemberSelect from "../create-team/TeamMemberSelect.svelte";
  import TeamTopicInput from "./TeamTopicInput.svelte";

  let isSubmitDisabled = $state(true);

  let teamTopic = $state({
    value: "",
    error: "",
    ariaInvalid: "",
    ariaDescribedBy: "teamTopicError",
  });

  let isInvalid = $state(true);

  let allUsersAvailable = $state(false);

  const tryToEnableSubmit = () => {
    if (teamTopic.ariaInvalid === "false" && !isInvalid && allUsersAvailable) {
      isSubmitDisabled = false;
    } else {
      isSubmitDisabled = true;
    }
  };

  const buildTeam = (/** @type {FormData} */ formData) => {
    const topic = formData.get("teamTopic");
    const roll_calls = formData.getAll("roll_call");
    const g_id = activeClassroom.g_id;
    const sub = activeClassroom.sub;

    const team = {
      topic,
      roll_calls,
      g_id,
      sub,
    };

    return team;
  };

  const createSubmission = async (e, g_id, team_id, leader_id) => {
    svelteState.loading = true;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams/${team_id}/submissions`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            leader_id: leader_id,
            team_id: team_id,
            g_id: g_id,
            github_url: "",
            ppt_url: "",
            report_url: "",
          }),
          credentials: "include",
        }
      );
      if (response.ok) {
        notifyAlert("success", "Submission successful");
      } else {
        notifyAlert("error", "Error submitting data");
      }
    } catch (error) {
      notifyAlert("error", "Network error");
    } finally {
      svelteState.loading = false;
    }
  };

  const createTeam = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const team = buildTeam(formData);
    let team_id = null;
    let leader_id = null;

    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${team.g_id}/teams`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(team),
          credentials: "include",
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log("Team created successfully:", data);
        team_id = data.team_id;
        leader_id = data.leader_id;
        createSubmission(e, team.g_id, team_id, leader_id);
        window.location.reload();
      } else {
        console.error("Error creating team:", response.statusText);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  };
</script>

<article class="card">
  <header>
    <h2>Create a Team</h2>
  </header>
  <form onsubmit={createTeam}>
    <TeamTopicInput bind:teamTopic {isSubmitDisabled} {tryToEnableSubmit} />
    <TeamMemberSelect
      bind:isInvalid
      {isSubmitDisabled}
      {tryToEnableSubmit}
      bind:allUsersAvailable
      g_id={activeClassroom.g_id}
    />

    <button type="submit" disabled={isSubmitDisabled}>
      <i class="fa-solid fa-people-group"></i> Create Team
    </button>
  </form>
</article>

<style>
</style>
