<script>
  let { leaderRollNo, g_id, teamId, members } = $props();
  import { notifyAlert, svelteState } from "../../../../stores/store.svelte";

  const deleteTeam = async () => {
    svelteState.loading = true;
    try {
      const response = await fetch(
        `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams/${teamId}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to delete team: ${response.statusText}`);
      }

      notifyAlert("success", "Team deleted successfully.");
      window.location.reload();
    } catch (error) {
      console.error("Error deleting team:", error);
      notifyAlert("error", "Failed to delete team.");
    } finally {
      svelteState.loading = false;
    }
  };
</script>

<section>
  <h3>Members</h3>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Roll No</th>
        <th>Student ID</th>
      </tr>
    </thead>
    <tbody>
      {#each members as member}
        <tr>
          <td>{member.name}</td>
          <td>{member.roll_no}</td>
          <td>{member.student_id}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</section>
<footer>
  {#if svelteState.user.roll_no === leaderRollNo}
    <button onclick={deleteTeam}>
      <i class="fa-solid fa-trash"></i> &nbsp; Delete Team
    </button>
  {/if}
</footer>

<style>
  /* your styles go here */
</style>
