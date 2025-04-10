<script>
    let { activeClassroom, activeMenu } = $props();

    import { notifyAlert, svelteState } from "../../../stores/store.svelte.js";
    import { convertDateToHumanReadable } from "../../utils/date.js";

    const getAllTeamsFromClassroom = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms/${activeMenu}/submissions`,
                {
                    method: "GET",
                    credentials: "include",
                }
            );
            const data = await response.json();
            console.log(data);
            if (response.status === 404) {
                notifyAlert(
                    "info",
                    "No teams are available for this classroom."
                );
                return [];
            }
            if (!response.ok) {
                throw new Error(data.message || "Failed to fetch teams");
            }

            return data;
        } catch (error) {
            // If the error is a 404, we can handle it gracefully
            if (error.response && error.response.status === 404) {
                notifyAlert(
                    "info",
                    "No teams are available for this classroom."
                );
                return [];
            } else {
                notifyAlert(
                    "error",
                    error.message || "An error occurred while fetching teams"
                );
            }
        }
    };
</script>

<main class="container">
    <header class="sticky-header">
        <hgroup class="left">
            <h1>{activeClassroom.sub}</h1>
            <h2>{activeMenu}</h2>
        </hgroup>
        <hgroup class="right">
            <h3>Taught By {svelteState.user.name}</h3>
            <h4>
                Created On {convertDateToHumanReadable(
                    activeClassroom.created_at
                )}
            </h4>
        </hgroup>
    </header>
    <section>
        {#await getAllTeamsFromClassroom()}
            <article aria-busy="true"></article>
        {:then teams}
            {#if teams?.length === 0}
                <article>
                    <p>No teams found for this classroom.</p>
                </article>
            {:else}
                {#each teams as team (team.team_id)}
                    <article>
                        <header>
                            <hgroup>
                                <h3>{team.team_details.topic}</h3>
                                <h4>{team.team_details.team_id}</h4>
                            </hgroup>
                        </header>
                        <!-- Basic details table -->
                        <table>
                            <tbody>
                                <tr>
                                    <td>Team No</td>
                                    <td>{team.team_details.team_no}</td>
                                </tr>
                                <tr>
                                    <td>Leader Name</td>
                                    <td>
                                        {#each team.team_details.members as member}
                                            {#if member.student_id === team.leader_id}
                                                {member.name}
                                            {/if}
                                        {/each}
                                    </td>
                                </tr>
                                <tr>
                                    <td>Leader ID</td>
                                    <td>{team.leader_id}</td>
                                </tr>
                                <tr>
                                    <td>No Members</td>
                                    <td>{team.team_details.no_members}</td>
                                </tr>
                                <tr>
                                    <td>Division</td>
                                    <td>{team.team_details.div}</td>
                                </tr>
                            </tbody>
                        </table>

                        <details>
                            <summary>Team Members</summary>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Student ID</th>
                                        <th>Roll No</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {#each team.team_details.members as member}
                                        <tr>
                                            <td>{member.name}</td>
                                            <td>{member.student_id}</td>
                                            <td>{member.roll_no}</td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </details>

                        <!-- Links as buttons -->
                        <div class="links grid">
                            {#if team.github_url}
                                <button
                                    onclick={() => {
                                        window.open(team.github_url, "_blank");
                                    }}
                                    class="button"
                                >
                                    <i class="fab fa-github"></i> &nbsp; GitHub
                                </button>
                            {:else}
                                <p>
                                    <i class="fas fa-exclamation-triangle"></i>
                                    &nbsp; No GitHub URL provided
                                </p>
                            {/if}
                            {#if team.ppt_url}
                                <button
                                    onclick={() => {
                                        window.open(team.ppt_url, "_blank");
                                    }}
                                    class="button"
                                >
                                    <i class="fas fa-file-powerpoint"></i> &nbsp;
                                    PPT
                                </button>
                            {:else}
                                <p>
                                    <i class="fas fa-exclamation-triangle"></i>
                                    &nbsp; No PPT URL provided
                                </p>
                            {/if}
                            {#if team.report_url}
                                <button
                                    onclick={() => {
                                        window.open(team.report_url, "_blank");
                                    }}
                                    class="button"
                                >
                                    <i class="fas fa-file-alt"></i> &nbsp; Report
                                </button>
                            {:else}
                                <p>
                                    <i class="fas fa-exclamation-triangle"></i>
                                    &nbsp; No Report URL provided
                                </p>
                            {/if}
                        </div>
                        <footer>
                            <small>
                                Created At: {convertDateToHumanReadable(
                                    team.created_at
                                )}
                            </small>
                        </footer>
                    </article>
                {/each}
            {/if}
        {:catch error}
            <p>Error: {error.message}</p>
        {/await}
    </section>
</main>

<style>
    main {
        padding: 0.5rem;
        height: 100vh;
        overflow: none;
    }

    header.sticky-header {
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

    header.sticky-header hgroup {
        margin: 0;
    }

    header.sticky-header hgroup.left {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    header.sticky-header hgroup.right {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        text-align: right;
    }

    header.sticky-header hgroup.right h3 {
        font-size: 1rem;
    }
    header.sticky-header hgroup.right h4 {
        font-size: 0.8rem;
    }

    section {
        padding: 0.5rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .links {
        display: flex;
        flex-direction: row;
        gap: 1rem;
        justify-content: space-between;
        align-items: center;
        border: 1px solid var(--pico-primary-border);
        padding: 0.5rem;
        border-radius: 4px;
    }

    .links p {
        margin: 0;
        font-size: 0.8rem;
        color: var(--pico-text-color);
    }

    .links button {
        flex: 1;
    }

    details {
        background-color: var(--pico-background-color);
        margin-bottom: 1rem;
        padding: 0.7rem;
        border: 1px solid var(--pico-primary-border);
        border-radius: 4px;
    }

    summary {
        font-weight: bold;
        cursor: pointer;
    }
</style>
