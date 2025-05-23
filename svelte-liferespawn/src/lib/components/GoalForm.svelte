<script>
    import { Window, ActionList } from "$components";
    import { impactLevels } from "$lib/data/impactLevels";
    import { ArrowRightIcon } from "svelte-feather-icons";

    let window = $state();
    let actionList = $state();

    let { actions } = $props();
    console.log(actions);

    export function show() {
        window.show();
    }

    let actionName = $state();
    let actionSign = $state();

    $effect(() => {
        let action = actionList.getSelectedAction();
        if (!action) return;
        console.log(action);
        actionName = action.name;
        actionSign = impactLevels[action.impact].sign;
    });
</script>

<Window bind:this={window}>
    <ActionList bind:this={actionList} {actions} />

    <div class="goal">
        <h1>DO</h1>
        <ArrowRightIcon />
        {#if actionName}
        <div class="action">
            {actionSign} {actionName}
        </div>
        {:else}
        <div class="action invalid">Select action</div>
        {/if}
    </div>
</Window>

<style>
    .invalid {
        font-style: italic;
    }
    .goal {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }
    .action {
        padding: 15px;
        border-radius: 10px;
        background-color: rgb(36,36,36);
    }
</style>
