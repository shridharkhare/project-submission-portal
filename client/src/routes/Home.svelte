<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { svelteState } from "../stores/store.svelte";
    import WelcomeMessage from "./../lib/landing/WelcomeMessage.svelte";
    import LoginRegisterCard from "./../lib/landing/LoginRegisterCard.svelte";

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
        padding: 2rem;
        min-height: 100vh;
        width: 100vw;
    }
</style>
