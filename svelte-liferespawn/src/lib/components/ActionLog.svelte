<script>
    import { Window } from "$components";
    import { impactLevels } from "$lib/data/impactLevels";

    let { actions } = $props();

    let window;
    let scrollbox;
    let duration = $state({ h: 0, m: 0, s: 0 });

    export function show() {
        window.show();
    }

    function scroll(data) {
        scrollbox.scrollTo({
            left: scrollbox.scrollLeft + data.deltaY,
        });
    }
</script>

<Window bind:this={window}>
    <div class="selected-action">
        <p>Watch TV</p>
        <p>Productive</p>
    </div>
    <div class="action-list" onwheel={scroll} bind:this={scrollbox}>
        <div class="inside">
            {#each actions as action}
                <button>
                    <h2>{action.name}</h2>
                    <p>
                        {impactLevels[action.impact].sign}
                        {impactLevels[action.impact].name}
                    </p>
                </button>
            {/each}
        </div>
    </div>
    <div class="inputs">
        <div>
            <h2>Duration</h2>
            <div>
                <input type="number" placeholder="0" />
                <p>Hours</p>
            </div>
            <div>
                <input type="number" placeholder="0" />
                <p>Minutes</p>
            </div>
        </div>
    </div>
</Window>

<style>
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
        border-bottom: 2px solid var(--main-color);
        border-top: 2px solid var(--main-color);
    }
    

    .action-list button {
        margin: 10px 20px;
        white-space: nowrap;
        background-color: transparent;
        padding: 15px;
        color: white;
        border-radius: 10px;
        background-color: rgb(36, 36, 36);
    }

    input {
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
</style>
