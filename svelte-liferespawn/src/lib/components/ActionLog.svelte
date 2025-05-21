<script>
    import { Window } from "$components";
    import { impactLevels } from "$lib/data/impactLevels";
    import { logout } from "$utils/logout";
    import { PlusIcon, SearchIcon } from "svelte-feather-icons";
    import PopUp from "./PopUp.svelte";

    let { actions } = $props();

    let window = $state();
    let scrollbox = $state();

    let durationEnabled = $state(true);
    let duration = $state({ h: 0, m: 0 });

    $effect(() => {
        if(!durationEnabled) duration = {h: 0, m: 0};
    });

    export function show() {
        window.show();
        selectedAction = -1;
    }

    /** CHAT GPT */

    let scrollTarget = $state(0);
    let isScrolling = $state(false);

    function scroll(data) {
        data.preventDefault();

        const maxScroll = scrollbox.scrollWidth - scrollbox.clientWidth;

        scrollTarget += data.deltaY;
        scrollTarget = Math.max(0, Math.min(scrollTarget, maxScroll)); // Clamp target

        startSmoothScroll();
    }

    function startSmoothScroll() {
        if (isScrolling) return;
        isScrolling = true;

        function step() {
            const current = scrollbox.scrollLeft;
            const distance = scrollTarget - current;

            scrollbox.scrollLeft += distance * 0.2;

            if (Math.abs(distance) > 2) {
                requestAnimationFrame(step);
            } else {
                scrollbox.scrollLeft = scrollTarget;
                isScrolling = false;
            }
        }

        requestAnimationFrame(step);
    }
    function trueScroll() {
        if (!isScrolling) {
            scrollTarget = scrollbox.scrollLeft;
        }
    }

    /** ---------------- */
    let actionElements = $state([]);
    let searchValue = $state("");
    $effect(() => {
        for (let e of actionElements) {
            let parseId = Number(e.id.split("_")[1]);

            if (
                actions.find((a) => a.id === parseId).name.includes(searchValue)
            ) {
                e.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                });

                break;
            }
        }
    });

    let selectedAction = $state(-1);
    function getSelectedAction() {
        if (selectedAction < 0) return false;
        return actions[selectedAction];
    }

    async function sendActionLog() {
        // ker action, duration
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "save_action",
                data: {
                    action_id: getSelectedAction()?.id,
                    duration_minutes: durationEnabled ? duration.h * 60 + duration.m : false,
                },
            }),
        });
        if (response.status === 401) return logout();
        if (!response.ok) return alert("error");

        let data = await response.json();
        console.log(data);
        if (data.status === "success") {
            window.hide();
        }
    }


</script>

<Window bind:this={window}>
    {#if actions.length > 0}
        {#if selectedAction > -1}
            <div class="selected-action">
                <h2>{actions[selectedAction].name}</h2>
                <p>
                    {impactLevels[actions[selectedAction].impact].sign}
                    {impactLevels[actions[selectedAction].impact].name}
                </p>
            </div>
        {:else}
            <div class="no-action">
                <p>Select action</p>
            </div>
        {/if}

        <div style="display: flex; gap: 5px;">
            <SearchIcon size="20" /><input
                type="text"
                class="search"
                placeholder="Search"
                bind:value={searchValue}
            />
        </div>
        <div
            class="action-list"
            onscroll={trueScroll}
            onwheel={scroll}
            bind:this={scrollbox}
        >
            <div class="inside">
                {#each actions as action, i}
                    <button
                        bind:this={actionElements[i]}
                        onclick={() => (selectedAction = i)}
                        class={selectedAction === i ? "yes-sel" : "not-sel"}
                        id={"actionId_" + action.id}
                    >
                        <h2>{action.name}</h2>
                        <p>
                            {impactLevels[action.impact].sign}
                            {impactLevels[action.impact].name}
                        </p></button
                    >
                {/each}
            </div>
        </div>
        <div class="inputs">
            <div>
                <div class="duration-title-div">
                    <h2>Duration</h2>
                    <input
                        type="checkbox"
                        bind:checked={durationEnabled}
                        class="duration-checkbox"
                    />
                </div>
                <div class:disabled={!durationEnabled}>
                    <div>
                        <input
                            type="number"
                            min=0
                            bind:value={duration.h}
                        />
                        <p>Hours</p>
                    </div>
                    <div>
                        <input
                            type="number"
                            min=0
                            bind:value={duration.m}
                        />
                        <p>Minutes</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="end">
            <button class="window-end-button" onclick={window.hide}
                >Cancel</button
            >
            <button class="window-end-button" onclick={sendActionLog}
                >Save</button
            >
        </div>
    {:else}
        <p>You do not have any actions.</p>
        <a href="./actions">Create an action <PlusIcon size="20" /></a>
    {/if}
</Window>

<style>
    .disabled {
        opacity: 0.7;
        pointer-events: none;
    }

    .duration-title-div {
        display: flex;
        align-items: center;
    }
    .duration-checkbox {
        width: 20px;
        height: 20px;
    }

    .end {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
    }
    .end button {
        margin: 20px;
    }

    a {
        display: inline-block;
        color: white;
        font-size: 1em;
        margin-top: 20px;
        display: flex;
        align-items: center;
    }

    .search {
        outline: none;
        background-color: transparent;
        width: 100%;
        color: white;
        font-size: 20px;
    }

    .selected-action {
        text-align: center;
        margin-bottom: 40px;
        padding: 20px;
        border-radius: 20px;
        background-color: rgb(36, 36, 36);
    }

    .yes-sel {
        background-color: var(--main-color);
    }
    .not-sel {
        background-color: rgb(36, 36, 36);
    }

    .no-action {
        background-color: rgb(36, 36, 36);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 40px;
    }
    .no-action p {
        font-style: italic;
    }

    .action-list {
        margin-bottom: 30px;
        overflow-x: auto;
        max-width: 500px;
    }
    .inside {
        margin-bottom: 20px;
        display: flex;
        overflow-x: visible;
        width: fit-content;
        min-width: 100%;
        border-bottom: 2px solid var(--main-color);
        border-top: 2px solid var(--main-color);
    }

    .action-list button {
        margin: 10px 20px;
        white-space: nowrap;
        padding: 15px;
        color: white;
        border-radius: 10px;
    }

    .inputs input {
        box-sizing: content-box;
        width: 4em;
        font-size: 1.2em;
        background-color: transparent;
        color: white;
        outline: none;
        border-bottom: 2px solid var(--main-color);
        margin-right: 10px;
    }

    .inputs p {
        display: inline-block;
    }

    ::-webkit-scrollbar {
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-corner {
        background: transparent;
    }

    ::-webkit-scrollbar-button {
        display: none;
        background: transparent;
        height: 0;
        width: 0;
    }

    ::-webkit-scrollbar-thumb {
        background-color: rgba(100, 100, 100, 0.6); /* Customize thumb */
        border-radius: 4px;
    }
</style>
