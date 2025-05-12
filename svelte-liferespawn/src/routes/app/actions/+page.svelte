<script>
    import { Window } from "$components";

    let actionWindow;


    const impactLevels = [
        {
            name: "🔴 Harmful",
            description:
                "This action actively sets you back. It drains energy, causes regret, or reinforces bad habits.",
        },
        {
            name: "🟠 Unhelpful",
            description:
                "Time spent here doesn’t contribute to your goals or well-being. Often feels like a waste.",
        },
        {
            name: "🟡 Neutral",
            description:
                "Doesn’t help or hurt. Just exists. Sometimes necessary, but not meaningful.",
        },
        {
            name: "🟢 Mildly Beneficial",
            description:
                "A small step in the right direction. Feels good, supports your growth a little.",
        },
        {
            name: "✅ Productive",
            description:
                "Clearly contributes to your goals. Makes you feel better or closer to who you want to be.",
        },
        {
            name: "💪 Strongly Beneficial",
            description:
                "Excellent for long-term growth. Physically, mentally, or emotionally rewarding.",
        },
        {
            name: "🌟 Core Identity",
            description:
                "This defines the person you’re trying to become. Deeply aligned with your ideal self.",
        },
    ];
</script>

<section class="app-section">
    <div class="top">
        <h1>Your actions</h1>
        <button onclick={actionWindow.show} class="new-action">New action</button>
    </div>
    <div class="action-list">
        {#each ". ".repeat(10).split(".") as nc}
            <button class="action">
                <h2>Clean room</h2>
                <p>🟢 Mildly Beneficial</p>
            </button>
        {/each}
    </div>
</section>

<Window bind:this={actionWindow}>
    test
</Window>



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
    }

    .action {
        background-color: var(--bg-color);
        color: white;
        padding: 20px;
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
