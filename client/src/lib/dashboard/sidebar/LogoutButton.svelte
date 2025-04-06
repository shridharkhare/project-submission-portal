<script>
  import { navigate } from "svelte-routing";
  import { svelteState } from "../../../stores/store.svelte";
  import ThemeToggle from "./ThemeToggle.svelte";

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

<div class="flex">
  <ThemeToggle />
  <button class="logout" onclick={handleLogout}>
    <i class="fa-solid fa-right-from-bracket"></i>
    &nbsp; Logout
  </button>
</div>

<style>
  .flex {
    display: flex;
    align-items: center;
  }
  
  .logout {
    margin-left: 0.5rem;
    flex: 1;
  }
</style>
