<script>
    import { Window, ActionList } from "$components";
    import { impactLevels } from "$lib/data/impactLevels";
    import { logout } from "$utils/logout";
    import { PlusIcon, SearchIcon } from "svelte-feather-icons";
    import PopUp from "./PopUp.svelte";

    let { actions } = $props();

    let window = $state();
    let scrollbox = $state();
    let actionList = $state();

    let durationEnabled = $state(true);
    let duration = $state({ h: 0, m: 0 });

    $effect(() => {
        if(!durationEnabled) duration = {h: 0, m: 0};
    });

    export function show() {
        window.show();
        selectedAction = -1;
    }



    
    let selectedAction = $derived(actionList?.getSelectedAction());
    



    async function sendActionLog() {
        // ker action, duration
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "save_action",
                data: {
                    action_id: selectedAction.id,
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
        {#if selectedAction?.name}
            <div class="selected-action">
                <h2>{selectedAction.name}</h2>
                <p>
                    {impactLevels[selectedAction.impact].sign}
                    {impactLevels[selectedAction.impact].name}
                </p>
            </div>
        {:else}
            <div class="no-action">
                <p>Select action</p>
            </div>
        {/if}

       
        <ActionList bind:this={actionList} {actions}/>
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

    

    .selected-action {
        text-align: center;
        margin-bottom: 40px;
        padding: 20px;
        border-radius: 20px;
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

</style>
