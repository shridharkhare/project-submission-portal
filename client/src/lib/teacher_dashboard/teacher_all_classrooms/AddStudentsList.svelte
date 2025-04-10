<script>
    import GetStudentList from "./GetStudentList.svelte";

    import { notifyAlert, svelteState } from "../../../stores/store.svelte";

    let studentList = $state(null);
    let classroom = $state({
        branch: "",
        semester: "",
        division: "",
    });
    let studentsCSVUploaded = $state(false);
    let studentsCSV = $state(null);
    let csvFile = $state(null);

    const handleFileChange = (event) => {
        csvFile = event.target.files[0];
    };
    const checkCSVHeaders = (headers) => {
        const requiredHeaders = ["student_id", "name", "email"];
        return (
            headers.length === requiredHeaders.length &&
            requiredHeaders.every((header) => headers.includes(header))
        );
    };

    const handleCSVUpload = async (event) => {
        event.preventDefault();

        if (!csvFile) {
            notifyAlert("error", "Please select a CSV file.");
            return;
        }

        try {
            const text = await csvFile.text();
            const rows = text.split("\n").filter((row) => row.trim() !== "");
            const headers = rows[0].split(",").map((header) => header.trim());

            if (!checkCSVHeaders(headers)) {
                notifyAlert(
                    "error",
                    "Invalid CSV format. Ensure it has exactly 3 columns: student_id, name, email."
                );
                return;
            }

            const data = rows.slice(1).map((row) => {
                const values = row.split(",").map((value) => value.trim());
                return headers.reduce((acc, header, index) => {
                    acc[header] = values[index];
                    return acc;
                }, {});
            });

            studentsCSV = data;
            studentsCSVUploaded = true;
            notifyAlert("success", "CSV uploaded and parsed successfully!");
        } catch (error) {
            console.error("Error parsing CSV file:", error);
            notifyAlert("error", "Failed to parse CSV file.");
        }
    };

    const postCSVData = async () => {
        svelteState.loading = true;
        try {
            const response = await fetch(
                `${import.meta.env.VITE_SERVER_URL}/api/v1/students`,
                {
                    method: "POST",
                    body: (() => {
                        const formData = new FormData();
                        formData.append("file", csvFile);
                        const metadata = {
                            year: Math.ceil(parseInt(classroom.semester) / 2),
                            branch: classroom.branch,
                            div: classroom.division,
                            semester: classroom.semester,
                        };
                        formData.append("metadata", JSON.stringify(metadata));
                        return formData;
                    })(),
                    credentials: "include",
                }
            );

            if (!response.ok) {
                throw new Error("Failed to add students");
            }

            const result = await response.json();
            notifyAlert("success", result.message);
        } catch (error) {
            console.error("Error adding students:", error);
            notifyAlert("error", "Failed to add students.");
        } finally {
            svelteState.loading = false;
            studentsCSVUploaded = false;
            studentsCSV = null;
        }
    };
</script>

<div class="container">
    <h1>Add student list for a division</h1>
    <GetStudentList bind:studentList bind:classroom />

    {#if studentList}
        <article>
            <h2>Students</h2>
            {#if studentList.length > 0}
                <div class="overflow-auto">
                    <table>
                        <thead>
                            <tr>
                                <th>Student ID</th>
                                <th>Name</th>
                                <th>Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each studentList as student}
                                <tr>
                                    <td>{student.student_id}</td>
                                    <td>{student.name}</td>
                                    <td>{student.email}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
                <p>
                    <strong>Note:</strong> The above list is fetched from the database.
                    You can add students to this list by uploading a CSV file.
                </p>
            {:else}
                <p>No students found.</p>
            {/if}
        </article>

        <article>
            <form onsubmit={handleCSVUpload}>
                <label class="flex-row">
                    Upload CSV
                    <input
                        type="file"
                        accept=".csv"
                        onchange={handleFileChange}
                    />
                </label>

                <button type="submit">
                    <i class="fa-solid fa-file-upload"></i> &nbsp;
                    {#if studentList.length > 0}
                        Overwrite these details with my CSV
                    {:else}
                        Add students from CSV
                    {/if}
                </button>
                
                <span>
                    Note: The CSV must have headers: <strong
                        >student_id, name, email</strong
                    >
                </span>
            </form>
        </article>
    {/if}

    <dialog id="csvUploadDialog" open={studentsCSVUploaded}>
        <article>
            <header class="dialog-header">
                <p>
                    <strong
                        >❗Are you sure you want to add these students?</strong
                    >
                </p>
                <button
                    aria-label="Close"
                    onclick={() => (studentsCSVUploaded = false)}
                >
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </header>
            <p>The following students will be added to:</p>
            <p>
                <strong>
                    {classroom.branch} | Semester {classroom.semester} | Division
                    {classroom.division}
                </strong>
            </p>
            <div class="overflow-auto">
                <table>
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Name</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each studentsCSV as student}
                            <tr>
                                <td>{student.student_id}</td>
                                <td>{student.name}</td>
                                <td>{student.email}</td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            </div>
            <footer>
                <button
                    class="btn btn-primary"
                    type="button"
                    onclick={postCSVData}
                >
                    Add Students
                </button>
                <button
                    class="btn btn-secondary"
                    type="button"
                    onclick={() => (studentsCSVUploaded = false)}
                >
                    Cancel
                </button>
            </footer>
        </article>
    </dialog>
</div>

<style>
    .container {
        padding: 1rem;
    }

    .flex-row {
        display: flex;
        align-items: center;
        gap: 1rem;
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
