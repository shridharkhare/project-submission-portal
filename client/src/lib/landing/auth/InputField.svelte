<script>
    export let id;
    export let label;
    export let type = "text";
    export let value = "";
    export let error = "";
    export let ariaInvalid = "";
    export let ariaDescribedby;
    export let placeholder = "";
    export let onInput;
</script>

<label>
    {label}
    <input
        bind:value
        on:input={onInput}
        {type}
        {id}
        {placeholder}
        aria-invalid={ariaInvalid === ""
            ? "grammar"
            : ariaInvalid === "true"
              ? true
              : false}
        aria-describedby={ariaDescribedby}
        required
    />
    <small id={ariaDescribedby}>{error}</small>
</label>

<style>
    input {
        height: 2.5rem;
    }
</style>
