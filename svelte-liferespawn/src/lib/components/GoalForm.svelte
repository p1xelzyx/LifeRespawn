<script>
    import { Window, ActionList, Time } from "$components";
    import { impactLevels } from "$lib/data/impactLevels";
    import {
        ArrowRightIcon,
        CheckIcon,
        ClockIcon,
        RepeatIcon,
        XIcon,
    } from "svelte-feather-icons";

    let selectedHour = $state(0);
    let selectedMinute = $state(0);
    let times = $state(0);

    let window = $state();
    let actionList = $state();

    let { actions } = $props();
    console.log(actions);

    export function show() {
        window.show();
        action = undefined;
    }

    let action = $derived(actionList?.getSelectedAction());

    let options = $state({ isPositive: true, isDuration: false });

    async function sendNewGoal() {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "new_goal",
                data: {
                    action_id: action.id,
                    duration_minutes: options.isDuration
                        ? selectedHour * 60 + selectedMinute
                        : false,
                    amount: !options.isDuration ? times : false,
                    positive: options.isPositive
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
    <div class="top">
        <h1>New goal</h1>
        <div class="options">
            <button
                class="option-btn"
                onclick={() => (options.isPositive = !options.isPositive)}
                class:moveRight={!options.isPositive}
                ><h2><CheckIcon /> Positive</h2>
                <h2><XIcon /> Negative</h2></button
            >
            <button
                class="option-btn"
                onclick={() => {
                    options.isDuration = !options.isDuration;
                    times = 0;
                }}
                class:moveRight={!options.isDuration}
                ><h2><ClockIcon /> Duration</h2>
                <h2><RepeatIcon /> Amount</h2></button
            >
        </div>
    </div>
    <ActionList bind:this={actionList} {actions} />
    <div class="goal">
        <h2>DO</h2>
        <ArrowRightIcon />
        {#if action}
            <div class="action">
                {impactLevels[action.impact].sign}
                {action.name}
            </div>
        {:else}
            <div class="action invalid">Select action</div>
        {/if}
        <ArrowRightIcon />
        <h2>{options.isPositive ? "AT LEAST" : "MAX"}</h2>
        <ArrowRightIcon />
        {#if options.isDuration}
            <Time bind:selectedHour bind:selectedMinute />
        {:else}
            <h2>
                <input class="times" bind:value={times} type="number" min="0" />
                {times == 1 ? "TIME" : "TIMES"}
            </h2>
        {/if}
        <ArrowRightIcon />
        <h2>PER DAY</h2>

        <div class="end-buttons">
            <button class="window-end-button" onclick={() => window.hide()}>Cancel</button>
            <button class="window-end-button" onclick={sendNewGoal}>Save</button>
        </div>
    </div>
</Window>

<style>
    .end-buttons {
        display: flex;
    }
    .window-end-button {
        margin: 20px;
    }

    .top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }

    .times {
        background-color: transparent;
        border-bottom: 2px solid var(--main-color);
        color: white;
        width: 2em;
        font-size: 1.2em;
        outline: none;
        text-align: center;
    }
    .times:focus {
        border-bottom: 2px solid white;
    }

    .option-btn h2 {
        padding: 5px 15px;
        margin: 0px 5px;
        color: white;
        display: flex;
        align-items: flex;
        gap: 10px;
        position: relative;
        z-index: 1;
    }

    .option-btn::before {
        content: "";
        position: absolute;
        height: 100%;
        width: 50%;
        background-color: var(--main-color);
        transition: all 0.2s;
        z-index: 0;
        border-radius: 10px;
    }

    .option-btn {
        width: 100%;
        position: relative;
        display: flex;
        background-color: transparent;
        border: none;
        z-index: 1;
        overflow: hidden;
    }

    .moveRight::before {
        transform: translateX(100%);
    }

    .moveRight:hover::before {
        transform: translateX(96%);
    }
    .option-btn:not(.moveRight):hover:before {
        transform: translateX(4%);
    }

    .options {
        margin: 30px 0;
        gap: 15px;
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .invalid {
        font-style: italic;
    }
    .goal {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        justify-content: center;
    }
    .action {
        padding: 15px;
        border-radius: 10px;
        background-color: rgb(36, 36, 36);
    }
</style>
