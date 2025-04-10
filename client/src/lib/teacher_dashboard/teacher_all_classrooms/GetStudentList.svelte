<script>
    import { notifyAlert, svelteState } from "../../../stores/store.svelte";
    let { studentList = $bindable(), classroom = $bindable() } = $props();

    const getStudentsByDivision = async (event) => {
        event.preventDefault();
        svelteState.loading = true;

        try {
            const formData = new FormData(event.target);
            const branch = formData.get("branch");
            const semester = formData.get("semester");
            const division = formData.get("division");

            classroom = { branch, semester, division };

            const response = await fetch(
                `${import.meta.env.VITE_SERVER_URL}/api/v1/students?branch=${branch}&semester=${semester}&div=${division}`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                }
            );

            if (response.ok) {
                const data = await response.json();
                studentList = data.data.length > 0 ? data.data : [];
                notifyAlert("success", "Students fetched successfully!");
            } else {
                throw new Error("Failed to fetch students.");
            }
        } catch (error) {
            notifyAlert("error", error.message);
        } finally {
            svelteState.loading = false;
        }
    };
</script>

<form onsubmit={getStudentsByDivision}>
    <fieldset>
        <legend>Division Details</legend>
        <div class="grid">
            <label>
                Branch
                <select name="branch">
                    <option value="CE">CE</option>
                    <option value="IT">IT</option>
                    <option value="MECH">MECH</option>
                    <option value="EXTC">EXTC</option>
                </select>
            </label>

            <label>
                Semester
                <select id="semester" name="semester">
                    {#each Array(8)
                        .fill(0)
                        .map((_, i) => i + 1) as semester}
                        <option value={semester}>{semester}</option>
                    {/each}
                </select>
            </label>

            <label>
                Division
                <select name="division">
                    {#each ["A", "B", "C", "D", "E"] as division}
                        <option value={division}>{division}</option>
                    {/each}
                </select>
            </label>
        </div>
    </fieldset>

    <button type="submit">
        <i class="fa-solid fa-database"></i> &nbsp; Check for Students
    </button>
</form>

<style>
    fieldset {
        border: 1px solid;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    legend {
        padding: 0 0.5rem;
    }
</style>
