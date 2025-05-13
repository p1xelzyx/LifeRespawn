<script>
    import { Window } from "$components";


    let moodValue = $state(5);
    let valueDisplayColor = $derived(`hsl(${moodValue * 12}, 100%, 50%)`);

    let moodWindow = $state();

    export function show() {
        moodWindow.show();
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
            <button class="end-button">Ok</button>
            <button class="end-button" onclick={moodWindow.hide}>Cancel</button>
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
        width: 500px;
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

    .end-button {
        font-size: 1.4em;
        border: 2px solid var(--main-color);
        color: var(--main-color);
        border-radius: 15px;
        padding: 20px;
        margin: 15px;
        transition: 0.1s all;
        background-color: transparent;
    }
    .end-button:hover {
        color: white;
        background-color: var(--main-color);
    }
</style>
