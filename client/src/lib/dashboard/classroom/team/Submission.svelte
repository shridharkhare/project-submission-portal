<script>
  import { onMount } from "svelte";
  import { notifyAlert, svelteState } from "../../../../stores/store.svelte";

  let { g_id, teamId, leader_id } = $props();

  let submissionData = $state({
    githubUrl: "",
    pptUrl: "",
    reportUrl: "",
  });

  const getExistingSubmission = async () => {
    svelteState.loading = true;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams/${teamId}/submissions`,
        {
          method: "GET",
          credentials: "include",
        }
      );
      if (response.ok) {
        const data = await response.json();
        submissionData.githubUrl = data.github_url;
        submissionData.pptUrl = data.ppt_url;
        submissionData.reportUrl = data.report_url;
      } else {
        notifyAlert("error", "Error fetching submission data");
      }
    } catch (error) {
      notifyAlert("error", "Network error");
    } finally {
      svelteState.loading = false;
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    svelteState.loading = true;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams/${teamId}/submissions`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            leader_id: leader_id,
            team_id: teamId,
            g_id: g_id,
            github_url: submissionData.githubUrl,
            ppt_url: submissionData.pptUrl,
            report_url: submissionData.reportUrl,
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

  onMount(() => {
    getExistingSubmission();
  });
</script>

<section>
  <h3>Submission</h3>
  <form onsubmit={handleSubmit}>
    <div>
      <label for="githubUrl">Github URL:</label>
      <input
        type="url"
        name="github_url"
        bind:value={submissionData.githubUrl}
        required
      />
    </div>
    <div>
      <label for="pptUrl">PPT URL:</label>
      <input
        type="url"
        name="ppt_url"
        bind:value={submissionData.pptUrl}
        required
      />
    </div>
    <div>
      <label for="reportUrl">Report URL:</label>
      <input
        type="url"
        name="report_url"
        bind:value={submissionData.reportUrl}
        required
      />
    </div>
    <button type="submit">
      <i class="fa-solid fa-paper-plane"></i>
      &nbsp; Submit
    </button>
  </form>
</section>

<style>
  section {
    padding: 1rem;
  }
</style>
