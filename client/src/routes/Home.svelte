<script>
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing";
  import { svelteState } from "../stores/store.svelte";
  import LoginRegisterCard from "./../lib/landing/LoginRegisterCard.svelte";
  import WelcomeMessage from "./../lib/landing/WelcomeMessage.svelte";

  onMount(() => {
    // Check if the user is already logged in
    if (svelteState.user) {
      // Redirect to the dashboard if logged in
      navigate("/dashboard");
    }
  });
</script>

<main class="container">
  <div class="grid">
    <WelcomeMessage />
    <LoginRegisterCard />
  </div>
</main>

<style>
  .container {
    min-height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .grid {
    width: 100%;
  }
</style>
