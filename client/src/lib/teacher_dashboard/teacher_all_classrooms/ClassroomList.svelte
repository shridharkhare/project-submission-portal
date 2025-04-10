<script>
    let { data, activeMenu = $bindable() } = $props();
    import { convertDateToHumanReadable } from "../../utils/date";
</script>

{#each data as classroom}
    <article class="classroom-card">
        <header>
            <h2>{classroom.sub}</h2>
            <p>{classroom.g_id}</p>
        </header>
        <div class="overflow-auto">
            <table>
                <tbody>
                    <tr>
                        <td><strong>Created At:</strong></td>
                        <td
                            >{convertDateToHumanReadable(
                                classroom.created_at
                            )}</td
                        >
                    </tr>
                </tbody>
            </table>
        </div>
        <footer>
            <button onclick={() => (activeMenu = classroom.g_id)}>
                View Classroom
            </button>
        </footer>
    </article>
{/each}

<style>
    h2 {
        font-size: 1.5rem;
        margin: 0;
    }

    p {
        font-size: 1rem;
        margin: 0.5rem 0;
    }

    article {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
