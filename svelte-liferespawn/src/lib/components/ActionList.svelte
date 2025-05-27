<script>
    import { impactLevels } from "$lib/data/impactLevels";
    import { PlusIcon, SearchIcon } from "svelte-feather-icons";

    let { actions, selectedAction = -1 } = $props();

    let scrollbox = $state();

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

    export function getSelectedAction() {
        return actions[selectedAction];
    }
    export function clear() {
        selectedAction = -1;
    }
</script>

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
                class:searched-item={action.name.includes(searchValue) &&
                    searchValue !== ""}
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

<style>
    .searched-item {
        transform: translateY(-5px);
        transition: 0.1s all;
    }

    .search {
        outline: none;
        background-color: transparent;
        width: 100%;
        color: white;
        font-size: 20px;
    }

    .yes-sel {
        background-color: var(--main-color);
    }
    .not-sel {
        background-color: rgb(36, 36, 36);
    }

    .not-sel:hover {
        transition: 0.1s all;
        background-color: rgb(50, 50, 50);
    }

    .action-list {
        margin-bottom: 30px;
        overflow-x: auto;
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
        background-color: rgba(100, 100, 100, 0.6);
        border-radius: 4px;
    }
</style>
