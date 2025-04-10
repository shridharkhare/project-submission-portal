<script>
    import "@picocss/pico";
    import { onMount } from "svelte";
    import { Route, Router, navigate } from "svelte-routing";

    import { notifyAlert, svelteState } from "./stores/store.svelte.js";

    import Loading from "./lib/utils/Loading.svelte";
    import ProtectedRoute from "./lib/utils/ProtectedRoute.svelte";

    import SnackBarAlert from "./lib/utils/SnackBarAlert.svelte";
    import Dashboard from "./routes/Dashboard.svelte";
    import Home from "./routes/Home.svelte";
    import NotFound from "./routes/NotFound.svelte";
    import TeacherDashboard from "./routes/TeacherDashboard.svelte";

    const getUserByCookie = async () => {
        svelteState.loading = true;
        try {
            const res = await fetch(
                `${import.meta.env.VITE_SERVER_URL}/api/v1/users/me`,
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                }
            );

            if (res.status === 200) {
                const data = await res.json();
                return data;
            } else if (res.status === 401) {
                // Clear the cookie
                deleteCookie("access_token");
                svelteState.loading = false;
                notifyAlert("info", "Session expired. Please log in again.");
            } else {
                const data = await res.json();
                if (data.error) {
                    svelteState.loading = false;
                    notifyAlert("error", data.error);
                } else {
                    svelteState.loading = false;
                    notifyAlert("error", "An unknown error occurred.");
                }
            }
        } catch (error) {
            svelteState.loading = false;
            notifyAlert("info", "There is no user logged in.");
        } finally {
            svelteState.loading = false;
        }
    };

    const deleteCookie = (/** @type {string} */ name) => {
        document.cookie = `${name}=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;`;
    };

    onMount(() => {
        // If user checked "Remember me" on login, the cookie will be set and we can get the user from it
        let previousUser = localStorage.getItem("wasLoggedIn") || null;

        if (previousUser) {
            getUserByCookie().then((user) => {
                if (user) {
                    svelteState.user = user;
                    localStorage.setItem("wasLoggedIn", "true");
                    notifyAlert("success", "Welcome back!");
                    navigate("/dashboard");
                } else {
                    svelteState.user = null;
                    localStorage.removeItem("wasLoggedIn");
                    notifyAlert(
                        "info",
                        "Session expired. Please log in again."
                    );
                }
            });
        } else {
            svelteState.user = null;
        }
    });
</script>

<main>
    {#if svelteState.loading}
        <Loading />
    {/if}

    <SnackBarAlert />

    <Router>
        <Route path="/">
            <Home />
        </Route>
        <Route path="/dashboard">
            {#if svelteState.user?.role === "teacher" || svelteState.user?.role === "admin"}
                <ProtectedRoute
                    component={TeacherDashboard}
                    id="teacher-dashboard"
                />
            {:else}
                <ProtectedRoute component={Dashboard} id="dashboard" />
            {/if}
        </Route>
        <Route path="*">
            <NotFound />
        </Route>
    </Router>
</main>

<style>
</style>
