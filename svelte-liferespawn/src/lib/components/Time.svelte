<script>
    const hoursArr = Array.from({ length: 25 }, (_, i) => i);;
    const minutesArr = Array.from({ length: 61 }, (_, i) => i);;

</script>

<div class="wrap">
    <div class="scroll">
        {#each hoursArr as h}
            <span>{h}</span>
        {/each}
    </div>
    <div>:</div>
    <div class="scroll">
        {#each minutesArr as m}
            <span>{m}</span>
        {/each}
    </div>
</div>

<style>
    .wrap {
        align-items: center;
        display: flex;
        gap: 10px;
        font-size: 2em;
        height: 200px;
    }

    .scroll {
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>
