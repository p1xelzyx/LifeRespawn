<script>
    import { MoodLog, ActionLog, DailyAnalysis } from "$components";

    let { data } = $props();
    console.log(data);

    let dailyAnalysis = $state();
    $inspect(dailyAnalysis);
    let moodLog = $state();
    let actionLog = $state();
</script>

<section class="app-section">
    <div class="section-1">
        <div class="log-info">
            <p>Write down how you feel right now, or what you just did.</p>
        </div>
        <div class="log-buttons">
            <button class="window-end-button" onclick={moodLog.show}
                >Log mood</button
            >
            <button class="window-end-button" onclick={actionLog.show}
                >Log action</button
            >
        </div>
    </div>

    <div class="section-2">
        <button class="window-end-button" onclick={dailyAnalysis.show}>
            Check today
        </button>
        <p>
            Check what you've completed and see what's still left to do today.
            Stay on track and finish strong!
        </p>
    </div>
</section>

<MoodLog bind:this={moodLog} />
<ActionLog bind:this={actionLog} actions={data.actions} />
<DailyAnalysis bind:this={dailyAnalysis} analysis={data.analysis} />

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
        border-bottom: 1px solid rgb(175, 175, 175);
    }

    .log-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        margin-left: auto;
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

    button {
        margin: 30px;
    }
</style>
