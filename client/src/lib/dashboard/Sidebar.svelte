<script>
  import { navigate } from "svelte-routing";

  import { svelteState } from "../../stores/store.svelte";

  // Props menuOptions and activeMenu are passed from the parent component
  let { menuOptions, activeMenu = $bindable() } = $props();

  function handleLogout() {
    // Check with alert if the user wants to log out
    if (!confirm("Are you sure you want to log out?")) {
      return;
    }

    // Clear user data from the store
    svelteState.user = null;
    localStorage.removeItem("wasLoggedIn");

    // Clear all cookies
    document.cookie.split(";").forEach((cookie) => {
      const cookieName = cookie.split("=")[0].trim();
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    });

    navigate("/");
  }
</script>

<aside class="sidebar">
  <div>
    <hgroup class="user-info">
      <h3>{svelteState.user.name || "User"}</h3>
      <h2 class="role">{svelteState.user.role.toUpperCase() || "User Role"}</h2>
    </hgroup>
    <nav class="menu">
      {#each menuOptions as option}
        <button
          class="menu-option {activeMenu === option.name ? 'active' : ''}"
          on:click={() => {
            activeMenu = option.name;
          }}
        >
          <i class="fa-solid {option.icon}"></i>
          &nbsp; {option.name}
        </button>
      {/each}
    </nav>
  </div>
  <button class="logout" on:click={handleLogout}>
    <i class="fa-solid fa-right-from-bracket"></i>
    &nbsp; Logout
  </button>
</aside>

<style>
  .sidebar {
    flex: 0 0 20%;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);

    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100vh;
  }

  .user-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .menu {
    display: flex;
    flex-direction: column;
  }

  .menu-option {
    background: none;
    border: none;
    color: #fff;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition:
      background-color 0.3s ease,
      color 0.3s ease;
  }

  .menu-option:hover {
    background-color: rgba(255, 255, 255, 0.2);
    color: #fff;
  }

  .menu-option.active {
    background-color: rgba(255, 255, 255, 0.5);
    color: #fff;
  }
</style>
