<!-- Create a 404 page -->
<script>
    import { onMount } from "svelte";
    import { navigate } from "svelte-routing";

    onMount(() => {
        const timer = setTimeout(() => {
            navigate("/");
        }, 5000);

        return () => clearTimeout(timer);
    });
</script>

<main>
    <h1>404 - Page Not Found</h1>
    <p>Sorry, the page you are looking for does not exist.</p>
    <p>You will be redirected to the home page in 5 seconds.</p>
</main>

<style>
    main {
        text-align: center;
        margin-top: 50px;
    }

    h1 {
        color: red;
    }

    p {
        font-size: 1.2em;
    }
</style>
