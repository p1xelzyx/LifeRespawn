<script>
    import { AlertCircleIcon, CheckIcon, XIcon } from "svelte-feather-icons";

    let tmpMissions = [
        {
            name: "zbris nsa",
            description: "zbris nsa iz ucnega nacrta",
            priority: 2,
        },
        { name: "predstavitev ukr", description: "", priority: 1 },
        {
            name: "nared bajto",
            description: "na polu nared bajto z elektriko",
            priority: 2,
        },
        { name: "posesej bajto", description: "", priority: 0 },
    ];
</script>

<section class="app-section">
    <div class="top">
        <h1>Your projects / missions</h1>
        <button class="new-mission">NEW MISSION</button>
    </div>

    <div class="list">
        {#each tmpMissions as mission}
            <div class="mission">
                <button class="delete"><XIcon /></button>
                <button class="check"><CheckIcon /></button>
                <h2>{mission.name}</h2>
                <button class="view-more">description</button>
                {#if mission.priority == 0}
                    <h3><span>Normal</span><span>priority</span></h3>
                {:else if mission.priority == 1}
                    <h3>
                        <AlertCircleIcon /><span
                            >Extreme</span
                        >priority
                    </h3>
                {:else}
                    <h3>
                        <span class="red"><AlertCircleIcon /></span><span
                            >Extreme</span
                        >priority
                    </h3>
                {/if}
            </div>
        {/each}
    </div>
</section>

<style>
    .red {
        color: red;
    }
    h3 {
        margin-left: auto;
        text-align: center;
        font-size: 1.2em;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    button {
        color: white;
        border: none;
        background-color: transparent;
        font-size: 1em;
    }

    .delete {
        color: red;
    }
    .check {
        color: lime;
    }
    .view-more {
        border-radius: 10px;
        padding: 10px;
        background-color: var(--main-color);
    }

    .mission {
        border-radius: 15px;
        display: flex;
        justify-content: start;
        flex-wrap: wrap;
        align-items: start;
        flex-direction: row;
        gap: 20px;
        background-color: rgb(36, 36, 36);
        padding: 15px;
        margin: 20px 0;
    }
    .top {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 20px;
    }

    .new-mission {
        font-size: 1.3em;
        color: var(--main-color);
        background-color: transparent;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid var(--main-color);
        transition: 0.1s all;
    }

    .new-mission:hover {
        color: white;
        background-color: var(--main-color);
        cursor: pointer;
    }

    .list {
        margin-top: 30px;
        border-radius: 10px;
        border: 2px solid var(--main-color);
        padding: 20px;
    }
</style>
