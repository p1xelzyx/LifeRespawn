<script>
    import { ActionForm } from "$components";

    import { impactLevels } from "$lib/data/impactLevels.js";

    let { data } = $props();
    console.log(data);

    let actionForm = $state();
</script>

<section class="app-section">
    <div class="top">
        <h1>Your actions</h1>
        <button onclick={() => actionForm.show()} class="new-action"
            >NEW ACTION</button
        >
    </div>
    <div class="action-list">
        {#if data.actions.length > 0}
            {#each data.actions as action}
                <button
                    onclick={() => actionForm.show(true, action)}
                    class="action"
                >
                    <h2>{action.name}</h2>
                    <p>
                        {impactLevels[action.impact].sign}
                        {impactLevels[action.impact].name}
                    </p>
                </button>
            {/each}
        {:else}
            <p class="no-actions">You don't have any actions yet</p>
        {/if}
    </div>
</section>

<ActionForm {impactLevels} bind:this={actionForm} />

<style>
    .no-actions {
        font-style: italic;
        color: gray;
        padding: 50px;
    }

    h1 {
        font-size: 2em;
    }

    .top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 60px;
    }

    .action-list {
        display: flex;
        flex-wrap: wrap;
        gap: 30px;
        justify-content: center;
        border-radius: 15px;
        border: 2px solid var(--main-color);
        padding: 20px;
    }

    .action {
        background-color: var(--bg-color);
        color: white;
        padding: 15px;
        border-radius: 11px;
        transition: 0.1s all;
    }

    .action:hover {
        background-color: var(--main-color);
        cursor: pointer;
    }

    .new-action {
        font-size: 1.3em;
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
