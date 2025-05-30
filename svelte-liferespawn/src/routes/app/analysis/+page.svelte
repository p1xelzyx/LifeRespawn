<script>
    let selectedId = $state(0);
    import { GoalHistory, MoodGraph } from "$components";

    let options = $state([
        "Goal History",
        "Mood Graph",
        "Missions",
        "Action Impact",
    ]);
</script>

<!-- todo 

- koledar z dnevi kdaj vsak dan pokaze rdeca ali zelene, hover pokaze kok golov je blo narjenih, ali prazno ce ni blo golov tist dan
- graf mood
- completed missions
- korelacija med actioni in kako vpliva na mood
-->

<section class="app-section">
    <h1 class="title">Analysis</h1>
    <div class="wrap">
        <div class="selection">
            {#each options as opt, i}
                <button
                    class="select-option"
                    class:selected={selectedId == i}
                    onclick={() => (selectedId = i)}>{opt}</button
                >
            {/each}
        </div>
        {#if selectedId == 0}
            <GoalHistory />
        {:else if selectedId == 1}
            <MoodGraph />
        {:else if selectedId == 2}
            <div>missions</div>
        {:else}
            <div>action graph</div>
        {/if}
    </div>
</section>

<style>
    .title {
        margin-bottom: 20px;
    }

    .wrap {
        display: flex;
        justify-content: space-between;
        gap: 20px;
    }
    .selection {
        display: flex;
        gap: 5px;
        flex-direction: column;
        max-width: fit-content;
        flex-wrap: wrap;
    }
    @media only screen and (max-width: 600px) {
        .selection {
            flex-direction: row;
        }
        .wrap {
            flex-direction: column;
        }
    }
    .select-option {
        padding: 10px;
        background-color: rgb(36, 36, 36);
        color: white;
        font-size: 1em;
        transition: 0.1s all;
    }
    .select-option:not(.selected):hover {
        background-color: rgb(24, 24, 24);
    }
    .selected {
        background-color: var(--main-color);
    }
</style>
