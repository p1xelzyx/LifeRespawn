<script>
    import { goto, invalidateAll } from "$app/navigation";
    import { Window } from "$components";
    import { logout } from "$utils/logout";
    import { redirect } from "@sveltejs/kit";
    let window = $state();

    const { impactLevels } = $props();

    let selectValue = $state(impactLevels.findIndex((e) => e.selected));

    let isEditMode = $state(false);
    let actionName = $state("");
    let actionId = $state(-1);

    export function show(editMode, action) {
        isEditMode = editMode;

        if (action) {
            actionName = action.name;
            selectValue = action.impact;
            actionId = action.id;
        }
        if (!isEditMode) {
            actionName = "";
            selectValue = 2;
        }

        window.show();
    }

    async function sendNewAction() {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "new_action",
                data: { name: actionName, impact: selectValue },
            }),
            headers: {
                "content-type": "application/json",
            },
        });
        if(response.status === 401) {
            return logout();
        }
        let data = await response.json();
        if (data.status === "success") {
            await invalidateAll();
            window.hide();
        }
    }

    async function deleteAction() {

        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "delete_action",
                data: { id: actionId }
            }),
            headers: {
                "content-type": "application/json",
            },
        });

        if(response.status === 401) {
            return logout();
        }
        let data = await response.json();
        console.log(data);
        if (data.status === "success") {
            await invalidateAll();
            window.hide();
        }
    }
    async function editAction() {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "edit_action",
                data: { id: actionId, name: actionName, impact: selectValue }
            }),
            headers: {
                "content-type": "application/json",
            },
        });
        if(response.status === 401) {
            return logout();
        }
        let data = await response.json();
        console.log(data);
        if (data.status === "success") {
            await invalidateAll();
            window.hide();
        }
    }
</script>

<Window flex={true} bind:this={window}>
    <h1>{isEditMode ? "Edit action" : "Create your action"}</h1>

    <div class="same-row">
        <h2>Name</h2>

        <input
            bind:value={actionName}
            type="text"
            placeholder="E.g. Watch TV"
        />
    </div>

    <div class="same-row">
        <h2>Impact on life</h2>
        <select bind:value={selectValue}>
            {#each impactLevels as level, i}
                <option selected={level.selected} value={i}
                    >{level.sign} {level.name}</option
                >
            {/each}
        </select>
    </div>

    <p>
        {impactLevels[selectValue].sign}
        {impactLevels[selectValue].description}
    </p>

    <div class="end-buttons">
        {#if isEditMode}
            <button class="window-end-button-red" onclick={deleteAction}
                >Delete</button
            >
            <button class="window-end-button" onclick={editAction}>Save</button>
        {:else}
            <button class="window-end-button" onclick={window.hide}
                >Cancel</button
            >
            <button class="window-end-button" onclick={sendNewAction}
                >Save</button
            >
        {/if}
    </div>
</Window>

<style>
    h2 {
        color: var(--main-color);
    }

    select {
        font-size: 1.15em;
        outline: none;
        background-color: rgb(48, 48, 48);
        padding: 0.5em;
        color: white;
        border: none;
    }
    input::placeholder {
        font-style: italic;
    }
    input {
        font-size: 1.15em;
        outline: none;
        background-color: rgb(48, 48, 48);
        padding: 0.5em;
        color: white;
    }

    input,
    select {
        width: 100%;
        max-width: 250px;
    }

    .same-row {
        display: flex;
        gap: 15px;
        align-items: center;
        border-bottom: 3px solid var(--main-color);
        width: 100%;
        max-width: 500px;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-top: 40px;
        font-size: 1.1em;
    }

    p {
        margin: 40px 0;
        font-size: 1.1em;
        max-width: 500px;
    }

    .end-buttons {
        justify-content: center;
        display: flex;
        width: 100%;
        flex-wrap: wrap;
        margin-top: auto;
    }
    .end-buttons button {
        min-width: fit-content;
        margin: 7px;
        padding: 12px;
    }
</style>
