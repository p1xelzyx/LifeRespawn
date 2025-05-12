<script>
    import { Window } from "$components";

    let moodValue = $state(5);
    let valueDisplayColor = $derived(`hsl(${moodValue * 12}, 100%, 50%)`);

    let moodWindow = $state();
</script>

<section class="app-section section-1">
    <div class="log-info">
        <p>Write down how you feel right now, or what you just did.</p>
        <p>You can always log your actions at the end of the day down below.</p>
    </div>
    <div class="log-buttons">
        <button class="main-color-3d-button" onclick={moodWindow.show}
            >Log mood</button
        >
        <button class="main-color-3d-button">Log action</button>
    </div>
</section>

<section class="app-section section-2">
    <button class="main-color-3d-button"> Finish your day </button>
    <p>What did you do today?</p>
</section>


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
    .log-info p {
        font-size: 1.1em;
        margin-bottom: 15px;
    }
    .section-1 {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        flex-wrap: wrap;
    }

    .log-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        margin-left: auto;
    }
    .log-buttons button {
        margin: 40px;
        font-size: 1.3em;
        width: 150px;
        height: 150px;
        padding: 30px;
        border-radius: 50%;
    }

    .section-2 {
        padding: 40px;
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }
    .section-2 p {
        font-size: 1.3em;
    }
    .section-2 button {
        padding: 30px;
        font-size: 1.5em;
        border-radius: 20px;
    }

    /* v mood window v */
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
    /* ^ mood window ^ */

</style>
