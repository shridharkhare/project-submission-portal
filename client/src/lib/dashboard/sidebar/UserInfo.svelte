<script>
  // your script goes here
  import { svelteState } from "../../../stores/store.svelte";
</script>

<div class="user-info">
  <div class="flex">
    <h3>{svelteState.user.name || "User"}</h3>
    <kbd>{svelteState.user.branch || "Branch"}</kbd>
  </div>
  <p>
    Semester {svelteState.user.semester || "0"} | {svelteState.user.div || "Z"} -
    {svelteState.user.roll_no || "0"}
  </p>
</div>

<style>
  .user-info {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    background-color: rgba(255, 255, 255, 0.185);
    border-radius: 0.5rem;
    padding: 0.25rem 0.5rem;
    margin-bottom: 0.5rem;
  }

  .flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  h3 {
    margin-bottom: 0;
  }

  p {
    margin: 0;
    font-size: 0.8rem;
    color: var(--text-color);
  }
</style>
