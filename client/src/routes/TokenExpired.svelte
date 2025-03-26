<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";

    onMount(() => {
        // Redirect to the login page after 3 seconds
        const timer = setTimeout(() => {
            navigate("/");
        }, 3000);

        // Clear the timer if the component is destroyed before the timeout
        return () => clearTimeout(timer);
    });
</script>

<div class="container">
    <h1>Token Expired</h1>
    <p>Please log in again.</p>
    <a href="/" role="button" class="contrast">Back to Home</a>
</div>

<style>
    .container {
        text-align: center;
        margin-top: 20vh;
    }
</style>
