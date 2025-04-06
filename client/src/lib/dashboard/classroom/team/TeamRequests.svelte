<script>
  import { onMount } from "svelte";
  import { notifyAlert, svelteState } from "../../../../stores/store.svelte";
  import { convertDateToHumanReadable } from "../../../utils/date";

  let { g_id } = $props();

  let teamRequests = $state([]);

  const getTeamRequests = async () => {
    svelteState.loading = true;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams/requests`,
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch team requests");
      }

      const data = await response.json();
      notifyAlert("success", "Team requests fetched successfully");
      return data;
    } catch (error) {
      notifyAlert(
        "error",
        error.message || "An error occurred while fetching team requests"
      );
    } finally {
      svelteState.loading = false;
    }
  };

  const approveRequest = async (req_id) => {
    svelteState.loading = true;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams/requests/${req_id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status: "approve" }),
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to accept team request");
      }

      notifyAlert("success", "Team request accepted successfully");
      teamRequests = teamRequests.filter(
        (request) => request.req_id !== req_id
      );
      window.location.reload();
    } catch (error) {
      notifyAlert(
        "error",
        error.message || "An error occurred while accepting the request"
      );
    } finally {
      svelteState.loading = false;
    }
  };

  const rejectRequest = async (req_id) => {
    svelteState.loading = true;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams/requests/${req_id}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status: "reject" }),
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to reject team request");
      }

      notifyAlert("success", "Team request rejected successfully");
      teamRequests = teamRequests.filter(
        (request) => request.req_id !== req_id
      );
    } catch (error) {
      notifyAlert(
        "error",
        error.message || "An error occurred while rejecting the request"
      );
    } finally {
      svelteState.loading = false;
    }
  };

  onMount(async () => {
    const data = await getTeamRequests();
    if (data) {
      teamRequests = data;
    }
  });
</script>

<section class="team-requests">
  <h2>Team Requests</h2>
  {#if teamRequests.length > 0}
    {#each teamRequests as request}
      <details name="team-request">
        <summary>
          <strong>Request from {request.sender_id}</strong>
        </summary>
        <table>
          <tbody>
            <tr>
              <td>Team ID</td>
              <td>{request.team_id}</td>
            </tr>
            <tr>
              <td>Topic</td>
              <td>{request.topic}</td>
            </tr>
            <tr>
              <td>Sent At</td>
              <td>{convertDateToHumanReadable(request.created_at)}</td>
            </tr>
          </tbody>
        </table>
        <button onclick={() => approveRequest(request.req_id)}>
          <i class="fa-solid fa-check"></i> &nbsp; Approve
        </button>
        <button class="secondary" onclick={() => rejectRequest(request.req_id)}>
          <i class="fa-solid fa-xmark"></i> &nbsp; Reject
        </button>
      </details>
    {/each}
  {:else}
    <p>No team requests available.</p>
  {/if}
</section>

<style>
  .team-requests {
    border: 2px dashed var(--pico-primary-border);
    border-radius: 8px;
    padding: 1rem;
  }

  .team-requests h2 {
    margin-bottom: 1rem;
  }

  .team-requests details {
    background-color: var(--pico-background-color);
    margin-bottom: 1rem;
    padding: 0.7rem;
    border: 1px solid var(--pico-primary-border);
    border-radius: 4px;
  }

  .team-requests summary {
    font-weight: bold;
    cursor: pointer;
  }

  .team-requests p {
    margin: 0.5rem 0;
  }

  .team-requests button {
    margin-right: 0.5rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
