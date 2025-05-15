<script>
    import { ActionForm } from "$components";

    const impactLevels = [
        {
            sign: "🔴",
            name: "Harmful",
            description:
                "This action actively sets you back. It drains energy, causes regret, or reinforces bad habits.",
        },
        {
            sign: "🟠",
            name: "Unhelpful",
            description:
                "Time spent here doesn’t contribute to your goals or well-being. Often feels like a waste.",
        },
        {
            sign: "🟡",
            name: "Neutral",
            description:
                "Doesn’t help or hurt. Just exists. Sometimes necessary, but not meaningful.",
            selected: true,
        },
        {
            sign: "🟢",
            name: "Mildly Beneficial",
            description:
                "A small step in the right direction. Feels good, supports your growth a little.",
        },
        {
            sign: "✅",
            name: "Productive",
            description:
                "Clearly contributes to your goals. Makes you feel better or closer to who you want to be.",
        },
        {
            sign: "💪",
            name: "Strongly Beneficial",
            description:
                "Excellent for long-term growth. Physically, mentally, or emotionally rewarding.",
        },
        {
            sign: "⭐",
            name: "Core Identity",
            description:
                "This defines the person you’re trying to become. Deeply aligned with your ideal self.",
        },
    ];

    let { data } = $props();
    console.log(data);

    let actionForm = $state();
</script>

<section class="app-section">
    <div class="top">
        <h1>Your actions</h1>
        <button onclick={() => actionForm.show()} class="new-action"
            >New action</button
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
