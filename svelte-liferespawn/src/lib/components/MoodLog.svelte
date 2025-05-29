<script>
    import { invalidateAll } from "$app/navigation";
    import { Window } from "$components";
    import { logout } from "$utils/logout";


    let moodValue = $state(5);
    let valueDisplayColor = $derived(`hsl(${moodValue * 12}, 100%, 50%)`);

    let moodWindow = $state();

    export function show() {
        moodWindow.show();
    }


    async function saveMood() {
        const response = await fetch("/api/post", {
            method: "POST",
            body: JSON.stringify({
                endpoint: "save_mood",
                data: {
                    level: moodValue
                }
            })
        })
        if(response.status === 401) logout();
        if(!response.ok) alert("error");
        
        let data = await response.json();
        console.log(data);
        if (data.status === "success") {
            await invalidateAll();
            moodWindow.hide();
        }
    }
</script>

<Window bind:this={moodWindow}>
    <div class="window-content">
        <h1>How do you feel?</h1>
        <input
            type="range"
            step="0.1"
            min="0"
            max="10"
            bind:value={moodValue}
        />
        <h1 style="color: {valueDisplayColor}">{moodValue}/10</h1>
        <div class="form-buttons">
            <button class="window-end-button" onclick={moodWindow.hide}>Cancel</button>
            <button class="window-end-button" onclick={saveMood}>Save</button>
        </div>
    </div>
</Window>

<style>
    h1 {
        font-size: 2.5em;
        text-align: center;
        margin-bottom: 50px;
    }

    input {
        width: 100%;
        margin-bottom: 20px;
    }

    .window-content {
        height: 100%;
        width: 100%;

        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }

    .form-buttons button {
        margin: 15px;
    }
</style>
