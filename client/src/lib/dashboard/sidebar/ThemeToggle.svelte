<script>
  import { onMount } from "svelte";

  let savedTheme = $state("light");

  onMount(() => {
    const prefferedTheme = window.matchMedia("(prefers-color-scheme: dark)")
      .matches
      ? "dark"
      : "light";
    savedTheme = localStorage.getItem("theme") || prefferedTheme;
    document.documentElement.setAttribute("data-theme", savedTheme);
  });

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    savedTheme = newTheme;
  }
</script>

<button class="theme-toggle" onclick={toggleTheme}>
  {#if savedTheme === "dark"}
    <i class="fa-solid fa-sun"></i>
  {:else}
    <i class="fa-solid fa-moon"></i>
  {/if}
</button>

<style>
  /* your styles go here */
</style>
