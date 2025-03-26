<script>
    import LoginForm from "./auth/LoginForm.svelte";
    import RegisterForm from "./auth/RegisterForm.svelte";

    let activeTab = "login";

    const switchTab = (tab) => {
        activeTab = tab;
    };
</script>

<article class="card">
    <div role="group" class="tabs">
        <button
            aria-current={activeTab === "login" ? "true" : "false"}
            on:click={() => switchTab("login")}
        >
            Login
        </button>
        <button
            aria-current={activeTab === "register" ? "true" : "false"}
            on:click={() => switchTab("register")}
        >
            Register
        </button>
    </div>

    {#if activeTab === "login"}
        <LoginForm />
    {:else if activeTab === "register"}
        <RegisterForm />
    {:else}
        <p>Invalid tab selected</p>
    {/if}
</article>

<style>
    article {
        flex: 5;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .tabs {
        display: flex;
        justify-content: space-around;
        margin-bottom: 1rem;
    }
</style>
