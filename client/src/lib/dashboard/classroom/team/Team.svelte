<script>
  let { activeClassroom, data } = $props();
  import { convertDateToHumanReadable } from "../../../utils/date";
  import Submission from "./Submission.svelte";
  import TeamMembers from "./TeamMembers.svelte";

  let activeTab = $state("teamMembers");

  const leaderName =
    data.members.find((member) => member.student_id === data.leader_id)?.name ||
    "N/A";
  const leaderRollNo =
    data.members.find((member) => member.student_id === data.leader_id)
      ?.roll_no || "N/A";
</script>

<div>
  <header>
    <hgroup>
      <h2>{data.topic}</h2>
      <p><strong>{activeClassroom.sub} - </strong> Team {data.team_no}</p>
    </hgroup>
    <small>
      Created by
      {leaderName} at {convertDateToHumanReadable(data.created_at)}
    </small>
  </header>
  <hr />

  <div>
    <div role="group" aria-label="Team Tabs">
      <button
        onclick={() => (activeTab = "teamMembers")}
        aria-current={activeTab === "teamMembers"}
      >
        <i class="fa-solid fa-users"></i> &nbsp;{data.members.length}{" "}
        {data.members.length === 1 ? "Member" : "Members"} &nbsp;
      </button>
      <button
        onclick={() => (activeTab = "submissions")}
        aria-current={activeTab === "submissions"}
      >
        <i class="fa-solid fa-file-export"></i> &nbsp;Submissions
      </button>
    </div>

    {#if activeTab === "teamMembers"}
      <TeamMembers
        {leaderRollNo}
        g_id={activeClassroom.g_id}
        teamId={data.team_id}
        members={data.members}
      />
    {/if}

    {#if activeTab === "submissions"}
      <Submission
        leader_id={data.leader_id}
        g_id={activeClassroom.g_id}
        teamId={data.team_id}
      />
    {/if}
  </div>
</div>

<style>
  button[aria-current="true"] {
    font-size: 1.2rem;
  }
</style>
