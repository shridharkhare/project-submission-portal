<script>
    import CreateClassroom from "./CreateClassroom.svelte";

    import AddStudentsList from "./AddStudentsList.svelte";
    import ClassroomList from "./ClassroomList.svelte";

    let { classroomData, activeMenu = $bindable() } = $props();
    let activeTab = $state("classrooms");
</script>

<section class="container">
    <!-- Tab Buttons -->
    <div role="group">
        <button
            aria-current={activeTab === "classrooms"}
            onclick={() => (activeTab = "classrooms")}
        >
            <i class="fa-solid fa-chalkboard-teacher"></i>&nbsp; Classrooms
        </button>
        <button
            aria-current={activeTab === "add-students"}
            onclick={() => (activeTab = "add-students")}
        >
            <i class="fa-solid fa-user-plus"></i>&nbsp; Add Students
        </button>
    </div>

    {#if activeTab === "classrooms"}
        <section>
            <h1>Classrooms you have created</h1>
            <div class="classroom-list">
                {#await classroomData}
                    <p>Loading classrooms...</p>
                {:then data}
                    {#if data.length === 0}
                        <p>No classrooms found.</p>
                    {:else}
                        <ClassroomList {data} bind:activeMenu />
                    {/if}
                {:catch error}
                    <p>Error loading classrooms: {error.message}</p>
                {/await}
            </div>
            <CreateClassroom />
        </section>
    {/if}

    {#if activeTab === "add-students"}
        <section>
            <AddStudentsList />
        </section>
    {/if}
</section>

<style>
    section {
        padding: 0.5rem;
        overflow: none;
    }

    p {
        font-size: 1rem;
        margin: 0.5rem 0;
    }

    button[aria-current="true"] {
        font-weight: bold;
    }

    .classroom-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
        gap: 1rem;
    }
</style>
