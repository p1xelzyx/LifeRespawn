<script>
    import { invalidateAll } from "$app/navigation";
    import { Window } from "$components";
    import { logout } from "$utils/logout";
    let window = $state();

    let priority = $state();
    let name = $state("");
    let desc = $state("");

    export function show() {
        priority = 0;
        name = "";
        desc = "";

        window.show();
    }

    async function saveMission() {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "save_mission",
                data: {
                    name,
                    description: desc,
                    priority: priority,
                },
            }),
        });
        if (response.status === 401) return logout();
        if (!response.ok) return alert("error");
        let data = await response.json();
        console.log(data);
        if (data.status === "success") {
            await invalidateAll();
            window.hide();
        }
    }

    
</script>

<Window bind:this={window}>
    <h2>New mission</h2>
    <div class="name-wrap">
        <h3>Name</h3>
        <input class="name" type="text" bind:value={name} />
    </div>
    <div class="desc-wrap">
        <h3>Description (optional)</h3>
        <textarea class="desc" bind:value={desc}></textarea>
    </div>
    <div class="priority-wrap">
        <h3>Priority</h3>
        <div>
            <button
                class="btn"
                class:selected={priority == 0}
                onclick={() => (priority = 0)}>Normal</button
            ><button
                class="btn"
                class:selected={priority == 1}
                onclick={() => (priority = 1)}>High</button
            ><button
                class="btn"
                class:selected={priority == 2}
                onclick={() => (priority = 2)}>Extreme</button
            >
        </div>
    </div>
    <div class="end-buttons">
        <button onclick={window.hide} class="window-end-button">Cancel</button>
        <button onclick={saveMission} class="window-end-button">Save</button>
    </div>
</Window>

<style>
    div:not(.priority-wrap > div) {
        margin: 30px 0;
    }

    h3 {
        margin-bottom: 10px;
    }

    .btn {
        color: white;
        background-color: transparent;
        border: none;
        font-size: 1em;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid var(--main-color);
        transition: all 0.1s;
    }

    .priority-wrap > div {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .selected {
        background-color: var(--main-color);
    }

    .btn:not(.selected):hover {
        scale: 1.1;
    }

    .name,
    .desc {
        background-color: transparent;
        font-size: 1em;
        outline: none;
        color: white;
        padding: 5px;
        background-color: rgb(36, 36, 36);
    }
    .desc {
        resize: none;
        width: 100%;
        height: 100px;
    }
    .name {
        border-bottom: 2px solid var(--main-color);
        max-width: 100%;
    }
    .end-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .window-end-button {
        margin: 30px 10px 0 10px;
    }
</style>
