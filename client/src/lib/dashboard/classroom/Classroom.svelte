<script>
    let { activeClassroom, activeMenu } = $props();

    import { convertDateToHumanReadable } from "../../utils/date.js";

    import { notifyAlert } from "../../../stores/store.svelte.js";

    import CreateTeamForm from "./create-team/CreateTeamForm.svelte";
    import Team from "./team/Team.svelte";
    import TeamRequests from "./team/TeamRequests.svelte";

    let teamData = $state(null);

    const checkIfUserInTeamInThisClassroom = async (
        /** @type {any} */ g_id
    ) => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${g_id}/teams`,
                {
                    method: "GET",
                    credentials: "include",
                }
            );

            const data = await response.json();
            if (!response.ok) {
                notifyAlert("error", `Error fetching teams: ${data.message}`);
                return null;
            }
            return data;
        } catch (error) {
            console.error("An error occurred while fetching team data:", error);
            return null;
        }
    };
</script>

<main class="container">
    <header>
        <hgroup class="left">
            <h1>{activeClassroom.sub}</h1>
            <h2>{activeMenu}</h2>
        </hgroup>
        <hgroup class="right">
            <h3>Taught By {activeClassroom.teacher}</h3>
            <h4>
                Created On {convertDateToHumanReadable(
                    activeClassroom.created_at
                )}
            </h4>
        </hgroup>
    </header>
    <section>
        {#await checkIfUserInTeamInThisClassroom(activeClassroom.g_id)}
            <p>Loading...</p>
        {:then data}
            {#if data}
                <Team {activeClassroom} {data} />
            {:else}
                <div>
                    <h3>No Teams Found</h3>
                    <p>
                        You are not part of any team in this classroom. Either
                        create a team or wait for a request from another team.
                    </p>
                </div>
                <div class="grid">
                    <CreateTeamForm {activeClassroom} />
                    <TeamRequests g_id={activeClassroom.g_id} />
                </div>
            {/if}
        {:catch error}
            <div>
                <h3>Error</h3>
                <p>
                    There was an error fetching the team data: {error.message}
                </p>
            </div>
        {/await}
    </section>
</main>

<style>
    main {
        padding: 0.5rem;
        overflow: auto;
        height: 100vh;
    }
    header {
        padding: 0.5rem;
        position: sticky;
        top: 0;
        z-index: 1;
        /* Frost Effect */
        backdrop-filter: blur(20px);
        border-radius: 0.5rem 0.5rem 0 0;

        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    header hgroup {
        margin: 0;
    }

    header hgroup.left {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    header hgroup.right {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        text-align: right;
    }

    header hgroup.right h3 {
        font-size: 1rem;
    }
    header hgroup.right h4 {
        font-size: 0.8rem;
    }

    section {
        padding: 0.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
</style>
