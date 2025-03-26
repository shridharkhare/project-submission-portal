<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";
    import { svelteState } from "../../stores/store.svelte.js";

    import Home from "../../routes/Home.svelte";

    export let component;
    export let id;

    onMount(() => {
        // If user is not logged in, redirect to home page
        if (!svelteState.user) {
            navigate("/");
        }
    });
</script>

{#if svelteState.user}
    <svelte:component this={component} {id} location={null} />
{:else}
    <svelte:component this={Home} />
{/if}
