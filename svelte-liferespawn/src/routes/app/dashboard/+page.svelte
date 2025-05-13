<script>
    import { MoodLog } from "$components";

    let moodLog = $state();
</script>

<section class="app-section section-1">
    <div class="log-info">
        <p>Write down how you feel right now, or what you just did.</p>
        <p>You can always log your actions at the end of the day down below.</p>
    </div>
    <div class="log-buttons">
        <button class="main-color-3d-button" onclick={moodLog.show}
            >Log mood</button
        >
        <button class="main-color-3d-button">Log action</button>
    </div>
</section>

<section class="app-section section-2">
    <button class="main-color-3d-button"> Finish your day </button>
    <p>What did you do today?</p>
</section>

<MoodLog bind:this={moodLog}/>


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

</style>
