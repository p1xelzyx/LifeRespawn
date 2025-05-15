<script>
    import { ActionForm } from "$components";

    let { data } = $props();
    console.log(data);

    let actionForm = $state();

</script>

<section class="app-section">
    <div class="top">
        <h1>Your actions</h1>
        <button onclick={() => actionForm.show()} class="new-action">New action</button>
    </div>
    <div class="action-list">
        {#each "Clean room.".repeat(10).split(".") as nc}
            <button onclick={() => actionForm.show(true, nc)} class="action">
                <h2>{nc}</h2>
                <p>🟢 Mildly Beneficial</p>
            </button>
        {/each}
    </div>
</section>

<ActionForm bind:this={actionForm}/>



<style>
    h1 {
        font-size: 2em;
    }

    .top {
        display: flex;
        justify-content: space-between;
        margin-bottom: 60px;
    }

    .action-list {
        display: flex;
        flex-wrap: wrap;
        gap: 30px;
        justify-content: center;
    }

    .action {
        background-color: var(--bg-color);
        color: white;
        padding: 10px;
        border-radius: 11px;
        transition: 0.1s all;
    }

    .action:hover {
        background-color: var(--main-color);
        cursor: pointer;
    }

    .new-action {
        font-size: 1.5em;
        color: var(--main-color);
        background-color: transparent;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid var(--main-color);
        transition: 0.1s all;
    }

    .new-action:hover {
        color: white;
        background-color: var(--main-color);
        cursor: pointer;
    }
</style>
