<script>
    import { Window } from "$components";

    let window = $state();

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
    let selectValue = $state(impactLevels.findIndex((e) => e.selected));

    export function show() {
        window.show();
    }
</script>

<Window flex={true} bind:this={window}>
    <h1>Create your action</h1>

    <div class="flex-wrap">
        <div class="same-row">
            <h2>Name</h2>

            <input type="text" placeholder="E.g. Watch TV" />
        </div>

        <div class="same-row">
            <h2>Impact on life</h2>
            <select bind:value={selectValue}>
                {#each impactLevels as level, i}
                    <option selected={level.selected} value={i}
                        >{level.sign} {level.name}</option
                    >
                {/each}
            </select>
        </div>
    </div>

    <p>{impactLevels[selectValue].sign} {impactLevels[selectValue].description}</p>

    <div class="end-buttons">
        <button class="window-end-button">Cancel</button>
        <button class="window-end-button">Save</button>
    </div>
</Window>

<style>
    .flex-wrap {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 15px;
    }

    h2 {
        color: var(--main-color);
    }

    select {
        font-size: 1.15em;
        outline: none;
        background-color: rgb(48, 48, 48);
        padding: 0.5em;
        color: white;
        border: none;
    }
    input::placeholder {
        font-style: italic;
    }
    input {
        font-size: 1.15em;
        outline: none;
        background-color: rgb(48, 48, 48);
        padding: 0.5em;
        color: white;
    }

    input,select {
        width: 100%;
        max-width: 250px;
    }

    .same-row {
        display: flex;
        gap: 15px;
        align-items: center;
        border-bottom: 3px solid var(--main-color);
        width: 100%;
        max-width: 500px;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-top: 40px;
        font-size: 1.1em;
    }

    p {
        margin: 40px 0;
        font-size: 1.1em;
    }

    .end-buttons {
        justify-content: center;
        display: flex;
        width: 100%;
        flex-wrap: wrap;
        margin-top: auto;
    }
    .end-buttons button {
        min-width: fit-content;
        margin: 7px;
        padding: 12px;
    }
</style>
