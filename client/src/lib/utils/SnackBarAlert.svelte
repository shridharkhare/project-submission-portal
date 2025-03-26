<script>
    import { svelteState } from "../../stores/store.svelte.js";
</script>

{#if svelteState.alert.show}
    <div class="snackbar {svelteState.alert.type}">
        {svelteState.alert.message}
    </div>
{/if}

<style>
    .snackbar {
        position: fixed;
        bottom: 1rem;
        right: 1rem;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: space-between;
        animation:
            fadeIn 0.3s ease-out,
            fadeOut 0.3s ease-in 2.7s;
    }

    .snackbar.success {
        background-color: var(--success-color, #4caf50);
    }

    .snackbar.error {
        background-color: var(--error-color, #f44336);
    }

    .snackbar.warning {
        background-color: var(--warning-color, #ff9800);
    }

    .snackbar.info {
        background-color: var(--info-color, #2196f3);
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(20px);
        }
    }
</style>
