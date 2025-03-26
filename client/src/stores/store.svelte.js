export const svelteState = $state({
    user: null,
    loading: false,
    alert: {
        type: null,
        message: null,
        show: false
    },
});

export const notifyAlert = (type, message) => {
    svelteState.alert.type = type;
    svelteState.alert.message = message;
    svelteState.alert.show = true;
    setTimeout(() => {
        svelteState.alert.show = false;
        svelteState.alert.type = null;
        svelteState.alert.message = null;
    }, 3000);
}
