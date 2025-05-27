<script>
    import {
        AlertCircleIcon,
        CheckIcon,
        InfoIcon,
        XIcon,
    } from "svelte-feather-icons";
    import { MissionForm } from "$components";
    import { invalidateAll } from "$app/navigation";
    import { logout } from "$utils/logout.js";

    let { data } = $props();

    let missionForm = $state();
    function showDesc(id) {
        descShown = id;
    }
    function hideDesc(id) {
        descShown = -1;
    }

    let descShown = $state(-1);

    async function deleteMission(id) {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "delete_mission",
                data: { id },
            }),
        });
        if (response.status === 401) return logout();
        if (!response.ok) return alert("error");
        let data = await response.json();
        console.log(data);
        if (data.status === "success") {
            await invalidateAll();
        }
    }

    async function completeMission(id) {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "/complete_mission",
                data: { id },
            }),
        });
        if(response.status === 401) return logout();
        if (!response.ok) return alert("error");
        console.log(data);
        if(data.status === "success") {
            await invalidateAll();
        }
    }
</script>

<section class="app-section">
    <div class="top">
        <h1>Your projects / missions</h1>
        <button class="new-mission" onclick={missionForm.show}
            >NEW MISSION</button
        >
    </div>

    <div class="list">
        {#if data?.missions?.length > 0}


        {#each data.missions.sort((a, b) => b.priority - a.priority) as mission}
            <div class="mission">
                <button class="delete" onclick={() => deleteMission(mission.id)}><XIcon size="30" /></button>
                <button class="check" onclick={() => completeMission(mission.id)}><CheckIcon size="30" /></button>
                <h2>{mission.name}</h2>
                <div
                    class="description-box"
                    role="tooltip"
                    onblur={() => hideDesc(mission.id)}
                    onmouseleave={() => hideDesc(mission.id)}
                    onfocus={() => showDesc(mission.id)}
                    onmouseover={() => showDesc(mission.id)}
                >
                    <button class="view-more">view description</button>
                    <div
                        class="description"
                        class:hide={!(mission.id == descShown)}
                    >
                        {#if mission.description}
                            {mission.description}
                        {:else}
                            <i class="gray">No description</i>
                        {/if}
                    </div>
                </div>
                {#if mission.priority == 0}
                    <h3><span>Normal</span><span>priority</span></h3>
                {:else if mission.priority == 1}
                    <h3>
                        <AlertCircleIcon /><span>High</span>priority
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
        {:else}
            <p class="nothing">You currently have no missions</p>
        {/if}
    </div>
</section>

<MissionForm bind:this={missionForm} />

<style>
    .nothing {
        text-align: center;
        width: 100%;
        padding: 30px;
        font-style: italic;
        color: rgb(155, 155, 155);
    }

    h3 {
        font-size: 1em;
    }

    .gray {
        color: rgb(161, 161, 161);
    }
    .description-box {
        position: relative;
    }
    .description {
        position: absolute;
        bottom: 100%;
        min-width: fit-content;
        width: max-content;
        max-width: min(35vw, 400px);
        z-index: 10;
        background-color: rgba(0, 104, 223, 0.377);
        backdrop-filter: blur(4px);
        padding: 10px;
        border-radius: 10px;
    }
    .hide {
        display: none;
    }

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
        height: 30px;
        color: red;
        border-radius: 5px;
    }
    .check {
        height: 30px;
        color: lime;
        border-radius: 5px;
    }
    .delete:hover {
        background-color: red;
        color: white;
    }
    .check:hover {
        background-color: green;
        color: white;
    }
    .view-more {
        padding: 10px;
        border-radius: 10px;
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
