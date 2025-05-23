<script>
    import { impactLevels } from "$lib/data/impactLevels";
    import { ArrowRightIcon } from "svelte-feather-icons";
    import { GoalForm } from "$components";

    let { data } = $props();

    let goalForm = $state();

    let tmpGoals = [
        {
            type: 0,
            action: { impact: 1, name: "gledanje tv" },
            duration: 60,
            amount: 0,
            days: [1, 1, 1, 1, 1, 1, 1],
        },
        {
            type: 1,
            action: { impact: 4, name: "odnes smeti vn" },
            duration: 0,
            amount: 2,
            days: [1, 1, 1, 1, 0, 0, 0],
        },
        {
            type: 1,
            action: { impact: 4, name: "učit se" },
            duration: 0,
            amount: 2,
            days: [0, 0, 1, 1, 1, 1, 0],
        },
    ];
    const DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
</script>

<section class="app-section">
    <div class="top">
        <h1>Goals</h1>
        <button class="new-goal" onclick={() => goalForm.show()}>NEW GOAL</button>
    </div>

    <div class="goal-list">
        {#each tmpGoals as goal}
            <div class="goal">
                <h3 class="action">
                    {impactLevels[goal.action.impact].sign}
                    {goal.action.name}
                </h3>
                <ArrowRightIcon />
                <h3 class="goal-label" class:negative={!goal.type}>
                    {#if goal.type == 1}
                        {#if goal.amount}
                            at least {goal.amount}
                            {goal.amount === 1 ? "time" : "times"} per day
                        {:else}
                            at least {Math.floor(goal.duration / 60)}h {goal.duration %
                                60}min per day
                        {/if}
                    {:else if goal.amount === 0 && goal.duration === 0}
                        dont do
                    {:else if goal.amount}
                        max {goal.amount}
                        {goal.amount === 1 ? "time" : "times"} per day
                    {:else}
                        max {Math.floor(goal.duration / 60)}h {goal.duration %
                            60}min per day
                    {/if}
                </h3>
                <div class="days-list">
                    {#each DAY_NAMES as dayName, i}
                        <button class="day" class:day-selected={goal.days[i]}>
                            {dayName}
                        </button>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
</section>

<GoalForm bind:this={goalForm} actions={data.actions}/>

<style>
    .goal-label {
        border-radius: 10px;
        padding: 10px;
        background-color: rgba(0, 255, 0, 0.4);
    }
    .negative {
        background-color: rgba(255, 0, 0, 0.4);
    }

    .days-list {
        margin-left: auto;
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }

    .day {
        padding: 10px;
        background-color: rgb(36, 36, 36);
        border-radius: 10px;
        color: white;
        font-size: 1em;
    }
    .day-selected {
        background-color: var(--main-color);
    }

    .action {
        border-radius: 10px;
        background-color: rgb(36, 36, 36);
        padding: 10px;
    }

    .goal {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        align-items: center;
        margin: 30px 0;
        padding: 15px 0;
        border-top: 2px solid var(--main-color);
        border-bottom: 2px solid var(--main-color);
    }

    .top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        flex-wrap: wrap;
    }

    .new-goal {
        font-size: 1.3em;
        color: var(--main-color);
        background-color: transparent;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid var(--main-color);
        transition: 0.1s all;
    }

    .new-goal:hover {
        color: white;
        background-color: var(--main-color);
        cursor: pointer;
    }
</style>
