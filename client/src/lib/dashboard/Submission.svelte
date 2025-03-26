<script>
  import { onMount } from "svelte";
  import { navigate } from "svelte-routing";
  import Loader from "./Loader.svelte";
  
  export let mode = "projects"; // "projects" or "submissions"
  export let projectId = null;
  export let subjectCode = null;
  export let projectName = "";
  export let submissions = []; // Add this prop to receive submissions data
  export let onBack = (id) => {
    if (id) {
      // Handle project selection
      navigate(`/submission/${id}`);
    } else {
      // Handle back navigation
      navigate('/dashboard');
    }
  };
  
  let items = [];
  let loading = true;
  let error = null;
  
  onMount(async () => {
    try {
      // Simulated API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (mode === "projects") {
        // Mock project data
        items = [
          {
            id: "1",
            name: "Web Development Project",
            subjectCode: "CS101",
            createdAt: "2023-09-01",
            deadline: "2023-10-15"
          },
          {
            id: "2",
            name: "Mobile App Development",
            subjectCode: "CS101",
            createdAt: "2023-09-05",
            deadline: "2023-10-20"
          },
          {
            id: "3",
            name: "Database Design Project",
            subjectCode: "CS102",
            createdAt: "2023-09-10",
            deadline: "2023-11-01"
          },
          {
            id: "4",
            name: "Machine Learning Assignment",
            subjectCode: "CS102",
            createdAt: "2023-09-15",
            deadline: "2023-11-10"
          }
        ];
        
        // Filter by subjectCode if provided
        if (subjectCode) {
          items = items.filter(item => item.subjectCode === subjectCode);
        }
      } else if (mode === "submissions") {
        // Use the actual submissions data passed from parent
        items = submissions;
      }
      
      loading = false;
    } catch (err) {
      error = `Failed to load ${mode}`;
      loading = false;
    }
  });
  
  function handleCardClick(id) {
    if (mode === "projects") {
      // Navigate to submissions for this project
      onBack(id);
    } else if (mode === "submissions") {
      // View submission details
      // This could navigate to a detailed view or open a modal
      console.log(`View submission ${id}`);
    }
  }
  
  function formatDate(dateString) {
    return dateString ? new Date(dateString).toLocaleDateString() : "N/A";
  }
</script>

<div class="submissions-container">
  {#if mode === "submissions"}
    <div class="back-navigation">
      <button class="outline" on:click={() => onBack()}>← Back to Projects</button>
      <h2>Submissions for {projectName}</h2>
    </div>
  {:else}
    <h2>Your Projects</h2>
  {/if}
  
  {#if loading}
    <Loader />
  {:else if error}
    <div class="error-message">
      <p>{error}</p>
      <button on:click={() => window.location.reload()}>Retry</button>
    </div>
  {:else if items.length === 0}
    <div class="empty-state">
      <p>{mode === "submissions" ? "No student submissions have been made yet." : "No projects found."}</p>
    </div>
  {:else}
    <div class="card-grid">
      {#each items as item}
        <button 
          class="card" 
          on:click={() => handleCardClick(item.id)}
          type="button"
        >
          {#if mode === "projects"}
            <h3>{item.name}</h3>
            <p>Subject: {item.subjectCode}</p>
            <p>Deadline: {formatDate(item.deadline)}</p>
          {:else}
            <h3>{item.studentName}</h3>
            <p>Roll Number: {item.rollNumber}</p>
            <p>Status: <span class={item.status === "Submitted" ? "status-submitted" : "status-pending"}>{item.status}</span></p>
            {#if item.submittedAt}
              <p>Submitted: {formatDate(item.submittedAt)}</p>
            {/if}
          {/if}
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .submissions-container {
    padding: 1rem 0;
  }
  
  .empty-state {
    text-align: center;
    padding: 2rem;
    background: #1e1e1e;
    border-radius: 8px;
    margin-top: 2rem;
  }
  
  .back-navigation {
    margin-bottom: 1.5rem;
  }
  
  .status-submitted {
    color: #4caf50;
    font-weight: bold;
  }
  
  .status-pending {
    color: #ff9800;
    font-weight: bold;
  }
</style>

