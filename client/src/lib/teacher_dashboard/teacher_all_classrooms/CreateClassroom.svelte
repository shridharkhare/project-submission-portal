<script>
    let showCreateClassroomDialog = $state(false);

    import { notifyAlert, svelteState } from "../../../stores/store.svelte";

    let subjects = $state([]);
    let branch = $state("CE");
    let semester = $state(0);
    let div = $state("A");
    let selectedSubject = $state("");

    // Function to handle the creation of a new classroom
    const createClassroom = async (event) => {
        event.preventDefault();
        svelteState.loading = true;

        const classroomDetails = {
            branch,
            semester,
            div: div,
            sub: selectedSubject,
        };

        try {
            const response = await fetch(
                `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                    body: JSON.stringify(classroomDetails),
                }
            );

            if (response.ok) {
                notifyAlert("Classroom created successfully", "success");
                showCreateClassroomDialog = false;
                window.location.reload();
            } else {
                const errorData = await response.json();
                notifyAlert(
                    errorData.message || "Failed to create classroom",
                    "error"
                );
            }
        } catch (error) {
            notifyAlert(
                "An error occurred while creating the classroom",
                "error"
            );
            console.error(error);
        } finally {
            svelteState.loading = false;
        }
    };

    const getSubjects = async () => {
        try {
            const response = await fetch(
                `${import.meta.env.VITE_SERVER_URL}/api/v1/subjects?branch=${branch}&semester=${semester}`,
                {
                    method: "GET",
                    credentials: "include",
                }
            );
            if (response.ok) {
                const data = await response.json();
                subjects = data.data;
                if (subjects.length === 0) {
                    notifyAlert(
                        "No subjects found for the selected criteria",
                        "info"
                    );
                }
            } else {
                notifyAlert("Failed to fetch subjects", "error");
            }
        } catch (error) {
            notifyAlert("An error occurred while fetching subjects", "error");
            console.error(error);
        }
    };
</script>

<div>
    <button
        class="create-classroom-button"
        onclick={() => (showCreateClassroomDialog = true)}
    >
        <i class="fa-solid fa-plus"></i>&nbsp; Create New Classroom
    </button>

    <dialog open={showCreateClassroomDialog}>
        <article>
            <header class="dialog-header">
                <h2>Create New Classroom</h2>
                <button
                    aria-label="Close"
                    onclick={() => (showCreateClassroomDialog = false)}
                >
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </header>
            <form>
                <div class="grid">
                    <label>
                        Branch
                        <select bind:value={branch} onchange={getSubjects}>
                            <option value="CE">CE</option>
                            <option value="IT">IT</option>
                            <option value="MECH">MECH</option>
                            <option value="EXTC">EXTC</option>
                        </select>
                    </label>

                    <label>
                        Semester
                        <select bind:value={semester} onchange={getSubjects}>
                            {#each Array(8)
                                .fill(0)
                                .map((_, i) => i + 1) as sem}
                                <option value={sem}>{sem}</option>
                            {/each}
                        </select>
                    </label>
                </div>

                <label>
                    Division:
                    <select bind:value={div}>
                        {#each ["A", "B", "C", "D", "E"] as division}
                            <option value={division}>{division}</option>
                        {/each}
                    </select>
                </label>

                {#if subjects?.length > 0}
                    <label>
                        Subject
                        <select bind:value={selectedSubject}>
                            <option value="" disabled selected
                                >Select Subject</option
                            >
                            {#each subjects as subject}
                                <option value={subject.subject_acronym}>
                                    {subject.subject_name} ({subject.subject_acronym})
                                </option>
                            {/each}
                        </select>
                    </label>
                {/if}
            </form>
            <footer>
                <button type="submit" onclick={createClassroom}>
                    <i class="fa-solid fa-plus"></i>&nbsp; Create Classroom
                </button>
            </footer>
        </article>
    </dialog>
</div>

<style>
    p {
        font-size: 1rem;
        margin: 0.5rem 0;
    }

    .create-classroom-button {
        background-color: #4caf50; /* Green */
        border: none;
        position: absolute;
        bottom: 1rem;
        right: 1rem;
        border-radius: 50px;
    }

    .dialog-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .dialog-header button {
        background: none;
        border: none;
        cursor: pointer;
    }
</style>
