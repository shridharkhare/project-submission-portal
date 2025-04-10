<script>
    import { onMount } from "svelte";
    import Sidebar from "../lib/dashboard/sidebar/Sidebar.svelte";

    import TeacherAllClassrooms from "../lib/teacher_dashboard/teacher_all_classrooms/TeacherAllClassrooms.svelte";
    import TeacherClassroom from "../lib/teacher_dashboard/teacher_classroom/TeacherClassroom.svelte";

    let classroomData = $state([]);

    let menuOptions = $state([
        {
            subject: "Dashboard",
            id: "dashboard",
        },
    ]);

    let activeMenu = $state("dashboard");

    const findClassroomById = (id) => {
        return classroomData.find((classroom) => classroom.g_id === id);
    };

    let activeClassroom = $derived(findClassroomById(activeMenu));

    const setMenuOptionsWithClassrooms = (/** @type {any[]} */ classrooms) => {
        menuOptions = [
            ...menuOptions,
            ...classrooms.map((classroom) => ({
                subject: classroom.sub,
                id: classroom.g_id,
            })),
        ];
    };

    const getClassroomData = async () => {
        const response = await fetch(
            `${import.meta.env.VITE_SERVER_URL}/api/v1/g_classrooms`,
            {
                method: "GET",
                credentials: "include",
            }
        );
        if (response.ok) {
            classroomData = await response.json();
            if (classroomData.length === 0) {
                console.error("No classrooms found");
                return;
            }
            setMenuOptionsWithClassrooms(classroomData);
        } else {
            console.error("Failed to fetch classroom data");
        }
    };

    // This function will run when the component is mounted
    onMount(() => {
        console.log("Dashboard component mounted");
        getClassroomData();

        return () => {
            console.log("Dashboard component unmounted");
        };
    });
</script>

<main class="dashboard-layout">
    <Sidebar {menuOptions} bind:activeMenu />
    <div class="main-content">
        {#if activeMenu && activeMenu == "dashboard"}
            <TeacherAllClassrooms {classroomData} bind:activeMenu />
        {:else}
            <TeacherClassroom {activeClassroom} {activeMenu} />
        {/if}
    </div>
</main>

<style>
    .dashboard-layout {
        display: flex;
        height: 100vh;
    }

    .main-content {
        flex: 1;
        height: 100%;
        overflow-y: auto;
    }
</style>
