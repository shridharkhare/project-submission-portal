<script>
  import { onMount } from "svelte";
  import Sidebar from "../lib/dashboard/Sidebar.svelte";

  let classroomData = $state([]); // Initialize classroomData as an empty array

  let menuOptions = [
    { name: "Dashboard", icon: "fa-home" },
    { name: "Classrooms", icon: "fa-chalkboard-teacher" },
    { name: "Assignments", icon: "fa-tasks" },
    { name: "Attendance", icon: "fa-user-check" },
    { name: "Settings", icon: "fa-cog" },
  ];

  let activeMenu = $state("Dashboard"); // Initialize currentMenu with the default value

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
  <main class="main-content">
    {#if activeMenu === "Dashboard"}
      <h1>Dashboard</h1>

      <p>Here is your classroom data:</p>

      <section class="grid">
        {#each classroomData as classroom}
          <article class="classroom-card">
            <header>
              <hgroup>
                <h2>{classroom.branch} - Semester {classroom.semester}</h2>
                <h3>{classroom.g_id}</h3>
              </hgroup>
            </header>
            <p><strong>Division:</strong> {classroom.div}</p>
            <p><strong>Subject:</strong> {classroom.sub}</p>
            <footer>
              <small
                >Created at: {new Date(
                  classroom.created_at
                ).toLocaleString()}</small
              >
              <button
                on:click={() => {
                  console.log("Classroom ID:", classroom.g_id);
                  // Add your logic to navigate to the classroom details page
                }}>View Details</button
              >
            </footer>
          </article>
        {/each}
      </section>
    {:else if activeMenu === "Classrooms"}
      <h1>Classrooms</h1>
    {:else if activeMenu === "Assignments"}
      <h1>Assignments</h1>
    {:else if activeMenu === "Attendance"}
      <h1>Attendance</h1>
    {:else if activeMenu === "Settings"}
      <h1>Settings</h1>
    {/if}
  </main>
</main>

<style>
  .dashboard-layout {
    display: flex;
    height: 100vh;
  }

  .main-content {
    flex: 1;
    padding: 1rem;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
  }

  .classroom-card header {
    margin-bottom: 0.5rem;
  }

  .classroom-card footer {
    margin-top: 1rem;
    font-size: 0.875rem;
    color: #666;

    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
