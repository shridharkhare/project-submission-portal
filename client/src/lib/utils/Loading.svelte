<script>
    const imgUrl = new URL("/src/assets/loading.svg", import.meta.url).href;
</script>

<div class="overlay">
    <div class="loading">
        <img src={imgUrl} alt="Loading" />
    </div>
</div>

<style>
    .overlay {
        display: grid;
        place-items: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 100;
    }
</style>
