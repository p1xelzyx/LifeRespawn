<script>
    import { impactLevels } from "$lib/data/impactLevels";
    import { ArrowRightIcon, Trash2Icon } from "svelte-feather-icons";
    import { GoalForm, DeleteGoal } from "$components";
    import { logout } from "$utils/logout.js";
    import { invalidateAll } from "$app/navigation";

    let { data } = $props();
    console.log(data);

    let goalForm = $state();
    let deleteGoal = $state();

    const DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];


     async function updateGoalDay(id, day) {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "update_goal_day",
                data: {
                    goal_id: id,
                    day: day
                },
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
</script>

<section class="app-section">
    <div class="top">
        <h1>Goals</h1>
        <button class="new-goal" onclick={() => goalForm.show()}>NEW GOAL</button>
    </div>

    <div class="goal-list">
        {#each data.goals as goal}
            <div class="goal">
                <button class="trash-icon" onclick={() => deleteGoal.show(goal.id)}><Trash2Icon/></button>
                <h3 class="action">
                    {impactLevels[data.actions.find(e => e.id == goal.action_id).impact].sign}
                    {data.actions.find(e => e.id == goal.action_id).name}
                </h3>
                <ArrowRightIcon />
                <h3 class="goal-label" class:negative={!goal.positive}>
                    {#if goal.positive == 1}
                        {#if goal.amount}
                            at least {goal.amount}
                            {goal.amount === 1 ? "time" : "times"} per day
                        {:else}
                            at least {Math.floor(goal.duration_minutes / 60)}h {goal.duration_minutes %
                                60}min per day
                        {/if}
                    {:else if goal.amount === 0 && goal.duration_minutes === 0}
                        dont do
                    {:else if goal.amount}
                        max {goal.amount}
                        {goal.amount === 1 ? "time" : "times"} per day
                    {:else}
                        max {Math.floor(goal.duration_minutes / 60)}h {goal.duration_minutes %
                            60}min per day
                    {/if}
                </h3>
                <div class="days-list">
                    {#each DAY_NAMES as dayName, i}
                        <button class="day" class:day-selected={goal.days[i]} onclick={() => updateGoalDay(goal.id, i)}>
                            {dayName}
                        </button>
                    {/each}
                </div>
            </div>
        {/each}
    </div>
</section>

<DeleteGoal bind:this={deleteGoal}/>
<GoalForm bind:this={goalForm} actions={data.actions}/>

<style>
    .trash-icon {
        color: red;
        border: none;
        background-color: transparent;
        padding: 0;
        margin-right: 10px;
    }

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
    .day:hover {
        scale: 1.1;
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
