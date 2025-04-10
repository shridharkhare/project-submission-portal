<script>
    import LogoutButton from "./LogoutButton.svelte";
    import UserInfo from "./UserInfo.svelte";

    import { svelteState } from "../../../stores/store.svelte.js";

    const role = svelteState.user.role;

    // Props menuOptions and activeMenu are passed from the parent component
    let { menuOptions, activeMenu = $bindable() } = $props();
</script>

<aside class="sidebar">
    <div>
        <UserInfo />
        <nav class="menu">
            {#if menuOptions.length === 0}
                {#if role === "student"}
                    <p>You have not been added in any project classroom yet.</p>
                {:else if role === "teacher"}
                    <p>You have not created any project classroom yet.</p>
                {/if}
            {:else}
                {#each menuOptions as option}
                    <button
                        class="menu-option {activeMenu === option.id
                            ? 'active'
                            : ''}"
                        onclick={() => {
                            activeMenu = option.id;
                        }}
                    >
                        {#if option.id === "dashboard"}
                            <i class="fa-solid fa-house"></i>
                        {:else}
                            <i class="fa-solid fa-chalkboard-user"></i>
                        {/if}
                        <div class="flex-column">
                            <h6>{option.subject}</h6>
                            {#if option.id != "dashboard"}
                                <p>{option.id}</p>
                            {/if}
                        </div>
                    </button>
                {/each}
            {/if}
        </nav>
    </div>

    <LogoutButton />
</aside>

<style>
    .sidebar {
        flex: 0 0 20%;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

        border-radius: 0 0.5rem 0.5rem 0;

        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100vh;
    }

    .menu {
        display: flex;
        flex-direction: column;
    }

    .menu-option {
        position: relative;
        margin-bottom: 0.25rem;
        background: none;
        border: none;
        padding: 0.25rem 0.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition:
            background-color 0.3s ease,
            color 0.3s ease;
    }

    .menu-option:hover {
        background-color: rgba(0, 94, 255, 0.2);
    }

    .menu-option.active {
        background-color: rgba(0, 94, 255, 0.5);
    }

    .menu-option i {
        font-size: 1.2rem;
    }

    .menu-option h6 {
        font-size: 1rem;
        margin: 0;
    }

    .menu-option p {
        font-size: 0.6rem;
        margin: 0;
    }

    .flex-column {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: start;
    }
</style>
