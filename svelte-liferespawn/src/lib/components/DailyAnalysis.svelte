<script>
    import { Window } from "$components";
    import {
        ArrowRightIcon,
        CheckIcon,
        CheckSquareIcon,
        XIcon,
    } from "svelte-feather-icons";

    let { analysis } = $props();

    let grouped = $derived.by(() => {
        let grouped = { positive: [], inProgress: [], failed: [] };
        for (let item of analysis) {
            let current =
                item.unit == "amount"
                    ? item.current
                    : `${Math.floor(item.current / 60)}h ${item.current % 60}m`;
            let goal =
                item.unit == "amount"
                    ? item.goal
                    : `${Math.floor(item.goal / 60)}h ${item.goal % 60}m`;

            if (item.positive) {
                let arr = [item.name, current, "at least", goal];
                grouped[
                    item.current >= item.goal ? "positive" : "inProgress"
                ].push(arr);
            } else {
                let arr = [item.name, current, "max", goal];
                grouped[item.current <= item.goal ? "positive" : "failed"].push(
                    arr,
                );
            }
        }
        return grouped;
    });

    let window = $state();

    export function show() {
        window.show();
        console.log(analysis);
    }
</script>

<Window bind:this={window} flex={true}>
    <div class="positive">
        <h1><CheckSquareIcon /> Completed / correct</h1>
        {#each grouped.positive as item}
            <p>
                <span class="name">{item[0]}</span><ArrowRightIcon />
                <span class="current">{item[1]}</span>
                / {item[2]}
                {item[3]}
            </p>
        {/each}
        {#if grouped.positive.length == 0}
            <i>None</i>
        {/if}
    </div>
    <div class="inProgress">
        <h1>In progress</h1>
        {#each grouped.inProgress as item}
            <p>
                <span class="name">{item[0]}</span><ArrowRightIcon />
                <span class="current">{item[1]}</span>
                / {item[2]}
                {item[3]}
            </p>
        {/each}
        {#if grouped.inProgress.length == 0}
            <i>None</i>
        {/if}
    </div>
    <div class="failed">
        <h1><XIcon /> Failed</h1>
        {#each grouped.failed as item}
            <p>
                <span class="name">{item[0]}</span><ArrowRightIcon />
                <span class="current">{item[1]}</span>
                / {item[2]}
                {item[3]}
            </p>
        {/each}
        {#if grouped.failed.length == 0}
            <i>None</i>
        {/if}
    </div>
    <button class="window-end-button">Close</button>
</Window>

<style>
    h1 {
        font-size: 1.9em;
        margin-bottom: 15px;
    }

    .name {
        padding: 5px;
        background-color: var(--main-color);
        border-radius: 4px;
    }
    .current {
        font-weight: bold;
        text-decoration: underline;
    }

    .positive h1 {
        color: rgb(52, 209, 31);
    }
    .inProgress h1 {
        color: orange;
    }
    .failed h1 {
        color: red;
    }

    div {
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 2px solid rgb(107, 107, 107);
    }
    i {
        color: rgb(97, 97, 97);
    }
    p {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        font-size: 1.2em;
        margin-left: 15px;
        margin-bottom: 20px;
    }
    button {
        margin: 30px;
    }
</style>
